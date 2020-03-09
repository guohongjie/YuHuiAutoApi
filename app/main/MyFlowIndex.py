#!/usr/bin/python
#-*-coding:utf-8 -*-
from app.main import flow
from flask import render_template,request,make_response,jsonify,session
from app.config.api_models import Project,Case_Http_API,Run_Suite
from app import db,redis
from sqlalchemy import func
import json,re
from app.config.public_function import isPassParams,outerOrderRect
from app.tasks.tasks import run_suite_api
import requests
@flow.route("/myFlowIndex",methods=["GET"])
def myFlowIndex():
    userName = session.get("userName")
    deptName = session.get("deptName")
    isAdmin = session.get("isAdmin")
    if isAdmin:
        datas = Project.query.distinct().all()
        project_api = [data for data in datas]
        suiteDatas = Run_Suite.query.all()
        return render_template("flow/flow.html",project_api=project_api,suiteDatas=suiteDatas)
    else:
        datas = Project.query.filter(Project.test_group==deptName).distinct().all()
        project_api = [data for data in datas]
        suiteDatas = Run_Suite.query.filter(
            Run_Suite.user == userName).filter(
            Run_Suite.test_group == deptName).all()
        return render_template("flow/flow.html", project_api=project_api, suiteDatas=suiteDatas)
@flow.route("/saveSuiteDatas",methods=["POST"])
def saveSuiteDatas():
    """保存流程数据"""
    userName = session.get("userName").strip()
    deptName = session.get("deptName").strip()
    strSuiteDatas = request.form.get("datas").strip()
    suiteDatas = strSuiteDatas.replace("	",""
                                    ).replace("	",""
                                    ).replace("\t",""
                                    ).replace("\n",""
                                    ).replace("\\t","").replace("\\n","")
    saveUpdate = request.form.get("saveUpdate").strip()
    flowName = request.form.get("flowName").strip()
    if saveUpdate=="1":    #新增
        datas = Run_Suite(user=userName,
                          test_group=deptName,suiteName=flowName,
                          suiteDatas=suiteDatas,modifyCount=0)
        db.session.add(datas)
        db.session.commit()
        resp = {'datas': '新增成功', 'code': '200'}
    else:    #修改
        suiteId = request.form.get("suiteId").strip()
        queryModifyCount = Run_Suite.query.filter_by(id=suiteId).first()
        # new_suite_data = unescape(suiteDatas,queryModifyCount.modifyCount)
        datas = Run_Suite.query.filter_by(id=suiteId
                                          ).update(dict(
            suiteDatas=suiteDatas,modifyCount=queryModifyCount.modifyCount+1))
        db.session.commit()
        resp = {'datas': '更新成功', 'code': '200'}
    return make_response(jsonify(resp))
@flow.route("/getProjectApi",methods=["GET"])
def getProjectApi():
    projectName = request.args.get("projectName").strip()
    curPage = request.args.get("curPage").strip()
    curPageDisplayCount = 10
    datas = Case_Http_API.query.filter(Case_Http_API.project==projectName).order_by(
        Case_Http_API.id.desc()).paginate(int(curPage), curPageDisplayCount, False)
    searchDatas = []
    for data in datas.items:
        temp_datas = []
        temp_datas.append(data.id)
        temp_datas.append(data.case_api)
        temp_datas.append(data.params)
        searchDatas.append(temp_datas)
    resp = {"code": 200, "datas": searchDatas,
            "total": datas.total, "curPage": curPage, "pages": datas.pages,
            "has_next": datas.has_next, "has_prev": datas.has_prev}
    msg_resp = make_response(jsonify(resp))
    return msg_resp
@flow.route("/getSuiteName",methods=["POST"])
def getSuiteName():
    suiteName = request.form.get("suiteName").strip()
    suiteId = request.form.get("suiteId").strip()
    datas = Run_Suite.query.filter(Run_Suite.suiteName==suiteName
                                   ).filter(Run_Suite.id==suiteId).first()
    msg_resp = make_response(datas.suiteDatas)
    return msg_resp
@flow.route("/testSuite",methods=["POST"])
def testSuite():
    """测试所绘制的业务流程图"""
    testURL = r"http://uwsgi.sys.bandubanxie.com/case_http_test"
    # testURL = r"http://127.0.0.1:5000/case_http_test"
    suiteDatas = request.form.get("datas").strip()
    new_suiteDatas = suiteDatas.replace("	",""
                                    ).replace("	",""
                                    ).replace("\t",""
                                    ).replace("\n",""
                                    ).replace("\\t","").replace("\\n","")
    suiteName = request.form.get("suiteName")   #增加来源标签,判断是否测试 None 则为测试来源
    isSuiteOrigin = request.form.get("isSuiteOrigin")
    strSuiteDatas = json.loads(new_suiteDatas,encoding='utf8')
    dictSuiteDatas = json.loads(strSuiteDatas,encoding='utf8')
    orderRect,orderPath = outerOrderRect(dictSuiteDatas)
    resp_msg = []
    api_detail_list = []
    for orderStringId in orderRect:
        if dictSuiteDatas["states"][orderStringId]["type"]=="start" or dictSuiteDatas["states"][orderStringId]["type"]=="end":
            continue
        elif dictSuiteDatas["states"][orderStringId]["type"]=="task":
            params = dictSuiteDatas["states"][orderStringId]["props"]["params"]["value"].strip()
            apiName = dictSuiteDatas["states"][orderStringId]["props"]["text"]["value"].strip()
            apiId = dictSuiteDatas["states"][orderStringId]["props"]["api_id"]["value"].strip()
            case_api = Case_Http_API.query.filter(Case_Http_API.id==int(apiId)
                                                      ).first()
            api_detail_list.append({"id":case_api.id,"name":case_api.case_api,
                                    "desc":case_api.description,"method":case_api.method})
            parseParams = isPassParams(case_api.case_api,params)   #解析参数,判断是否参数传递
            if isSuiteOrigin == "1":    #判断测试来源 1:页面测试按钮
                suite_cookie = case_api.cookies
            elif isSuiteOrigin == "2":    #2:接口调度-传递cookie指向测试环境
                suite_cookie = request.form.get('cookies')
            if "请检查上下文接口参数或检查请求参数化" in parseParams:
                pass_status = "Mistake"
                test_dict = [case_api.case_api, parseParams, "参数错误,请检查上下文接口参数或检查请求参数化!",pass_status]
                resp_msg.append(test_dict)
                break
            else:
                if not suiteName:    #来源=测试按钮
                    newSuiteName = "tester"
                else:
                    newSuiteName = "tester"
                suiteName = newSuiteName+"&&"+ case_api.case_api
                req_datas = {
                        "case_host":case_api.case_host,
                        "case_url":case_api.case_url,
                        "method":case_api.method,
                        "params":parseParams,
                        "headers":case_api.headers,
                        "cookies":suite_cookie,
                        "islogin":case_api.isLogin,
                        "account_project":case_api.account_project,
                        "account_username":case_api.account_username,
                        "account_passwd":case_api.account_passwd,
                        "project_cn":"None",
                        "isSuiteOrigin":isSuiteOrigin,
                        "suiteName": suiteName
                    }
                test_resp = requests.post(url=testURL,data=req_datas)
                if test_resp.status_code == 200:
                    try:
                        json_object = json.loads(test_resp.content,encoding="utf8")
                        if json_object["code"] != 200:
                            pass_status = "Mistake"
                            test_dict = [case_api.case_api,
                                         parseParams,
                                         test_resp.content, pass_status]
                            resp_msg.append(test_dict)
                            break
                        else:
                            if case_api.isSchedule:  # 参加校验
                                assert_list = case_api.checkAssert.split(",")
                                listStatus = []
                                for assert_value in assert_list:
                                    assertResult = bool(re.search(assert_value, json_object['test_datas']))
                                    listStatus.append(assertResult)
                                if False not in listStatus:
                                    pass_status = "Success"
                                    test_dict = [case_api.case_api, parseParams,test_resp.content,pass_status]
                                    resp_msg.append(test_dict)
                                else:
                                    pass_status = "Failure"
                                    test_dict = [case_api.case_api, parseParams, "接口业务请求通过,但返回值校验错误:(校验值为:%s)"%(assert_value)+test_resp.content,pass_status]
                                    resp_msg.append(test_dict)
                                    break
                            else:
                                pass_status = "Success"
                                test_dict = [case_api.case_api, parseParams, test_resp.content, pass_status]
                                resp_msg.append(test_dict)
                    except ValueError,e:
                        pass_status = "Mistake"
                        test_dict = [case_api.case_api, parseParams, "请求错误,请检查接口配置参数!",pass_status]
                        resp_msg.append(test_dict)
                        break
                else:
                    pass_status = "Mistake"
                    test_dict = [case_api.case_api, parseParams, "请求错误,请先进行接口调试!",pass_status]
                    resp_msg.append(test_dict)
                    break
    resp = {"datas":resp_msg,"code":"200","order":orderPath,"api_detail":api_detail_list}
    return make_response(jsonify(resp))
@flow.route("/deleteSuite",methods=["GET"])
def deleteSuite():
    suiteId = request.args.get("suiteId")
    delete_datas = Run_Suite.query.filter(Run_Suite.id == int(suiteId)).first()
    db.session.delete(delete_datas)
    db.session.commit()
    resp = {'datas': '删除成功', 'code': '200'}
    return make_response(jsonify(resp))
@flow.route("/getRedisValue",methods=["GET"])
def getRedisValue():
    key = request.args.get("key").strip()
    if "attr" in key:
        redis_key = key[2:-2].split("&&attr(")
        try:
            redis_value = redis.get(redis_key[0])
        except Exception as e:
            redis_pass_value = "%s获取失败,请检查上下文接口传递参数或检查参数格式!"%(redis_key[0])
            resp = {"datas":redis_pass_value,"code":"400"}
            return make_response(jsonify(resp))
        if redis_value:
            redis_pass_value =str(eval(redis_value.decode("utf-8") + str(redis_key[1].decode("utf-8"))))
        else:
            redis_pass_value = "未获取到缓存数据,请检查参数!"
    else:
        try:
            redis_value = redis.get(key)
        except Exception as e:
            redis_pass_value = "%s获取失败,请检查上下文接口传递参数或检查参数格式!" % (redis_value)
            resp = {"datas": redis_pass_value, "code": "400"}
            return make_response(jsonify(resp))
        if redis_value:
            redis_pass_value = redis_value
        else:
            redis_pass_value = "未获取到缓存数据,请检查参数!"
    resp = {"datas":redis_pass_value,"code":"200"}
    return make_response(jsonify(resp))
@flow.route("/getApiDesc",methods=["GET"])
def getApiDesc():
    api_id = request.args.get("api_id")
    api_data = Case_Http_API.query.filter(Case_Http_API.id==int(api_id)).first()
    api_desc_data = api_data.description
    resp = {"datas":api_desc_data,"code":"200"}
    return make_response(jsonify(resp))
@flow.route("/scheduleSuite",methods=["GET"])
def scheduleSuite():
    """工作流调度接口,传入domain(业务域),env_num,env_flag"""
    domain = request.args.get("domain")
    env_num = request.args.get("env_num")
    env_flag = request.args.get("env_flag")
    developer = request.args.get("developer")
    cookies = """{"env_flag":"%s","env_num":"%s"}"""%(env_flag,env_num)
    if domain:
        domainList = domain.strip().split(",")
        if len(domainList) == 1:
            suite = Run_Suite.query.filter(func.find_in_set(domainList[0],Run_Suite.domain)).filter(Run_Suite.statu==1)
            if suite.all()==[]:
                msg = "业务域不存在"
                resp_msg = {"datas": msg, "code": "400","total":"0"}
                return make_response(jsonify(resp_msg))
        else:
            sqlStr = """Run_Suite.query.filter(func.find_in_set("%s",Run_Suite.domain))"""
            conditionList = []
            for i in range(1,len(domainList)):
                unionStr = """union(%s)"""%(sqlStr%(domainList[i]))
                conditionList.append(unionStr)
            suite = eval(sqlStr%(domainList[0])+"."+".".join(conditionList).filter(Run_Suite.statu==1))#+".all()")
            # print suite_all.statement.compile(compile_kwargs={"literal_binds": True})
        #
        # run_suite_api.apply_async(
        #     args=[suite.count(),suite.all(),cookies,domain,developer],
        #     countdown=int(1))
        run_suite_api(suite.count(),suite.all(),cookies,domain,developer)
        resp_msg = {"datas":"功能域接口调度成功","code":"200","total":suite.count()}
    else:
        msg = "未传入业务域"
        resp_msg = {"datas":msg,"code":"400","total":"0"}
    return make_response(jsonify(resp_msg))