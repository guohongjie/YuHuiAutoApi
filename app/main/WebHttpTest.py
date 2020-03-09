#-*-coding:utf-8 -*-
from app.main import test
from flask import request,make_response,jsonify,session,url_for
from app.base.pythonProject.base.getCookies import *
from app.config.project_loginIn import loginIn
from app.config.public_function import replace_cn
import sys,re
import json
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
    login_resp_msg = None
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