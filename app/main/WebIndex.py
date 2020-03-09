#!/usr/bin/python
#-*-coding:utf-8 -*-
from __future__ import division
from app.main import views
from flask import render_template,request,make_response,jsonify,session
from app import db,redis
from app.config.user_models import User,Manager,DeptName,Message
from flask_login import login_required
from sqlalchemy import func,and_
import base64
import json
from urllib import unquote
import datetime
from app.config.api_models import Project,\
    Case_Http_API,Web_Model_Set,Test_User_Reg,Key_Value,Run_Suite,Test_Report
@views.route("/webIndex",methods=["GET"])
@login_required
def webIndex():
    """WEB首页"""
    userName = session.get("userName")
    userId = session.get("userId")
    deptName = session.get("deptName")
    isAdmin = session.get("isAdmin")
    if isAdmin:    #是否管理员
        modelNameLink_caidan = Web_Model_Set.query.filter(Web_Model_Set.modelStatus==1
                                                   ).filter(Web_Model_Set.levelName=="菜单管理").all()
        modelNameLink_neirong = Web_Model_Set.query.filter(Web_Model_Set.modelStatus==1
                                                   ).filter(Web_Model_Set.levelName=="内容管理").all()
        projectCount = db.session.query(Project.id).count()    #统计所有项目
        deptInterfaceCount = db.session.query(Case_Http_API.id).count()    #统计所有接口数据
        groupsApi = ["%s" % (deptName)]
        imgUrl = "static/userImg/admin.jpg"
        msgCount = Message.query.filter(Message.toUser=="admin").filter(Message.status==0).count()
        return render_template('home/index.html', modelNameLink_caidan=modelNameLink_caidan,
                               project_cout=projectCount,modelNameLink_neirong=modelNameLink_neirong,
                           userName=userName,deptName=deptName,groupsApi=groupsApi,msgCount=msgCount,
                               userinterfaceCount=deptInterfaceCount,userImg=imgUrl,
                               interfaceCount=deptInterfaceCount)
    else:
        modelNameLink_caidan = Web_Model_Set.query.filter(Web_Model_Set.modelStatus == 1
                                                          ).filter(Web_Model_Set.levelName == "菜单管理"
                                                                   ).filter(Web_Model_Set.isAdmin==0).all()
        modelNameLink_neirong = Web_Model_Set.query.filter(Web_Model_Set.modelStatus == 1
                                                           ).filter(Web_Model_Set.levelName == "内容管理"
                                                                    ).filter(Web_Model_Set.isAdmin==0).all()
        groupsApi = ["%s"%(deptName),"非%s"% (deptName)]    #定义　部门查询模块　&　非本部门查询模块
        projectCount = db.session.query(Project.id).filter_by(test_group=deptName).count()   #用户部门项目统计
        deptInterfaceCount = db.session.query(Case_Http_API.id
                                              ).filter_by(test_group=deptName).count()    #用户部门接口统计
        userInterfaceCount = db.session.query(Case_Http_API.id
                                              ).filter_by(test_group=deptName,
                                                          tester=userName).count()    #用户接口统计
        userImg = User.query.filter(User.userName==userName
                                    ).filter(User.userId==userId).first()
        if not userImg.imgUrl:
            imgUrl ="static/userImg/default.jpg"
        else:
            imgUrl = userImg.imgUrl
        msgCount = Message.query.filter(Message.toUser==userName).filter(Message.status!=3).count()
        return render_template('home/index.html', modelNameLink_caidan=modelNameLink_caidan,
                               project_cout=projectCount,msgCount=msgCount,modelNameLink_neirong=modelNameLink_neirong,
                               userinterfaceCount=userInterfaceCount,interfaceCount=deptInterfaceCount,
                               userName=userName, deptName=deptName,groupsApi=groupsApi,userImg=imgUrl)
@views.route("/homeIndex",methods=["GET"])
@login_required
def homeIndex():
    startDate = datetime.datetime.now().strftime('%Y-%m-%d')
    endDate = datetime.datetime.now().strftime('%Y-%m-%d')
    return render_template('home/homeIndex.html',startDate=startDate,endDate=endDate)
@views.route("/index",methods=["GET"])
@login_required
def index():
    return render_template('home/homeIndex.html')
@views.route("/pageIndex",methods=["GET"])
@login_required
def pageIndex():
    return render_template('home/pageIndex.html')
@views.route("/message",methods=["GET"])
def messageIndex():
    # urlName = "static/userImg/"+userName+".png"
    isAdmin = session.get("isAdmin")
    if isAdmin:
        tester_user = User.query.distinct().all()
        users = [singleUser.userName for singleUser in tester_user]
        return render_template("home/message.html",tester=users,isAdmin=isAdmin)
    else:
        userName = session.get("userName")
        return render_template("home/message.html",tester=userName,isAdmin=isAdmin)
@views.route("/msgSearch",methods=['GET'])
def msgSearch():
    msg_tester = request.args.get("msg_tester")
    msg_review = request.args.get("msg_review")
    page = request.args.get("curPageIndex") if request.args.get("curPageIndex") else 1   #当前展示页
    curPage = int(page) if page else 1
    isAdmin = session.get("isAdmin")
    userName = session.get("userName")
    pageDisplayCount = request.args.get("pageDisplayCount")  # 展示行数
    curPageDisplayCount = int(pageDisplayCount) if pageDisplayCount else 10
    if isAdmin:
        if msg_tester=="None" and msg_review=="None":
            messageDatas = Message.query.paginate(curPage, curPageDisplayCount, False)
        elif  msg_tester!="None" and msg_review=="None":
            messageDatas = Message.query.filter(Message.fromUser==msg_tester
                                                ).filter(Message.toUser==userName
                                                         ).paginate(curPage, curPageDisplayCount, False)
        elif  msg_tester=="None" and msg_review!="None":
            messageDatas = Message.query.filter(Message.status == msg_review
                                                ).paginate(curPage, curPageDisplayCount, False)
        else:
            messageDatas = Message.query.filter(Message.status==msg_review
                                                ).filter(Message.toUser==msg_tester
                                                         ).filter(Message.toUser==userName
                                                         ).paginate(curPage, curPageDisplayCount, False)
    else:
        if msg_tester == "None" and msg_review == "None":
            messageDatas = Message.query.filter(Message.toUser==userName).filter(Message.status!=3).paginate(curPage, curPageDisplayCount, False)
        elif msg_tester != "None" and msg_review == "None":
            messageDatas = Message.query.filter(Message.toUser==userName).filter(Message.toUser == msg_tester
                                                ).filter(Message.status!=3).paginate(curPage, curPageDisplayCount, False)
        elif msg_tester == "None" and msg_review != "None":
            messageDatas = Message.query.filter(Message.toUser==userName).filter(Message.status == msg_review
                                                ).paginate(curPage, curPageDisplayCount, False)
        else:
            messageDatas = Message.query.filter(Message.toUser==userName).filter(Message.status == msg_review
                                                ).filter(Message.fromUser == msg_tester
                                                         ).paginate(curPage, curPageDisplayCount, False)
    searchDatas = []
    for data in messageDatas.items:
        temp_datas = []
        temp_datas.append(data.id)
        temp_datas.append(data.createDate)
        temp_datas.append(data.fromUser)
        temp_datas.append(data.msg)
        temp_datas.append(data.status)
        temp_datas.append(isAdmin)
        searchDatas.append(temp_datas)
    resp = {"code": 200, "datas": searchDatas,
            "total": messageDatas.total, "curPage": curPage, "pages": messageDatas.pages,
            "has_next": messageDatas.has_next, "has_prev": messageDatas.has_prev}
    msg_resp = make_response(jsonify(resp))
    return msg_resp
@views.route("/msgReviews",methods=["GET"])
def msgReviews():
    pid = request.args.get("pid")
    isAdmin = session.get("isAdmin")
    userName = session.get("userName")
    if isAdmin:
        messageDatas = Message.query.filter(Message.id == pid).first()          #查询消息id
        if messageDatas.func == "uploadDept":        #来源方法等于上传
            try:
                params = json.loads(messageDatas.params)     #取出更新数据
                dept = DeptName.query.filter(DeptName.deptName == params['updateDept']).first()    #查询更新部门数据
                userData = User.query.filter(User.userId ==
                                         messageDatas.userId).filter(User.userName == messageDatas.fromUser)     #查询用户数据
                updateUser = userData.update(dict(deptId=dept.deptId, imgUrl=params['urlName']))    #更新用户部门Id 和头像链接
                messageDatas.status = 1   #审批状态更改为已审核
                msg = "已同意%s更换至:%s"%(messageDatas.fromUser,params['updateDept'])
                wc = Message.query.filter(Message.id==pid).update(dict(fromUser=userName,toUser=userData.first().userName,msg=msg))
                db.session.commit()
                resp = {'datas': "更新成功", 'code': '200'}
            except Exception as e:
                db.session.rollback()
                resp = {'datas': str(e), 'code': '400'}
        else:
            msg = "暂未开通其他功能"
            resp = {'datas': msg, 'code': '200'}
    else:
        msg = "当前用户非管理员!不可操作"
        resp = {'datas': msg, 'code': '400'}
    return make_response(jsonify(resp))
@views.route("/msgReject",methods=["GET"])
def msgReject():
    pid = request.args.get("pid")
    isAdmin = session.get("isAdmin")
    userName = session.get("userName")
    if isAdmin:
        messageDatas = Message.query.filter(Message.id == pid).first()  # 查询消息id
        if messageDatas.func == "uploadDept":  # 来源方法等于上传
            try:
                params = json.loads(messageDatas.params)  # 取出更新数据
                userData = User.query.filter(User.userId ==
                                             messageDatas.userId).filter(
                    User.userName == messageDatas.fromUser)  # 查询用户数据
                messageDatas.status = 2  # 审批状态更改为已审核
                msg = "已拒绝%s更换至:%s"%(messageDatas.fromUser,params['updateDept'])
                wc = Message.query.filter(Message.id == pid).update(
                    dict(fromUser=userName, toUser=userData.first().userName, msg=msg))
                db.session.commit()
                resp = {'datas': "更新成功", 'code': '200'}
            except Exception as e:
                db.session.rollback()
                resp = {'datas': str(e), 'code': '400'}
        else:
            msg = "暂未开通其他功能"
            resp = {'datas': msg, 'code': '200'}
    else:
        msg = "当前用户非管理员!不可操作"
        resp = {'datas': msg, 'code': '400'}
    return make_response(jsonify(resp))
@views.route("/msgRead",methods=["GET"])
def msgRead():
    pid = request.args.get("pid")
    try:
        datas = Message.query.filter(Message.id == pid).update(
            dict(status=3))
        db.session.commit()
        resp = {'datas': "更新成功", 'code': '200'}
    except Exception as e:
        db.session.rollback()
        resp = {'datas': str(e), 'code': '400'}
    return make_response(jsonify(resp))
@views.route("/userInfo",methods=["GET"])
def userInfo():
    userName = session.get("userName")
    userId = session.get("userId")
    isAdmin = session.get("isAdmin")
    if isAdmin:
        datas = Manager.query.filter(Manager.userName==userName).first()
        return render_template('home/userInfo.html',userDatas=datas,depts="管理员")
    else:
        datas = User.query.filter(User.userId==userId).filter(User.userName==userName).first()
        depts = DeptName.query.distinct().all()
        return render_template('home/userInfo.html',userDatas=datas,depts=depts)
@views.route("/uploadDept",methods=['POST'])
def uploadDept():
    userName = session.get("userName")
    userId = session.get("userId")
    nowDept = session.get("deptName")
    updateDept = request.form.get("deptName")
    urlName = "static/userImg/"+userName+".png"

    try:
        msg = "用户:%s申请修改部门: %s --> %s"%(userName,nowDept,updateDept)
        params = {"nowDept":nowDept,"updateDept":updateDept,"urlName":urlName}
        datas = Message(createDate=None,userId=userId
                        ,fromUser=userName,toUser="admin",msg=msg,
                        params=json.dumps(params,encoding="utf8",ensure_ascii=False),
                        func="uploadDept")
        db.session.add(datas)
        db.session.commit()
        resp = {'msg': '已申请!待管理员审批后更新!', 'code': '200'}
    except Exception as e:
        db.session.rollback()
        resp = {'msg': str(e), 'code': '400'}
    return make_response(jsonify(resp))
@views.route('/uploadImg', methods=['POST'])
def uploadImg():
    userName = session.get("userName")
    imgStr = request.get_data()
    imgName = "app/static/userImg/"+userName+".png"
    with open(imgName, "wb") as f:
        try:
            img = json.loads(imgStr)
            f.write(base64.b64decode(img['uploadImg']))
            resp = {'msg': '已申请!待管理员审批后更新!', 'code': '200'}
        except Exception as e:
            resp = {'nsg': str(e), 'code': '400'}
    return make_response(jsonify(resp))
@views.route("/testIndex",methods=["GET"])
@login_required
def testIndex():
    return render_template('/api_test/test_phones.html')
@views.route('/run_api_index', methods=['GET', 'POST'])
@login_required
def run_api_index():
    api_project = Project.query.with_entities(Project.project).distinct().all()
    return render_template('/api_test/run_api_index.html',projects=api_project)
@views.route("/query_phones",methods=["GET"])
@login_required
def test_query():
    """Test_Phones"""
    query_phone = request.args.get("PHONE")
    env = request.args.get("ENV")
    if query_phone == "None":
        query_phone = eval(query_phone)
    if env == "None":
        env = eval(env)
    try:
        if query_phone and env == None:
            test_phones = db.session.query(Test_User_Reg.id,Test_User_Reg.phone,Test_User_Reg.type,
                                       Test_User_Reg.env,Test_User_Reg.description).filter(
                Test_User_Reg.phone.like(query_phone+"%")).all()
        elif query_phone and env:
            test_phones = db.session.query(Test_User_Reg.id,Test_User_Reg.phone, Test_User_Reg.type,
                                           Test_User_Reg.env, Test_User_Reg.description).filter(
                Test_User_Reg.phone.like(query_phone + "%")).filter_by(env=env).all()
        elif query_phone ==None and env:
            test_phones = db.session.query(Test_User_Reg.id,Test_User_Reg.phone, Test_User_Reg.type,
                                           Test_User_Reg.env, Test_User_Reg.description).filter_by(env=env).all()
        elif query_phone == None and env ==None:
            test_phones = db.session.query(Test_User_Reg.id,Test_User_Reg.phone, Test_User_Reg.type,
                                           Test_User_Reg.env, Test_User_Reg.description).all()
        s =map(wc,[telephone for telephone in test_phones])
        msg = {"code":200,"msg":"查询成功","data":s}
    except Exception as e:
        msg = {"code":200,"msg":str(e),"data":"[]"}
    return make_response(jsonify(msg))
def wc(x):
    dictA = {}
    dictA["id"] = x[0]
    dictA["phone"] = x[1]
    dictA["type"] = x[2]
    dictA["env"] = x[3]
    dictA["desc"] = x[4]
    return dictA
@views.route("/query_phone",methods=["GET"])
def query_id():
    """Test_Phones"""
    pid = request.args.get("pid")
    test_phones = db.session.query(Test_User_Reg.id,Test_User_Reg.phone, Test_User_Reg.type,
                                           Test_User_Reg.env, Test_User_Reg.description).filter_by(id=pid).first()
    msg = {"code":200,"msg":"查询成功","data":test_phones[0]}
    return make_response(jsonify(msg))
@views.route("/update_phone",methods=["GET"])
def update_phone():
    """Test_Phones"""
    pid = request.args.get("pid")
    phone = request.args.get("phone")
    env = request.args.get("env")
    type = request.args.get("type")
    desc = request.args.get("desc")
    try:
        dept = session.get("deptName")
        if dept == u"其他":
            raise Exception, '当前部门无权限运行接口'
        if env not in ["beta", "stage,prod"]:
            raise Exception, "操作环境不存在"
        if len(phone) != 11:
            raise Exception, "手机号需等于11位"
        if type < 0 and type > 6:
            raise Exception, "账号类型说明超出范围"
        if pid =="":
            datas = db.session.query(Test_User_Reg.id).filter_by(phone=phone,type=type,env=env).count()
            if datas != 0:
                raise Exception,"手机号已存在"
            else:
                datas = Test_User_Reg(phone=phone,env=env,type=type,description=desc)
                db.session.add(datas)
        else:
            Test_User_Reg.query.filter_by(id=pid).update(dict(phone=phone,type=type,description=desc,env=env))
        db.session.commit()
        resp = {'datas': '更新成功', 'code': '200'}
    except Exception as e:
        db.session.rollback()
        resp = {'datas': str(e), 'code': '400'}
    return make_response(jsonify(resp))
@views.route("/get_redis_key",methods=["GET"])
def get_redis_key():
    redis_key = db.session.query(Key_Value.user_key).filter_by(status=1).all()
    s = ",".join([key[0] for key in redis_key])
    return s
@views.route("/set_key_value",methods=["GET"])
def set_key_value():
    key = request.args.get("key")
    value = request.args.get("value")
    try:
        if key.upper()=="NONE" or key==None:
            raise Exception,"Key不能为空！"
        redis.set(key,value)
        msg = "set success!"
    except Exception as e:
        print str(e)
        msg = str(e)
    return jsonify({"code":"200","msg":msg})


# 资源排行榜数据
@views.route('/dataResource', methods=['GET'])
def dataResource():
    # res = {"plan": 81, "doing": 4, "done": 3, "delay": 16}
    userApiCout = db.session.query(Case_Http_API.tester,func.count(Case_Http_API.id)
                                      ).filter(Case_Http_API.tester!="admin").group_by(Case_Http_API.tester).order_by(func.count(Case_Http_API.id).desc()).all()
    userImgUrl = db.session.query(User.userName,User.imgUrl).all()
    userDatas = []
    userImgs = {}
    orderByCount = []
    for user,apiCount in userApiCout:
        userDatas.append([user,apiCount])
    for user,img in userImgUrl:
        userImgs[user] = img
    for user in userDatas:
        orderByCount.append([user[0],user[1],userImgs[user[0]]])
    resp = {"code":200,"orderByCount":orderByCount}
    return make_response(jsonify(resp))

# 项目统计
@views.route("/dataTofu",methods=["GET"])
def dataTofu():
    userName = session.get("userName")
    projectCount = Project.query.filter(Project.use_status==0).count()  # 统计所有项目
    apiCount = Case_Http_API.query.filter().count()  # 统计所有接口数据
    flowCount = Run_Suite.query.filter(Run_Suite.statu==1).count()
    apiSelfCount = Case_Http_API.query.filter(Case_Http_API.tester==userName).count()  # 统计所有接口数据
    resp = '{"ProjectCount":' + str(projectCount) + ',"JobCount":' + str(apiCount) + ',"JobAllplan":' + str(flowCount) + ',"JobResCount":' + str(apiSelfCount) + '}'
    return resp
# 环形数据
@views.route('/dataRing', methods=['GET', 'POST'])
def dataRing():
    allCount = Project.query.count()
    date = datetime.datetime.now().strftime('%Y-%m-%d 12:00:00')
    doingCount = Project.query.filter(Project.use_status==1).filter(
        and_(Project.endDate>=date)).count()    #进行项目
    delayCount = Project.query.filter(Project.use_status==1).filter(
        and_(Project.endDate<=date)).count()    #延期项目
    planCount = Project.query.filter(Project.use_status==1).filter(
        and_(Project.startDate>=date)).count()    #未开始项目
    overCount = Project.query.filter(Project.use_status==0).count()    #已完成项目

    doingDataCount = "%.2f" % (doingCount/allCount * 100)
    delayDataCount = "%.2f" % (delayCount/allCount * 100)
    overDataCount = "%.2f" % (overCount/allCount * 100)
    planDataCount = "%.2f" % (planCount/allCount * 100)
    resp = '{"plan":' + planDataCount + ',"doing":' + doingDataCount + ',"done":' + overDataCount + ',"delay":' + delayDataCount + '}'
    return resp
# 任务燃尽图数据
@views.route('/rdj', methods=['GET', 'POST'])
def rdj():
    env = request.args.get("env")
    startDate = request.args.get("startDate")
    endDate = request.args.get("endDate")
    if env == "None" or env == None:
        env= None
    if startDate=="":
        startDate = datetime.datetime.now().strftime('%Y-%m-%d 00:00:00')
    else:
        startDate = startDate + " 00:00:00"
    if endDate=="":
        endDate = datetime.datetime.now().strftime('%Y-%m-%d 23:59:59')
    else:
        endDate = endDate + " 23:59:59"
    if env:
        datas = Test_Report.query.filter(and_(
            Test_Report.createDate.__le__(endDate),
            Test_Report.createDate.__ge__(startDate)
        )).filter(Test_Report.type=="work_flow").filter(Test_Report.cookies.like('%'+env+'%')
                                                        ).all()
    else:
        datas = Test_Report.query.filter(and_(
            Test_Report.createDate.__le__(endDate),
            Test_Report.createDate.__ge__(startDate)
        )).filter(Test_Report.type == "work_flow").all()
    for m in datas:
        print m.id
    d1Datas = []
    d2Datas = []
    for i in range(len(datas)):
        w = i + 1
        #[成功||失败,功能域,创建时间]
        d1Datas.append([w,datas[i].success_count,datas[i].domain,datas[i].createDate])
        d2Datas.append([w,datas[i].fail_count,datas[i].domain,datas[i].createDate])
    res = {"d1":d1Datas,"d2":d2Datas}
    return make_response(jsonify(res))
