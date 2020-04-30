#-*-coding:utf-8 -*-
from app.main import test
from flask import request,make_response,jsonify,session,url_for
from app.base.pythonProject.base.getCookies import *
from app.config.project_loginIn import loginIn
from app.config.public_function import replace_cn
import sys,re,time
import json
from app.config.sql import betaDB
import cgi
from collections import OrderedDict
from app.tasks.tasks import run_schedule_api
from app import redis
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
@test.route('/case_http_test',methods = ['POST'])
def case_http_test():
    """接口测试模块
    :param case_host:  domain
    :param case_url:  path
    :param method:  请求方式
    :return:  Response
    """
    login_resp_msg = "未进行登录"
    try:
        case_host = request.form["case_host"].strip()
        if case_host == None or case_host == "" or case_host == "None":
            raise Exception, "请求HOST不能为空!"
        case_url = request.form["case_url"].strip()
        if case_url == None or case_url == "" or case_url == "None":
            raise Exception, "请求URL不能为空!"
        method = request.form["method"].strip()
        if method == None or method == "" or method == "None":
            raise Exception, "请检查请求方式参数!"
        project_cn = request.form["project_cn"].strip()
        isSuiteOrigin = request.form.get("isSuiteOrigin")  # 用于判断流程图来源
        suiteName = request.form.get("suiteName")  # 流程图名称
        dept = session.get("deptName")
        if dept == u"其他":
            raise Exception,'当前部门无权限运行接口'
        params = request.form["params"]
        if params == "":
            raise Exception,"Params输入项不能为空,默认为None!"
        elif params[:4]=="str(":
            params = params[4:-1].replace("\'","\"")
            # wc = params.replace("""str(',"str(\"").replace("]'","]\"").replace("'","")
        else:
            try:
                params = eval(replace_cn(request.form["params"].strip()))
            except Exception as e:
                raise Exception,"Params输入项存在异常,请检查参数项!"
        headers = request.form["headers"]
        if headers == "":
            raise Exception,"Headers输入项不能为空,默认为None!"
        else:
            try:
                headers = eval(replace_cn(request.form["headers"].strip()))
            except Exception as e:
                raise Exception,"Headers输入项存在异常,请检查参数项!"
        cookies = request.form["cookies"]
        if cookies == "":
            raise Exception, "Cookies输入项不能为空,默认为None!"
        else:
            try:
                cookies = eval(replace_cn(request.form["cookies"].strip()))
            except Exception as e:
                raise Exception,"Cookies输入项存在异常,请检查参数项!"
        islogin = request.form["islogin"]
        account_project = request.form["account_project"]
        account_username = request.form["account_username"].strip()
        account_passwd = request.form["account_passwd"].strip()
        url = case_host + case_url
        if account_project.upper() == "NONE" or account_project=="":
            account_project = None
        if account_username.upper() == "NONE" or account_username=="":
            account_username = None
        if account_passwd.upper() == "NONE" or account_passwd=="":
            account_passwd = None
        if islogin.upper() == "TRUE" or islogin==True:  #勾选需要登录后获取登录cookies
            login_resp = loginIn(cookies["env_flag"], cookies["env_num"], account_project=account_project ,
                                  account_username=account_username,account_passwd=account_passwd)
            login_resp_code = login_resp["code"]
            login_resp_msg = login_resp["msg"]
            new_cookies = login_resp["cookies"]
            if login_resp_code != 200:    #登录失败-后续测试不进行
                response = make_response(jsonify({"code": 400, "test_datas": "前置登录失败,接口测试未进行","login_msg": login_resp_msg}))
                return response
            else:    #登录成功
                if method == "POST":
                    resp = postFunction(url, params, headers, new_cookies)
                    resp_msg = resp.content
                elif method == "GET":
                    resp = getFunction(url, params, headers, new_cookies)
                    resp_msg = resp.content
                if project_cn == u"CRM绩效规则重构" and "系统错误" not in resp.content:    #未系统错误进行
                    resp_dict = json.loads(resp_msg, encoding="utf8")
                    if resp_dict["returnCode"] != "0" and resp_dict["returnCode"] != 0:    #判断业务返回错误
                        resp_msg = resp_dict["returnMsg"]    #返回错误信息
                    else:    #例外接口
                        if case_url == "/v6/order/face_course/post/create_order.htm":
                            order_sn = update_order_status(resp_msg)    #业务返回信息传入,更改订单状态
                            resp_msg = order_sn    #订单号赋值返回信息
                        else:
                            phone = params["phone"]
                            phId = params["phId"]
                            pId = params["pId"]
                            order_sn = update_order_status(resp_msg)  # 更改订单状态=2,call_back＝当前时间,返回order_sn　字段
                            if pId in ["7698", "8326", "8327", "8215", "7996","9224",
                                       "9225","9226","9227","9228","9229"]:  # 罐罐熊正式课&练字课商品ID,并对应授权
                                msg = bearJoinCategoryProduct(phone, phId, order_sn, new_cookies)
                            else:
                                msg = joinCategoryProduct(phone, phId,
                                                          order_sn, new_cookies)  # 传入order_sn字段,查找　memberId,orderId

                            resp_msg = order_sn + ":" + msg
        else:    #不需要登录
            new_cookies = cookies
            if method == "POST":
                resp = postFunction(url, params, headers, new_cookies)
            elif method == "GET":
                resp = getFunction(url, params, headers, new_cookies)
            login_resp_msg = "该接口配置无需登录"
            if resp.status_code == 200:
                resp_msg = resp.content
            else:
                resp_msg = resp.content
                response = make_response(jsonify(
                    {"code": 400, "test_datas": cgi.escape(resp_msg), "login_msg": login_resp_msg}))  # 返回response
                return response
    except Exception as e:
        resp_msg = str(e)
    else:
        if isSuiteOrigin in["1","2"] and resp.status_code==200: #1 测试按钮来源; 2 调度测试来源
            resultRE = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
            redis.set(suiteName,json.dumps(resultRE,ensure_ascii=False,encoding="utf8"),600)
    response = make_response(jsonify({"code":200,"test_datas":cgi.escape(resp_msg),"login_msg":login_resp_msg}))  # 返回response
    return response
@test.route('/doSelfSchedule',methods = ['POST'])
def doSelfSchedule():
    try:
        api_json = request.form["api_json"]
        schedule_env = request.form["schedule_env"]
        schedule_num = request.form["schedule_num"]
        timer = request.form["timer"]
        api_dict = json.loads(api_json,encoding='utf8')
        orderApiDict = OrderedDict(api_dict.items())    #手工调度接口排序
        cookies = {"env_flag":schedule_env,"env_num":schedule_num}    #cookies
        userName = session['userName']
        origin = "doSelfSchedule"    #来源,异步任务识别操作来源
        task = run_schedule_api.apply_async(
            args=[origin,orderApiDict,cookies,userName],
            countdown=int(timer))
        msg = {"code": "200", "msg": "操作成功","id":task.id}
        return jsonify(msg), 202, {'Location': url_for('api_test.taskstatus', task_id=task.id)}
    except Exception as e:
        msg = {"code": "400", "msg": "操作失败","method":"doSelfSchedule","reason": str(e)}
    return make_response(jsonify(msg))
@test.route('/status/<task_id>')
def taskstatus(task_id):
    task = run_schedule_api.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': u'启动中...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', ''),
            'pass_status':task.info.get('pass_status',''),
            'datas':task.info.get('data_list','')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
            'errorMsg':str(task.traceback)
        }
    return jsonify(response)


def postFunction(url,params,headers,cookies):
    resp_req_data = requests.post(url,data=params,headers=headers,cookies=cookies)
    if resp_req_data.status_code != 200:
        resp_req_json = requests.post(url, json=params, headers=headers, cookies=cookies)
        if resp_req_json.status_code!= 200:
            return resp_req_data
        else:
            return resp_req_json
    return resp_req_data
def getFunction(url,params,headers,cookies):
    resp_req_data = requests.get(url, params=params, headers=headers, cookies=cookies)
    if resp_req_data.status_code != 200:
        resp_req_json = requests.get(url, json=params, headers=headers, cookies=cookies)
        if resp_req_json.status_code!= 200:
            return resp_req_data
        else:
            return resp_req_json
    return resp_req_data
def postFunctionFile(url,params,headers,cookies,file):
    resp = requests.post(url,data=params,headers=headers,cookies=cookies,files=file)
    return resp
def getFunctionFile(url,params,headers,cookies,file):
    resp = requests.get(url, params=params, headers=headers, cookies=cookies,files=file)
    return resp







@test.route("/test_upload",methods=["POST"])
def upload_test():
    project_cn = request.form["project_cn"]
    case_host = request.form["case_host"]
    case_url = request.form["case_url"]
    method = request.form["method"]
    file_desc = request.form["file_desc"]
    try:
        params = eval(request.form["params"])
        headers = eval(request.form["headers"])
        cookies = eval(request.form["cookies"])
        islogin = request.form["islogin"]
        account = request.form["account"]
        file_1 = request.files['file']
        upload_file = {file_desc:(file_1.filename, file_1, file_1.mimetype)}
        url = case_host + case_url
        if account.upper() == "NONE" or account == None:
            account = None
        if islogin.upper() == "TRUE" or islogin == True:
            new_cookies = loginIn(project_cn,cookies["env_flag"], cookies["env_num"], account).get_dict()
        else:
            new_cookies = cookies
        if method == "POST":
            resp = postFunctionFile(url, params, headers, new_cookies,upload_file)
        elif method == "GET":
            resp = getFunctionFile(url, params, headers, new_cookies,upload_file)
    except Exception as e:
        resp = str(e)
    response = make_response(jsonify({"code": 200, "datas": resp}))  # 返回response
    return response
def update_order_status(resp):
    select_data = betaDB()
    resp_dict = json.loads(resp, encoding="utf8")
    outTradeNo = resp_dict["data"]["outTradeNo"]
    sql = """update ysx_order.ysx_order_info a  set a.order_state="2" , a.callback_time= now(),a.ORDER_AMOUNT='100',a.ORIGINAL_AMOUNT='100' where a.order_sn ="{order_sn}";""".format(
    order_sn=outTradeNo)
    select_data.execute_sql(sql)
    select_data.execute_close()
    resp = outTradeNo
    return resp
def joinCategoryProduct(phone,phId,resp,new_cookies):
    select_data = betaDB()
    order_sn = resp
    sql = """select a.order_id,a.member_id from ysx_order.ysx_order_info a where a.order_sn ="{order_sn}";""".format(order_sn=order_sn)
    data = select_data.execute_select(sql)
    order_id,member_id = data[0][0],data[0][1]
    phone = phone
    productCoursehourseId = phId
    accreditReason = u"测试使用"
    url = r"https://admin.yunshuxie.com/v1/admin/write_source/writeCourse/joinCategoryProduct.json"
    request_params = {"memberId":member_id,"orderId":order_id,"phone":phone,
                      "productCoursehourseId":productCoursehourseId,"accreditReason":accreditReason}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
    resp = requests.post(url=url,data=request_params,headers=headers,cookies=new_cookies)
    resp_dict = json.loads(resp.text,encoding="utf8")
    if phId=="9772" or phId==9772:
        chanel_url = """https://admin.yunshuxie.com/v2/live_course/role/member_role_list.json?memberId=&phone={phone}&sort=memberId&order=asc&limit=10&offset=0&_=1572507705540""".format(phone=phone)
        chanel_resp = requests.get(url=chanel_url,headers=headers,cookies=new_cookies)
        chanel_resp_dict = json.loads(chanel_resp.text, encoding="utf8")
        moocClassId = chanel_resp_dict["rows"][0]["moocClassId"]
        update_order_sn_sql = """update ysx_order.ysx_wechat_service_user a 
set a.order_sn="{order_sn}"
where a.PHONE="{phone}" and a.MOOC_CLASS_ID="{moocClassId}";""".format(order_sn=order_sn,phone=phone,moocClassId=moocClassId)
        select_data.execute_sql(update_order_sn_sql)
        select_data.execute_close()
    if productCoursehourseId == "9639":
        mzjd_sql = """select a.PRODUCT_COURSE_HOURS_IDS from ysx_order.ysx_order_item a where a.order_id={order_id};""".format(order_id=order_id)
        data = select_data.execute_select(mzjd_sql)
        phids = data[0][0].split(",")
        text = ""
        for phid in range(0,len(phids)-1):
            request_params = {"memberId": member_id, "orderId": order_id, "phone": phone,
                              "productCoursehourseId": phids[phid], "accreditReason": accreditReason}
            resp = requests.post(url=url, data=request_params, headers=headers, cookies=new_cookies)
            text = resp.text
            resp_dict = json.loads(resp.text, encoding="utf8")
            if resp_dict["returnCode"] == 0 or resp_dict["returnCode"] == "0":
                text += "授权成功,"
            else:
                text +="授权课程请求失败,"
        return text
    else:
        request_params = {"memberId": member_id, "orderId": order_id, "phone": phone,
                          "productCoursehourseId": productCoursehourseId, "accreditReason": accreditReason}
        resp = requests.post(url=url,data=request_params,headers=headers,cookies=new_cookies)
        resp_dict = json.loads(resp.text,encoding="utf8")
        if resp_dict["returnCode"] == 0 or resp_dict["returnCode"] == "0":
            return "授权成功"
        else:
            return "授权课程请求失败"
def bearJoinCategoryProduct(phone,phId,resp,new_cookies):
    select_data = betaDB()
    sql = """select a.order_id,a.member_id from ysx_order.ysx_order_info a where a.order_sn ="{order_sn}";""".format(order_sn=resp)
    data = select_data.execute_select(sql)
    order_id,member_id = data[0][0],data[0][1]
    phone = phone
    productCoursehourseId = phId
    accreditReason = u"测试使用"
    if phId == "9775":
        categoryId = "106"
    else:
        categoryId = "102"
    grade = "1"
    url = r"https://admin.yunshuxie.com/v1/elementary/joinCategoryProduct.json"
    request_params = {"memberId":member_id,"orderId":order_id,"phone":phone,"categoryId":categoryId,"grade":grade,
                      "productCoursehourseId":productCoursehourseId,"accreditReason":accreditReason}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
    resp = requests.post(url=url,data=request_params,headers=headers,cookies=new_cookies)
    resp_dict = json.loads(resp.text,encoding="utf8")
    if resp_dict["returnCode"] == 0 or resp_dict["returnCode"] == "0":
        return "授权成功"
    else:
        return "授权课程请求失败"




#
# @test.route("/ClassInCreate",methods=["GET"])
# def ClassInCreate():
#     """
#     Admin创建ClassIn流程启动
#     :return:
#     """
#     env_flag = request.args.get("env_flag")
#     env_num = request.args.get("env_num")
#     phone = request.args.get("phone")
#     developer =request.args.get("developer")
#     redis.set("ClassInCreate", "{'phone':'%s'}"%phone, 600)
#     redis.set("ClassInCreateFlag", "{'env_flag':'%s'}"%env_flag, 600)
#     redis.set("ClassInCreateNum", "{'env_num':'%s'}"%env_num, 600)
#     url = "http://uwsgi.sys.bandubanxie.com/scheduleSuite?domain=ClassIn&env_flag=%s&env_num=%s&developer=%s"%(env_flag,env_num,developer)
#     wctv = {}
#     resp = requests.get(url=url)
#     time.sleep(10)
#     value = redis.get("v1/admin/product_chapter/create_live_room.json")
#     wctv["schedule"] = resp.text
#     wctv["RoomMsg"] = value
#     return make_response(jsonify(wctv))