#!/usr/bin/python
# -*-coding:utf-8-*-
__author__ = "guohongjie"
import requests
import json
def get_cookie(env_flag,env_num,account_username=None,account_passwd=None):
    """登录接口,并返回cookies
    :param url 请求连接
    :param header 请求头
    :return cookies"""
    cookies = requests.cookies.RequestsCookieJar()  # 生成cookies 容器
    cookies.set('env_flag', env_flag)  #设置测试环境
    cookies.set("env_num",env_num)  #设置环境号
    username = account_username   #默认账号
    password = account_passwd   #默认密码
    url = r""    #登录接口
    params = {"username":username,"password":password}  # 登录参数
    header = {"Accept": "application/json, text/javascript, */*; q=0.0",
              "Cache-Control": "no-cache",
              "Connection": "keep-alive",
              "Pragma": "no-cache",
              "Content-Type": "application/x-www-form-urlencoded",
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
              "X-Requested-With": "XMLHttpRequest"}
    resp = requests.post(url,headers=header,data=params,cookies=cookies)
    try:
        if resp.status_code == 200:
            dict_resp = json.loads(resp.content, encoding="utf8")
            if dict_resp["code"] == "0" or dict_resp["code"] == 0:
                cookies.update(resp.cookies)
                msg = "登录成功,进行后续操作..."
                code = 200
            else:
                msg = "登录失败,请检查用户名及密码准确!"
                code = 400
        else:
            msg = "服务器返回码错误,请检查登录系统环境!"
            code = 400
    except Exception as e:
        msg = "登录失败,失败提示:%s" % (str(e))
        code = 400
    return {"msg": msg, "cookies": cookies, "code": code}
def get_cookies(project,env_flag,env_num,account_username=None,account_passwd=None):
    """
    :param project: 发布项目
    :param env_flag: 发布环境
    :param env_num: 发布环境号
    :return: cookies
    """
    if project == "":    #定义某个登录方法
        cookie = get_cookie(env_flag,env_num,account_username,account_passwd)
    else:
        cookie = {"msg": "未封装登录程序", "cookies":None, "code":400}
    return cookie

if __name__ == "__main__":
    #print get_wechat_teaco_cookies("beta","5","向前！向前！")
    phone = 60000012616
    #while True:
#
    get_cookie("beta","8","%s"%(phone))
      #  phone += 1
     #   if phone>60000012530:
       #     break

