#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import unittest
import json
import hashlib
import redis
import urllib
# from log import TestLog,fengefu,lianjiefu
# from getConfig import ReadConfig
# logging = TestLog().getlog()
class Ysx_Porvider_Service_Info(unittest.TestCase):
    """用户信息查询"""
    @classmethod
    def setUp(self):
        self.session = requests.Session()
        request_retry = requests.adapters.HTTPAdapter(max_retries=3)
        self.session.mount("https://", request_retry)
        self.session.mount("http://", request_retry)
        header = {"Connection": "keep-alive"
            , "Content-Type": "application/x-www-form-urlencoded",
                  "Cache-Control": "no-cache",
                  "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 Safari/601.1 wechatdevtools/1.02.1904090 MicroMessenger/6.7.3 Language/zh_CN webview/15578306374265793 webdebugger port/22562"}
        self.session.headers = header
        # s = ReadConfig()
        # env_flag = s.get_env("env_flag")
        # env_num = s.get_env("env_num")
        cookies = {"env_flag": "beta", "env_num": "1"}
        self.session.cookies = requests.utils.cookiejar_from_dict(cookies)
        self.salt = "mengmengda"
    #     self.msg = u"""\n   {Case}     Except:  {Except}-*-\n        Really:  {Really}"""  # 校验HTTP返回代码
    #     # self.redis_host = s.get_env("beta").split(":") if env_flag == "beta" else s.get_env("prod_stage").split(":")
        r = redis.Redis(host="172.17.1.81", port=6389, password="yunshuxie1029Password")
        self.captcha = "111111"
        redis_shell = "code_1_60000007023"
        r.set(redis_shell, self.captcha)  # 设置验证码 111111
        r.expire(redis_shell, "30")  # 设置失效时间
    def test_01_user_check_user_exist(self):
        """用户手机号已存在<br/>https://api.yunshuxie.com/yunshuxie-passport-service/user/check_user_exist<br/>{"phone":"13260062372"}"""
        expect = {"code":"201001","message":u"手机号已存在"}
        url = r"https://api.yunshuxie.com/yunshuxie-passport-service/user/check_user_exist"
        params = {"phone":"13260062372"}
        string = urllib.urlencode(params)
        s = string + self.salt
        md = hashlib.md5()
        md.update(s)
        md5 = md.hexdigest()
        data = string + "&sign=" + md5
        print data
        self.resp = self.session.post(url, data=data)  # PC短信验证码登录
        print self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        assert result["code"] == expect["code"],self.msg.format(Case=u"查看是否注册", Except=expect["code"],Really=result["code"])
        assert result["message"] == expect["message"],self.msg.format(Case=u"查看是否注册", Except=expect["code"],Really=result["code"])
    def test_02_user_check_user_exist(self):
        """用户手机号未存在<br/>https://api.yunshuxie.com/yunshuxie-passport-service/user/check_user_exist<br/>{"phone":"13260062372"}"""
        expect = {"code": "201002", "message": u"用户不存在"}
        url = r"https://api.yunshuxie.com/yunshuxie-passport-service/user/check_user_exist"
        params = {"phone": "60000007017"}
        string = urllib.urlencode(params)
        s = string + self.salt
        md = hashlib.md5()
        md.update(s)
        md5 = md.hexdigest()
        data = string + "&sign=" + md5
        print data
        self.resp = self.session.post(url, data=data)  # PC短信验证码登录
        print self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        assert result["code"] == expect["code"], self.msg.format(Case=u"查看是否注册", Except=expect["code"],
                                                                 Really=result["code"])
        assert result["message"] == expect["message"], self.msg.format(Case=u"查看是否注册", Except=expect["code"],
                                                                       Really=result["code"])
    def test_03_user_register(self):
        """个人APP注册<br/>https://api.yunshuxie.com/yunshuxie-passport-service/user/register<br/>{"phone":"60000007023","code":"111111","pwd":"123456","memberType":"0","regType":"1"}"""
        url = r"https://api.yunshuxie.com/yunshuxie-passport-service/user/register"
        params = {"phone":"60000007023","code":"111111","pwd":"123456","memberType":"0","regType":"1"}
        string = urllib.urlencode(params)
        s = string + self.salt
        md = hashlib.md5()
        md.update(s)
        md5 = md.hexdigest()
        data = string + "&sign=" + md5
        print data
        self.resp = self.session.post(url, data=data)  # PC短信验证码登录
        print self.resp.content
        #result = json.loads(self.resp.content, encoding="utf8")


    @classmethod
    def tearDown(self):
        pass
if __name__ == "__main__":
    unittest.main()