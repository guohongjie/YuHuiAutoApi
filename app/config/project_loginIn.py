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

# def unescape(string,count):
#     string = urllib2.unquote(string).decode('utf8')
#     quoted = HTMLParser.HTMLParser().unescape(string).encode(sys.getfilesystemencoding())
#     new_string = re.sub(r'%u([a-fA-F0-9]{4}|[a-fA-F0-9]{2})', lambda m: unichr(int(m.group(1), 16)), quoted)
#     if count==0:
#         return new_string
#     else:
#         count -= 1
#         return unescape(new_string,count)
