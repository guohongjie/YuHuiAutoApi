#!/usr/bin/python
#-*-coding:utf-8 -*-
from getCookies import get_wacc_admin_cookie,get_ysx_crm_cookie
import requests
from requests_toolbelt import MultipartEncoder
import json
def makeUser_test(env_flag,env_num,phone,role):
    """
    admin创建用户&crm备注测试账号
    """
    userPhones = phone.split(",")
    employeeTypes = role.split(",")
    if len(userPhones) != len(employeeTypes):
        raise Exception("用户手机号和用户角色数量不等！")
    else:
        resp_msg = add_admin_crm_tester(env_flag,env_num,userPhones,employeeTypes)
        return resp_msg,userPhones,employeeTypes

def add_admin_crm_tester(env_flag,env_num,userPhones,employeeTypes):
    resp_cookies = get_wacc_admin_cookie(env_flag,env_num)
    if resp_cookies["code"] != 200:
        raise Exception, "登录失败,请检查登录配置"
    else:
        alert_list_msg =[]
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest", "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "zh-CN,zh;q=0.9", "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryF7Lcp4O5PcTcLugw"}
        session = requests.Session()
        session.headers = header
        session.cookies = resp_cookies["cookies"]
        request_retry = requests.adapters.HTTPAdapter(max_retries=3)
        session.mount("https://", request_retry)
        session.mount("http://", request_retry)
        url = r"https://admin.yunshuxie.com/v1/admin/account/add/user.json"
        userNames = ["测试_" + userName for userName in userPhones]
        for index in range(len(userNames)):
                if len(userPhones[index]) != 11:
                    text = "{phone}:ADMIN手机号不等于11位!CRM:未执行!\n".format(phone=userPhones[index])
                    alert_list_msg.append(text)
                else:
                    datas = {"memberIcon": "", "pwd": "test123456",
                             "email": "automation@yunshuxie.com", "weiboName": "",
                             "nickName": userNames[index], "qq": "",
                             "interest": "", "phone": userPhones[index], "weichatNum": "",
                             "remark": "自动化测试",
                             "memberType": employeeTypes[index],
                             "ChoiceOfTeacher": "默认分组",
                             "ChoiceOfTeacher": "默认分组",
                             "readRole": "0", "ChoiceOfTeacher": "云舒写教育科技",
                             "button": ""}
                    data = MultipartEncoder(datas)
                    header["Content-Type"] = data.content_type
                    resp = session.post(url, data=data)
                    if resp.status_code == 200:
                        result = json.loads(resp.content)
                        if result["returnCode"] == "0":
                            crm_resp_msg = add_crm_tester(env_flag,env_num,userPhones[index])
                            text = "{phone}:ADMIN{msg}!CRM:{crm_resp}!\n".format(msg=result["returnMsg"],phone=userPhones[index],crm_resp=crm_resp_msg)
                            alert_list_msg.append(text)
                        else:
                            text = "{phone}:ADMIN{msg}!CRM:未执行!\n".format(msg=result["returnMsg"],phone=userPhones[index])
                            alert_list_msg.append(text)
                    else:
                        text = "{phone}:ADMIN服务器返回非200!CRM:未执行!\n".format(phone=userPhones[index])
                        alert_list_msg.append(text)
        alert_msg = " ".join(alert_list_msg)
        return alert_msg
def add_crm_tester(env_flag,env_num,phone):
    url = r"https://admin.crm.yunshuxie.com/test/account/management/insert/test/account"
    resp_cookies = get_ysx_crm_cookie(env_flag,env_num)
    if resp_cookies["code"] != 200:
        raise Exception, "登录失败,请检查登录配置"
    else:
        header = {"Accept": "application/json, text/javascript, */*; q=0.01", "Accept-Encoding": "gzip, deflate",
               "Accept-Language": "zh-CN,zh;q=0.9", "Cache-Control": "no-cache", "Connection": "keep-alive",
               "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Pragma": "no-cache",
               "Referer": "http://admin.crm.yunshuxie.com/test/account/management/goto/insert/test/account",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
               "X-Requested-With": "XMLHttpRequest"}
        session = requests.Session()
        session.headers = header
        session.cookies = resp_cookies["cookies"]
        data = {"phones": phone, "userNames": "测试_{phone}".format(phone=phone), "employeeTypes": 0}
        resp = session.post(url, data=data)
        if resp.status_code==200:
            result = json.loads(resp.content)
            if result["returnCode"] == 0:
                return "添加成功!"
            else:
                return "添加失败!"
        else:
            return "CRM服务器返回非200!"