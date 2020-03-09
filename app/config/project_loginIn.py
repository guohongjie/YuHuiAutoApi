#!/usr/bin/python
#-*-coding:utf-8 -*-
###_author_:guohongjie
###封装接口测试登录前置
from app.base.pythonProject.base.getCookies import get_cookies
def loginIn(env_flag,env_num, account_project,
            account_username,account_passwd):
    """传入登录项目(中文)/测试环境&环境号码/登录账号密码,返回登录cookies"""
    new_cookies = get_cookies(account_project,env_flag,env_num,account_username,account_passwd)
    return new_cookies