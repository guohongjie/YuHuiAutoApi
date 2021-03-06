#!/usr/bin/python
# -*-coding:utf-8-*-
__author__ = "guohongjie"
import requests
import redis
from py_redis import MyRedis
import json
import hashlib
import urllib
import pymysql
from app.config.config import SystemConfig





def get_material_platform_cookies(env_flag,env_num,account_username=None,account_passwd=None):
    """物料平台登录"""
    url = "wc"
    cookies = requests.cookies.RequestsCookieJar()  # 生成cookies 容器
    cookies.set('env_flag', env_flag)  # 设置测试环境
    cookies.set("env_num", env_num)  # 设置环境号
    header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
    username = account_username
    pwd = account_passwd
    params = {"phone": username,"pwd": pwd}
    resp = requests.get(url=url, headers=header, cookies=cookies, params=params)
    try:
        if resp.status_code == 200:
            dict_resp = json.loads(resp.content, encoding="utf8")
            if dict_resp["returnCode"] == "0" or dict_resp["returnCode"] == 0:
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
    if project == "":
        cookie = (env_flag,env_num,account_username,account_passwd)
    else:
        cookie = {"msg": "未封装登录程序", "cookies":None, "code":400}
    return cookie


