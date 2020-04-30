#-*-coding:utf-8 -*-
from app.main import views
from flask import render_template,request,make_response,jsonify,session
from app import db
from app.config.api_models import Project, Case_Http_API ,Case_Http_File,Login_Base_Project
from app.config.user_models import User,DeptName
from app.config.public_function import replace_cn
from sqlalchemy import and_,func
import json
@views.route('/addHttpProject',methods=['POST','GET'])
def add_project():
    """增加测试项目"""
    if request.method == 'GET':
        projects = db.session.query(Project.project).all()
        msg = {"datas":projects,"code":200}
    elif request.metho == 'POST':
        projects = request.form['project'].strip()
        descript = request.form['descript'].strip()
        try:
            datas = Project(project=projects,description=descript)
            db.session.add(datas)
            db.session.commit()
            msg = {"datas": "%s was insert successful!" % (projects),"code":200}
        except Exception as e:
            msg = {"datas":str(e),"code":200}
    response = make_response(jsonify(msg))  # 返回response
    return response
@views.route('/httpIndex/<intBool>')
def http_select(intBool):
    """API测试首页"""
    loginProjects_tuple = Login_Base_Project.query.filter_by(status=1).all()    #封装登录提供方法
    loginProjects = [m.project for m in loginProjects_tuple]
    isAdmin = session.get("isAdmin")
    deptNameSession = session.get("deptName")
    if isAdmin:    #判断管理员
        Api_project = Project.query.distinct().all()    #提取所有测试项目,传入页面中
        tester_user = User.query.distinct().all()
        style = ""
        selfApi_project = Api_project
    else:
        if intBool=="1":    #当前项目组查看
            Api_project = Project.query.filter(func.find_in_set(deptNameSession,Project.test_group)
                ).distinct().all()
            dept = DeptName.query.filter(
                    DeptName.deptName==deptNameSession).first()
            tester_user = User.query.filter_by(status=1,deptId=dept.deptId).all()
            style=""
            selfApi_project = Api_project
        else:
            Api_project = Project.query.filter(
                Project.test_group!=deptNameSession).distinct().all()
            dept = DeptName.query.filter(
                DeptName.deptName==deptNameSession).first()
            deptId = dept.deptId
            tester_user = User.query.filter(and_(User.status==1,User.deptId!=deptId)).all()
            style='style=display:none'
            selfApi_project = Project.query.filter(
                Project.test_group==deptNameSession).distinct().all()
    users = [singleUser.userName for singleUser in tester_user]
    return render_template("/api_test/case_http_edit.html",style=style,selfApi_project=selfApi_project,
                           api_project=Api_project, tester=users,intBool=intBool,
                           loginProjects=loginProjects)

@views.route('/httpInsert',methods=['POST'])
def http_insert():
    """增加测试用例步骤接口"""
    project = request.form['project'].strip()
    case_api = request.form['case_api'].strip()
    case_desc = request.form['description'].strip()
    case_host = request.form['case_host'].strip()
    case_url = request.form['case_url'].strip()
    method = request.form['method']
    response = replace_cn(request.form['response'].strip())
    params = replace_cn(request.form["params"].strip())
    headers = replace_cn(request.form["headers"].strip())
    cookies = replace_cn(request.form["cookies"].strip())
    islogin = request.form["islogin"]
    account_project = request.form["account_project"].strip()
    account_username = request.form["account_username"].strip()
    account_passwd = request.form["account_passwd"].strip()
    check_assert = request.form["check_assert"]
    assert_value = request.form['assert_value'].strip()
    tester = session.get("userName")
    test_group = session.get("deptName")
    try:
        if params == "":
            raise Exception,"Params输入项不能为空,默认为None!"
        if headers == "":
            raise Exception,"Headers输入项不能为空,默认为None!"
        if cookies == "":
            raise Exception, "Cookies输入项不能为空,默认为None!"
        if islogin==True and account_project=="None":
            raise Exception, "勾选登录框后,请选择登录项目!"
    except Exception as e:
        resp = {'datas':str(e),'code': '400'}
        return make_response(jsonify(resp))
    try:
        test_env = json.loads(cookies, encoding="utf8")["env_flag"]
    except Exception as e:
        resp = {'datas': '请检查cookies项(非json格式)\nPS:\n{"env_flag":"","env_num":""}', 'code': '400'}
        return make_response(jsonify(resp))
    if islogin == "true":
        islogin = 1
    else:
        islogin = 0
    if check_assert == "true":
        check_assert = 1
    else:
        check_assert = 0
    try:
        datas = Case_Http_API(project=project, case_api=case_api,
                              description=case_desc, case_host=case_host,
                              case_url=case_url,method=method,params=params,
                              response=response,headers=headers,cookies=cookies,
                              isLogin=islogin,account_project=account_project,
                              account_username=account_username,
                              account_passwd=account_passwd,test_env=test_env,
                              test_group=test_group,tester=tester,
                              isSchedule=check_assert,checkAssert=assert_value
                              )
        db.session.add(datas)
        db.session.commit()
        msg = {"datas":"%s 创建成功!"%(case_api),"code":200}
    except Exception as e:
        db.session.rollback()
        msg = {"code":400,"datas":str(e)}
    response = make_response(jsonify(msg)) #返回response
    return response
@views.route('/httpSearch',methods=['GET'])
def httpSearch():
    """接口提供返回测试步骤"""
    isAdmin = session.get("isAdmin")
    dept = session.get("deptName")
    case_name = request.args.get('case_name')  if request.args.get('case_name') else 'None'   #接口名称
    case_url_name = request.args.get('case_url_name')  if request.args.get('case_url_name')  else 'None'  #接口链接
    project = request.args.get('project')    #测试业务项目
    state = request.args.get("state")    #测试接口状态
    test_env = request.args.get("test_env")    #测试接口环境
    tester = request.args.get("test_group")    #所属测试人员
    test_project = request.args.get("test_project")    #发布项目包
    page = request.args.get("curPageApi") if request.args.get("curPageApi") else 1   #当前展示页
    isSelfGroup = request.args.get("isSelfGroup")
    pageDisplayCount = request.args.get("pageDisplayCount")    #展示行数
    curPage = int(page) if page else 1
    curPageDisplayCount = int(pageDisplayCount) if pageDisplayCount else 10
    dict_filter = {
        "project":project,
        "status":state,
        "test_env":test_env,
        "tester":tester
    }
    if isAdmin:
        filters = {}
        for key,value in dict_filter.items():    #筛选参数值＝None的数据
            if value!=None and str(value).upper()!="NONE":
                filters[key] = value
        api_datas = Case_Http_API.query.filter_by(**filters)
    else:
        if isSelfGroup == u"测试项目_1":
            filters = {"test_group":dept}
            for key, value in dict_filter.items():  # 筛选参数值＝None的数据
                if value != None and str(value).upper() != "NONE":
                    filters[key] = value
            api_datas = Case_Http_API.query.filter_by(**filters)
        else:
            filters = {}
            for key, value in dict_filter.items():  # 筛选参数值＝None的数据
                if value != None and str(value).upper() != "NONE":
                    filters[key] = value
            api_datas = Case_Http_API.query.filter_by(**filters).filter(Case_Http_API.test_group!=dept)
    if str(case_url_name).upper() != "NONE" and str(case_name).upper() == "NONE":
        datas = api_datas.filter(Case_Http_API.case_url.like("%"+case_url_name+"%")).order_by(Case_Http_API.id.desc()).paginate(curPage,curPageDisplayCount,False)
    elif str(case_url_name).upper() == "NONE" and str(case_name).upper() == "NONE":
        datas = api_datas.order_by(Case_Http_API.id.desc()).paginate(curPage,curPageDisplayCount,False)
    elif str(case_url_name).upper() == "NONE" and str(case_name).upper() != "NONE":
        datas = api_datas.filter(Case_Http_API.case_api.like("%"+case_name+"%")).order_by(Case_Http_API.id.desc()).paginate(curPage, curPageDisplayCount, False)
    else:
        datas = api_datas.filter(Case_Http_API.case_url.like("%"+case_url_name+"%")).filter(
            Case_Http_API.case_api.like("%" + case_name + "%")
        ).order_by(Case_Http_API.id.desc()).paginate(curPage, curPageDisplayCount, False)
    searchDatas = []
    for data in datas.items:
        temp_datas = []
        temp_datas.append(data.id)
        temp_datas.append(data.project)
        temp_datas.append(data.case_api)
        temp_datas.append(data.description)
        temp_datas.append(data.case_url)
        temp_datas.append(data.status)
        temp_datas.append(data.params)
        temp_datas.append(data.method)
        searchDatas.append(temp_datas)
    resp = {"code": 200, "datas": searchDatas,
            "total":datas.total,"curPage":curPage,"pages":datas.pages,
            "has_next":datas.has_next,"has_prev":datas.has_prev}
    msg_resp = make_response(jsonify(resp))
    return msg_resp
@views.route('/httpUpdate',methods=['GET','POST'])
def httpUpdate():
    """用例更新操作接口"""
    pid = request.form['pid'].strip()
    project = request.form['project'].strip()
    case_api = request.form['case_api'].strip()
    description = request.form['description'].strip()
    case_host = request.form['case_host'].strip()
    case_url = request.form['case_url'].strip()
    method = request.form['method']
    params = replace_cn(request.form['params'].strip())
    response = replace_cn(request.form['response'].strip())
    headers = replace_cn(request.form['headers'].strip())
    cookies = replace_cn(request.form['cookies'].strip())
    islogin = request.form["islogin"]
    account_project = request.form["account_project"].strip()
    account_username = request.form["account_username"].strip()
    account_passwd = request.form["account_passwd"].strip()
    check_assert = request.form["check_assert"]
    assert_value = request.form['assert_value']
    tester = session.get("userName")
    test_group = session.get("deptName")
    isAdmin = session.get("isAdmin")
    try:
        if params == "":
            raise Exception,"Params输入项不能为空,默认为None!"
        if headers == "":
            raise Exception,"Headers输入项不能为空,默认为None!"
        if cookies == "":
            raise Exception, "Cookies输入项不能为空,默认为None!"
        if islogin=='true' and account_project=="None":
            raise Exception, "勾选登录框后,请选择登录项目!"
    except Exception as e:
        resp = {'datas':str(e),'code': '400'}
        return make_response(jsonify(resp))
    try:
        test_env = json.loads(cookies, encoding="utf8")["env_flag"]
    except Exception as e:
        resp = {'datas': '请检查cookies项(非json格式)\nPS:\n{"env_flag":"","env_num":""}', 'code': '400'}
        return make_response(jsonify(resp))
    if islogin =="true":
        islogin = 1
    else:
        islogin = 0
    if check_assert =="true":
        check_assert = 1
    else:
        check_assert = 0
    cha_datas = Case_Http_API.query.filter_by(id=pid).first()
    if cha_datas.tester != tester and isAdmin==False:
        resp = {'datas': '更新失败,当前登录人员非接口创建人员!', 'code': '400'}
    else:
        try:
            if isAdmin==False:
                datas = Case_Http_API.query.filter_by(id=pid).update(dict(
                    project=project,case_api=case_api,description=description,
                    case_host=case_host,case_url=case_url,method=method,
                    params=params,response=response,headers=headers,cookies=cookies,
                    isLogin=islogin,account_project=account_project,
                    account_username=account_username,account_passwd=account_passwd,
                    tester=tester,test_group=test_group,test_env=test_env,
                    isSchedule=check_assert,checkAssert=assert_value
                ))
            else:
                datas = Case_Http_API.query.filter_by(id=pid).update(dict(
                    project=project, case_api=case_api, description=description,
                    case_host=case_host, case_url=case_url, method=method,
                    params=params, response=response, headers=headers, cookies=cookies,
                    isLogin=islogin, account_project=account_project,
                    account_username=account_username, account_passwd=account_passwd,
                    test_env=test_env,
                    isSchedule=check_assert, checkAssert=assert_value
                ))

            db.session.commit()
            resp = {'datas': '更新成功', 'code': '200'}
        except Exception as e:
            db.session.rollback()
            resp = {'datas': str(e), 'code': '400'}
    return make_response(jsonify(resp))
@views.route('/httpStatus',methods=["GET"])
def httpStatus():
    """更改测试接口状态"""
    pid = request.args.get("pid")
    status = request.args.get("status")
    tester = session.get("userName")
    isAdmin = session.get("isAdmin")
    cha_datas = Case_Http_API.query.filter_by(id=pid).first()
    if cha_datas.tester != tester and isAdmin==False:
        resp = {'datas': '更新失败,当前登录人员非接口创建人员!', 'code': '400'}
    else:
        try:
            Case_Http_API.query.filter_by(id=pid).update(dict(status=int(status)))
            db.session.commit()
            resp = {'datas': '更新成功', 'code': '200'}
        except Exception as e:
            db.session.rollback()
            print str(e)
            resp = {"code": 400, "datas": str(e)}
    return make_response(jsonify(resp))
@views.route('/httpDelete',methods=["GET"])
def httpDelete():
    """删除测试接口"""
    pid = request.args.get("pid")
    project = request.args.get('project').strip()
    case_api = request.args.get('case_api').strip()
    tester = session.get("userName")
    isAdmin = session.get("isAdmin")
    cha_datas = Case_Http_API.query.filter_by(id=pid).first()
    if cha_datas.tester != tester and isAdmin==False:
        resp = {'datas': '删除失败,当前登录人员非接口创建人员!', 'code': '400'}
    else:
        try:
            delete_datas = Case_Http_API.query.filter(Case_Http_API.id==pid,Case_Http_API.project==project,
                                       Case_Http_API.case_api==case_api).first()
            db.session.delete(delete_datas)
            db.session.commit()
            resp = {'datas': '删除成功', 'code': '200'}
        except Exception as e:
            db.session.rollback()
            print str(e)
            resp = {"code": 400, "datas": str(e)}
    return make_response(jsonify(resp))
@views.route('/httpCopy',methods=["GET"])
def httpCopy():
    pid = request.args.get("pid")
    case_api = request.args.get("case_api").strip()
    copy_project_choice = request.args.get("copy_project_choice").strip()
    copy_test_env = request.args.get("copy_test_env").strip()
    tester = session.get("userName")
    test_group = session.get("deptName")
    copy_datas = Case_Http_API.query.filter(Case_Http_API.id==pid,Case_Http_API.case_api==case_api).first()
    new_cookies = u'{"env_flag":"%s","env_num":"1"}'%(copy_test_env)
    cookies = new_cookies
    try:
        datas = Case_Http_API(project=copy_project_choice,
                              case_api=copy_datas.case_api,
                              description=copy_datas.description,
                              case_url=copy_datas.case_url,
                              method=copy_datas.method,
                              response=copy_datas.response,
                              status=copy_datas.status,
                              params=copy_datas.params,
                              case_host=copy_datas.case_host,
                              headers=copy_datas.headers,
                              cookies=cookies,
                              isLogin=copy_datas.isLogin,
                              test_env=copy_test_env,
                              test_group=test_group,
                              tester=tester,
                              account_project=copy_datas.account_project,
                              account_username=copy_datas.account_username,
                              account_passwd=copy_datas.account_passwd,
                              checkAssert=copy_datas.checkAssert,
                              isSchedule=copy_datas.isSchedule )
        db.session.add(datas)
        db.session.commit()
        resp = {'datas': '复制成功', 'code': '200'}
    except Exception as e:
        db.session.rollback()
        print str(e)
        resp = {"code": 400, "datas": str(e)}
    return make_response(jsonify(resp))

@views.route("/searchHttpSchedule",methods=['GET'])
def searchHttpSchedule():
    """查询集成调度参数"""
    pid = request.args.get("api_pid")
    case_api = request.args.get("case_api")
    schedule_datas = Case_Http_Schedule.query.filter(Case_Http_Schedule.api_id==pid).filter(Case_Http_Schedule.case_api==case_api).first()
    if schedule_datas:
        resp_msg={"code":"200","count":"1","data":{"status":schedule_datas.status,"assertValue":schedule_datas.assertValue,"params":schedule_datas.params}}
    else:
        resp_msg={"code":"200","count":"0","data":{}}
    return make_response(jsonify(resp_msg))
@views.route("/saveHttpSchedule",methods=["GET"])
def saveHttpSchedule():
    """保存集成调度参数"""
    pid = request.args.get("api_pid")
    case_api = request.args.get("case_api")
    params = request.args.get("params")
    status = request.args.get("status")
    assertValue = request.args.get("assertValue")
    schedule_datas = Case_Http_Schedule.query.filter(Case_Http_Schedule.api_id == pid).filter(
        Case_Http_Schedule.case_api == case_api).first()
    if not schedule_datas:
        try:
            datas = Case_Http_Schedule(api_id=pid,case_api=case_api,params=params,assertValue=assertValue,status=status)
            db.session.add(datas)
            db.session.commit()
            resp_msg = {"datas": "%s 更新成功!" % (case_api), "code": 200}
        except Exception as e:
            db.session.rollback()
            resp_msg = {"code": 400, "datas": str(e)}
    else:    #修改数据
        try:
            Case_Http_Schedule.query.filter_by(api_id=pid).update(dict(status=status,
                                                                   api_id=pid,
                                                                   params=params,
                                                                   assertValue=assertValue
                                                               ))
            db.session.commit()
            resp_msg = {"datas": "%s 更新成功!" % (case_api), "code": 200}
        except Exception as e:
            db.session.rollback()
            resp_msg = {"code": 400, "datas": str(e)}
    return make_response(jsonify(resp_msg))
@views.route('/httpCondition')
def case_condition():
    """加载接口名称，操作接口名称配置"""
    project = request.args.get('project')
    object_api = db.session.query(Case_Http_API.case_api).filter_by(project=project).all()
    dict_resp = {"code": 200, "datas":object_api}
    resp = make_response(jsonify(dict_resp))
    return resp

@views.route("/httpUnionSearch",methods=['GET'])
def httpUnionSearch():
    project = request.args.get('project')
    case_api = request.args.get('case_api')
    pid = request.args.get('pid')
    object_api = db.session.query(Case_Http_API.project,
                                  Case_Http_API.case_api,
                                  Case_Http_API.description,
                                  Case_Http_API.case_host,
                                  Case_Http_API.case_url,
                                  Case_Http_API.method,
                                  Case_Http_API.response,
                                  Case_Http_API.params,
                                  Case_Http_API.headers,
                                  Case_Http_API.cookies,
                                  Case_Http_API.isLogin,
                                  Case_Http_API.account_project,
                                  Case_Http_API.account_username,
                                  Case_Http_API.account_passwd,
                                  Case_Http_API.isSchedule,
                                  Case_Http_API.checkAssert
                                  ).filter_by(project=project,case_api=case_api,id=pid).first()
    resp = {"code": 200, "datas": object_api}
    msg_resp = make_response(jsonify(resp))
    return msg_resp

@views.route("/save_upload_data",methods=["POST"])
def save_upload_data():
    file_1 = request.files['file']
    file_desc = request.form["file_desc"]
    filename = file_1.filename
    content_type = file_1.mimetype
    targetId = request.form["targetId"]  #获取case_api　数据库id值,如接口新建则为999999999
    if targetId=="999999999":  #新建数据
        project = request.form["project"]
        case_api = request.form["case_api"]
        case_desc = request.form["case_desc"]
        case_host = request.form["case_host"]
        case_url = request.form["case_url"]
        method = request.form["method"]
        try:
            targetId = db.session.query(Case_Http_API.id).filter_by(project=project,case_api=case_api,
                                                                description=case_desc,case_host=case_host,
                                                                    case_url=case_url,method=method).first()
            datas = Case_Http_File(case_api_id=str(targetId[0]),file_desc=file_desc,
                                   file_name=filename,content_type=content_type)
            targetId = targetId[0]
            db.session.add(datas)
            db.session.commit()
            resp = {"datas": "%s 更新成功!" % (case_api), "code": 200}
        except Exception as e:
            db.session.rollback()
            resp = {"code": 400, "datas": str(e)}
    else:  #修改数据
        try:
            datas = Case_Http_File.query.filter_by(case_api_id=targetId).update(dict(
                file_desc=file_desc,file_name=filename,content_type=content_type))
            if datas:
                db.session.commit()
                resp = {'datas': '更新成功', 'code': '200'}
            else:  #新增数据
                project = request.form["project"]
                case_api = request.form["case_api"]
                case_desc = request.form["case_desc"]
                case_host = request.form["case_host"]
                case_url = request.form["case_url"]
                method = request.form["method"]
                targetId = db.session.query(Case_Http_API.id).filter_by(project=project, case_api=case_api,
                                                                        description=case_desc, case_host=case_host,
                                                                        case_url=case_url, method=method,
                                                                        id=targetId).first()
                datas = Case_Http_File(case_api_id=targetId[0], file_desc=file_desc,
                                       file_name=filename, content_type=content_type)
                targetId = targetId[0]
                db.session.add(datas)
                db.session.commit()
                resp = {"datas": "%s 更新成功!" % (case_api), "code": 200}
        except Exception as e:
            db.session.rollback()
            resp = {'datas': str(e), 'code': '400'}
    try:
        file_1.save("./app/upload_file/%s_%s" % (str(targetId),filename))
    except Exception as e:
        resp = {'datas': str(e), 'code': '401'}
    return make_response(jsonify(resp))

