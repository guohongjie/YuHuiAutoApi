#-*-coding:utf-8 -*-
from app.main import views
from flask import render_template,request,make_response,jsonify,session
from app import db
from app.config.api_models import Project
from app.config.user_models import DeptName
import datetime
@views.route('/projectIndex',methods=['GET','POST'])
def project_select():
    """API测试首页"""
    api_project = Project.query.with_entities(Project.project).distinct().all()
    #提取测试项目,传入页面中
    test_group = DeptName.query.filter(DeptName.status==1).all()
    return render_template("project_edit.html", api_project=api_project,
                           test_groups=test_group)

@views.route('/projectSearch',methods=['GET'])
def project_search():
    project = request.args.get('project')# 项目名称
    test_group = request.args.get('test_group')
    pro_status = request.args.get("pro_status")
    if pro_status=="None":
        if project=='None' and test_group=='None':
            #当项目为空、接口名为空、状态为 全部
            datas = db.session.query(Project.id,Project.project,Project.description,Project.domain,Project.test_group).all()
        elif project=="None" and test_group!='None':
            #项目为空、接口名为空、状态不为all
            datas = db.session.query(Project.id,Project.project,Project.description,Project.domain,Project.test_group).filter_by(test_group=test_group).all()
        elif project!='None' and test_group=='None':
            datas = db.session.query(Project.id,Project.project,Project.description,Project.domain,Project.test_group).filter_by(project=project).all()
        else:
            datas = db.session.query(Project.id,Project.project,Project.description,Project.domain,Project.test_group).filter_by(project=project,test_group=test_group).all()
    else:
        date = datetime.datetime.now().strftime('%Y-%m-%d 12:00:00')
        if pro_status=="0":
            datas = db.session.query(Project.id,Project.project,Project.description,Project.domain,Project.test_group).filter_by(use_status=0).all()
        elif pro_status=="1":
            datas = db.session.query(Project.id,Project.project,
                                     Project.description,Project.domain,
                                     Project.test_group).filter(
                                     Project.use_status==1).filter(
                                     Project.endDate>=date).all()
        elif pro_status=="2":
            datas = db.session.query(Project.id, Project.project,
                                     Project.description, Project.domain,
                                     Project.test_group).filter(
                Project.use_status == 1).filter(
                Project.startDate >= date).all()
        elif pro_status=="3":
            datas = db.session.query(Project.id, Project.project,
                                     Project.description, Project.domain,
                                     Project.test_group).filter(
                Project.use_status == 1).filter(
                Project.endDate<=date).all()

    resp = {"status": 200, "datas": datas}
    msg_resp = make_response(jsonify(resp))
    return msg_resp
@views.route("/projectSingleDatas",methods=["GET"])
def projectSingleDatas():
    pid = request.args.get("pid")
    datas =Project.query.filter(Project.id==pid).first()
    msg = {"project_name":datas.project,"project_en":datas.project_en,"project_domain":datas.domain,
           "project_status":datas.use_status,"startDate":str(datas.startDate)[:10],"endDate":str(datas.endDate)[:10],
           "RC":datas.description,"id":datas.id
           }
    return make_response(jsonify({"code":200,"datas":msg}))
@views.route("/projectUpdate",methods=["GET"])
def projectUpdate():
    pid = request.args.get("pid")
    project_name = request.args.get("project")
    project_en = request.args.get("project_en")
    domain = request.args.get("domain")
    description = request.args.get("description")
    startDate = request.args.get("startDate")
    endDate = request.args.get("endDate")
    project_status = request.args.get("project_status")
    if project_name == "" or domain == "" or description == "" or startDate == "" or endDate =="":
        resp = {'code': '400',"datas": "项目名称 or 项目domain or 项目描述 or 日期 不能为空!"}
        return make_response(jsonify(resp))
    try:
        datas = Project.query.filter_by(id=pid).update(dict(
        project=project_name, project_en=project_en, domain=domain,
        description=description, startDate=startDate, endDate=endDate,
        use_status=project_status))
        db.session.commit()
        resp = {'datas': '更新成功', 'code': '200'}
    except Exception as e:
        db.session.rollback()
        resp = {'datas': str(e), 'code': '400'}
    return make_response(jsonify(resp))
@views.route('/projectInsert',methods=['POST','GET'])
def project_insert():
    """增加测试项目步骤接口"""
    project = request.args.get('project').strip()
    project_en = request.args.get('project_en').strip()
    domain = request.args.get('domain').strip()
    description = request.args.get('description').strip()
    test_group = session["deptName"]
    startDate = request.args.get("startDate")
    endDate = request.args.get("endDate")
    project_status = request.args.get("project_status")
    if project == "" or domain == "" or description == "" or startDate == "" or endDate =="":
        msg = {"result": "项目名称 or 项目domain or 项目描述 or 日期 不能为空!"}
    else:
        try:
            dept = session.get("deptName")
            if dept == u"其他":
                raise Exception, '当前部门无权限运行接口'
            datas = Project(project=project,domain=domain,project_en=project_en,description=description,test_group=test_group,
                            startDate=startDate+" 00:00:00",endDate=endDate+ " 23:59:59",use_status=int(project_status))
            db.session.add(datas)
            msg = {"status":200,"result":"%s was insert successful!"}
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            msg = {"status": 400,"result":str(e)}
    response = make_response(jsonify(msg)) #返回response
    return response