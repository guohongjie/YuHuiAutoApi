#!/usr/bin/python
# -*-coding:utf-8
from binascii import b2a_hex, a2b_hex
import re
import requests
import json
from urllib import unquote
from app import redis as res
from redis.exceptions import ConnectionError
import random
from app.base.pythonProject.base.getCookies import get_cookies
from requests_toolbelt import MultipartEncoder
import datetime


def replace_cn(str_params):
    """修改全角字符"""
    new_str_params = str_params.replace("＂", '"')
    new_str_params1 = new_str_params.replace("＂", '"')
    new_str_params2 = new_str_params1.replace("＇", "'")
    new_str_params3 = new_str_params2.replace("，", ",")
    new_str_params4 = new_str_params3.replace("｛", "{")
    new_str_params5 = new_str_params4.replace("｝", "}")
    new_str_params6 = new_str_params5.replace("：", ":")
    return new_str_params6


def run_test(origin, dict_datas, cookies):
    try:
        if origin == "doSelfSchedule":
            url = dict_datas["case_host"] + dict_datas["case_url"]  # 请求连接
            method = dict_datas["method"]  # 请求方式
            headers = eval(replace_cn(dict_datas["headers"].strip()))  # 请求头
            islogin = dict_datas["islogin"]  # 是否需要前置登录
            case_api = dict_datas["case_api"]  # 接口名称
            isSchedule = dict_datas["isSchedule"]
            checkAssert = dict_datas["checkAssert"]
            cookies = cookies
            params = eval(replace_cn(dict_datas["params"].strip()))  # 请求参数
        else:  # 集成调度
            project = dict_datas["project"]  # 业务项目
            url = dict_datas["case_host"] + dict_datas["case_url"]  # 请求连接
            method = dict_datas["method"]  # 请求方式
            assertValue = dict_datas["assertValue"]
            headers = eval(replace_cn(dict_datas["headers"]).strip())  # 请求头
            islogin = dict_datas["islogin"]  # 是否需要前置登录
            case_api = dict_datas["case_api"]  # 接口名称
            cookies = cookies
            params = eval(replace_cn(dict_datas["params"].strip()))  # 请求参数(需要进行参数传递设置,暂时不修改)
    except Exception as e:
        pass_status = "Mistake"
        error_msg = "参数错误,请检查参数"
        return pass_status, error_msg
    else:
        try:
            if islogin:  # 判断需要登陆状态时，进行登录
                env_flag = cookies["env_flag"]
                env_num = cookies["env_num"]
                account_project = dict_datas["account_project"]  # 需要登录状态时,获取登录状态
                account_username = dict_datas["account_username"]
                account_password = dict_datas["account_passwd"]
                if not account_username and not account_project or not account_password:
                    account_project, account_username, account_password = None, None, None
                elif account_project.upper() == "NONE" and account_username.upper() == "NONE" or account_password.upper() == "NONE":
                    account_project, account_username, account_password = None, None, None
                cookies = get_cookies(account_project, env_flag, env_num,
                                      account_username=account_username,
                                      account_passwd=account_password)  # 更新cookies信息，变更为已登录
                if cookies["code"] != 200:
                    raise Exception, "登录失败!请检查用户名密码!"
                else:
                    new_cookies = cookies["cookies"].get_dict()
                    if method.upper() == "GET":
                        resp = getFunction(url=url, headers=headers, params=params, cookies=new_cookies)
                    else:
                        resp = postFunction(url=url, headers=headers, params=params, cookies=new_cookies)
            else:
                cookies = cookies
                if method.upper() == "GET":
                    resp = getFunction(url=url, headers=headers, params=params, cookies=cookies)
                else:
                    resp = postFunction(url=url, headers=headers, params=params, cookies=cookies)
            if origin == "doSelfSchedule":  # 判断当前调度等于手工调度
                if resp.status_code == 200:
                    if isSchedule:  # 参加校验
                        assert_list = checkAssert.split(",")
                        for assert_value in assert_list:
                            assertResult = re.findall(assert_value, resp.text)
                            if assertResult:
                                pass_status = "Success"
                            else:
                                pass_status = "Failure"
                    else:  # 不参加校验
                        pass_status = "Success"
                else:
                    pass_status = "Failure"
            else:  # 集成调度(需要进行参数值校验,暂时不添加)
                if resp.status_code == 200:
                    try:
                        resp_dict = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
                        pass_status = "Success"
                    except Exception as e:
                        pass_status = "Failure"
                else:
                    pass_status = "Mistake"
            return pass_status, resp.text
        except Exception as e:
            pass_status = "Mistake"
            error_msg = case_api + ':' + str(e)
            return pass_status, error_msg


def postFunction(url, params, headers, cookies):
    resp = requests.post(url, data=params, headers=headers, cookies=cookies)
    return resp


def getFunction(url, params, headers, cookies):
    resp = requests.get(url, params=params, headers=headers, cookies=cookies)
    return resp


def wechatQY_msg(developer, project_cn, success_count, fail_count, mistake_count, report_url, cookies):
    try:
        if mistake_count is None:
            content = u"""工作流调度测试结果: \n发起者: {developer} \n测试项目: {project_en} \n测试环境: {cookies} \n通过工作流: {success_count} \n未通过工作流: {fail_count} \n结果查看地址: {report_url}""".format(
                project_en=project_cn,
                success_count=success_count,
                fail_count=fail_count,
                developer=developer,
                report_url=report_url,
                cookies=cookies
            )
        else:
            content = u"""接口平台调度测试结果:\n测试: {developer} \n测试项目: {project_en} \n通过接口数: {success_count} \n未通过接口数: {fail_count} \n程序失败接口数: {mistake_count} \n结果查看地址: {report_url}""".format(
                project_en=project_cn,
                success_count=success_count,
                fail_count=fail_count,
                mistake_count=mistake_count,
                developer=developer,
                report_url=report_url
                )
        params = {
            "tos": u"guohongjie,renhuihui,zhaohongling,pengjunxia,wangmengxiao,hongchen,tianningxue,liushuang,xuhongying,jiayujiao,panze,huyanfeng,liangguoqing,{developer}".format(
                developer=developer),
            "content": content, "app": "qa", "sed": "guohongjie"}
        qiye_wechat_url = r"http://msg.inf.bandubanxie.com/api/v0.2/msg/qiye_weixin"
        requests.post(url=qiye_wechat_url, data=params)
        return True
    except Exception as e:
        raise Exception, str(e)


def isPassParams(apiName, params):
    try:
        compile = re.compile("(\$\(.*?\))")
        result = re.findall(compile, params)
        evalCompile = re.compile("eval(.*?)end")
        evalResult = re.findall(evalCompile, params)
        # result.extend(evalResult)
        if not result and not evalResult:
            return params
        elif not result and evalResult:
            if evalResult:
                parseEvalDictValue = parseEvalValue(evalResult)
                for key, value in parseEvalDictValue.items():
                    newParams = params.replace("eval" + key.decode("utf8") + "end", value.decode("utf8"))
                    params = newParams
                return params
        else:
            if evalResult:
                parseEvalDictValue = parseEvalValue(evalResult)
                for key, value in parseEvalDictValue.items():
                    newParams = params.replace("eval" + key.decode("utf8") + "end", value.decode("utf8"))
                    params = newParams
            if result:
                parseDictValue = parseParams(result)  # 开始替换参数
                for key, value in parseDictValue.items():
                    newParams = params.replace(key.decode("utf8") + ')', value.decode("utf8"))
                    params = newParams
            return params
    except Exception as e:
        return apiName + ":" + str(e)


def parseParams(result):
    listValue = []
    dict_Key_Value = {}

    map(lambda x: listValue.append(x[2:-1].split("&&attr(")), result)
    for i in range(len(listValue)):
        try:
            if len(listValue[i]) == 1:
                redis_value = res.get(listValue[i])
                if redis_value:
                    subNullRedisValue = redis_value.decode("utf8").replace("null,", "\"null\",").replace("false,", "\"false\",").replace("true,", "\"true\",")
                    dict_Key_Value[result[i]] = unquote(str(eval(subNullRedisValue)))
                else:
                    dict_Key_Value[result[i]] = "未获取到缓存数据,请检查参数!"
            else:
                redis_value = res.get(listValue[i][0])
                if redis_value:
                    subNullRedisValue = redis_value.decode("utf8").replace("null,", "\"null\",").replace("false,", "\"false\",").replace("true,", "\"true\",")
                    dict_Key_Value[result[i]] = unquote(
                        str(eval(subNullRedisValue + str(listValue[i][1]).decode("utf-8"))))
                else:
                    dict_Key_Value[result[i]] = "未获取到缓存数据,请检查参数!"
        except SyntaxError as e:
            dict_Key_Value[result[i]] = "参数语法错误,请检查上下文接口参数或检查请求参数化!"
        except IndexError as e:
            dict_Key_Value[result[i]] = "参数索引错误,请检查上下文接口参数或检查请求参数化!"
        except ConnectionError as e:
            dict_Key_Value[result[i]] = "redis链接错误,请检redis服务配置!"
    return dict_Key_Value


def parseEvalValue(evalResult):
    dict_Key_Value = {}
    for evalValue in evalResult:
        try:
            newEvalVale = evalValue.replace("&nbsp", " ")
            wc = eval(newEvalVale)
            dict_Key_Value[evalValue] = wc
        except SyntaxError as e:
            dict_Key_Value[evalValue] = "参数语法错误!"
        except IndexError as e:
            dict_Key_Value[evalValue] = "参数索引错误,请检查上下文接口参数或检查请求参数化!"
        except ConnectionError as e:
            dict_Key_Value[evalValue] = "redis链接错误,请检redis服务配置!"
    return dict_Key_Value


def outerOrderRect(dictA):
    wc = []
    wd = []
    states = dictA["states"]
    for key, value in states.items():
        if value["text"]["text"] == u"开始":
            start_rect = key
        if value["text"]["text"] == u"结束":
            end_rect = key
    dictA_path = dictA["paths"]

    def wctv(start_rect, pathTo, dictA_path):
        temp_dict = {}
        for key, value in dictA_path.items():
            if value["from"] == pathTo:
                temp_dict["from"] = dictA["states"][value["from"]]["text"]["text"]
                temp_dict["to"] = value["text"]["text"]
                wc.append(temp_dict)
                if value["from"] == start_rect:
                    wd.append(value["from"])
                    wd.append(value["to"])
                else:
                    wd.append(value["to"])
                return wctv(start_rect, value["to"], dictA_path)

    wctv(start_rect, start_rect, dictA_path)
    if wd.index(start_rect) != 0:
        raise Exception, "解析失败:未存在开始步骤!"
    if end_rect != wd[-1]:
        raise Exception, "解析失败:未存在结束步骤!"
    return wd, wc


# ClassIn创建课程任务
def saveOrUpdate_live_product_chapter(env_flag, env_num, productCourseId):
    start_time = (datetime.datetime.now() + datetime.timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M:%S")
    end_time = (datetime.datetime.now() + datetime.timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")
    cookies = get_cookies(project="云舒写ADMIN后台管理系统", env_flag=env_flag,
                          env_num=env_num,
                          account_username="automation@yunshuxie.com",
                          account_passwd="test123456")
    search_chapter_url = "https://admin.yunshuxie.com/v1/admin/product_chapter/query_product_chapter_list.json"
    contentHeader = {'Content-Type': 'application/json;charset=UTF-8',
                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    searchParams = {"productCourseId": productCourseId, "sort": "sortCode", "order": "asc", "limit": "1000",
                    "offset": "0"}
    searchChapterResp = requests.get(url=search_chapter_url, headers=contentHeader, params=searchParams,
                                     cookies=cookies["cookies"].get_dict())
    if searchChapterResp.status_code == 200:
        delete_room_url = "https://admin.yunshuxie.com/v1/admin/product_chapter/delete_product_chapter.json"
        deleteHeaders = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
        chapterRespText = json.loads(searchChapterResp.text, encoding="utf8")
        for i in range(len(chapterRespText["rows"])):
            productChapterId = chapterRespText["rows"][i]["productChapterId"]
            deleteProductChapterParams = {"productChapterId": productChapterId}
            deleteResp = requests.post(url=delete_room_url,
                                       headers=deleteHeaders,
                                       data=deleteProductChapterParams,
                                       cookies=cookies["cookies"].get_dict())
            if deleteResp.status_code != 200:
                return deleteResp
        url = "https://admin.yunshuxie.com/v1/admin/product_chapter/saveOrUpdate_live_product_chapter.json"
        params = {"productChapterId": "-1",
                  "productCourseId": productCourseId,  # "107564",
                  "jsonData":
                      """[{"sortCode":"1","templateType":1,"templateDataContent":{"title":"学习计划","content":"回答"}},{"sortCode":"2","templateType":1,"templateDataContent":{"title":"学习任务","content":"回答2"}}]""",
                  "productChapterTitle": "测试任务-%s" % (start_time),
                  "wordsNumber": "0",
                  "introduction": "测试描述", "readAbilityType": "-1", "sortCode": "1",
                  "liveTeacherId": "68",
                  "liveTeacherName": "测试老师专用1",
                  "chapterStartTime": start_time,
                  "chapterEndTime": end_time,
                  "isDiscuss": "2",
                  "isJob": "2",
                  "content": "测试开创问题1",
                  "title": "学习计划", "title": "学习任务",
                  "content": "测试开创问题2", "button": "", "fileTypeArray": ""}
        headers = {
            "Content-Type": "",
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://admin.yunshuxie.com",
            "Referer":
                "https://admin.yunshuxie.com/v1/admin/live_product_info/edit_live_product_course.htm?productCourseId=107564&productType=137",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        m = MultipartEncoder(
            fields=params)
        headers['Content-Type'] = m.content_type
        resp = requests.post(url=url, headers=headers, data=m,
                             cookies=cookies["cookies"].get_dict())
        return resp
    else:
        return searchChapterResp

if __name__ == "__main__":
    print saveOrUpdate_live_product_chapter(env_flag="prod",
                                            env_num="1",
                                            productCourseId="107656")