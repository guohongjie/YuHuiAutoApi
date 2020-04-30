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
class Ysx_Porvider_Service_Login(unittest.TestCase):
    """用户信息操作服务"""
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
        cookies = {"env_flag": "stage", "env_num": "2"}
        self.session.cookies = requests.utils.cookiejar_from_dict(cookies)
        self.salt = "mengmengda"
        self.msg = u"""\n   {Case}     Except:  {Except}-*-\n        Really:  {Really}"""  # 校验HTTP返回代码
    def test_01_user_login(self):
        """账号密码登录_type=APP登录(1) 微信登录(2) Pc登录(3)
        :param: userName = 60000007001
        :param: pwd = 123456
        :param: type = 1
        :return code == 0
        """
        expect = {"code":"0"}
        url = r"https://api.yunshuxie.com/yunshuxie-passport-service/user/login"
        params = {"userName": "60000007001", "pwd": "123456", "type": "1"}
        string = urllib.urlencode(params)
        s = string + self.salt
        md = hashlib.md5()
        md.update(s)
        md5 = md.hexdigest()
        data = string + "&sign=" + md5
        self.resp = self.session.post(url, data=data)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        assert result["code"] == expect["code"],self.msg.format(Case=u"APP账号密码登录",Except=expect["code"],Really=result["code"])
        params = {"userName": "60000007001", "pwd": "123456", "type": "2","wechatCode":"081NtWKq1tU8kl0Vf5Iq1ddyKq1NtWKY"}
        string = urllib.urlencode(params)
        s = string + self.salt
        md = hashlib.md5()
        md.update(s)
        md5 = md.hexdigest()
        data = string + "&sign=" + md5
        self.resp = self.session.post(url, data=data)
        result = json.loads(self.resp.content, encoding="utf8")
        assert result["code"] == expect["code"], self.msg.format(Case=u"微信账号密码登录",Except=expect["code"],
                                                                       Really=result["code"])
        params = {"userName": "60000007001", "pwd": "123456", "type": "3"}
        string = urllib.urlencode(params)
        s = string + self.salt
        md = hashlib.md5()
        md.update(s)
        md5 = md.hexdigest()
        data = string + "&sign=" + md5
        self.resp = self.session.post(url, data=data)
        result = json.loads(self.resp.content, encoding="utf8")
        assert result["code"] == expect["code"], self.msg.format(Case=u"PC账号密码登录",Except=expect["code"],
                                                                       Really=result["code"])
    def test_02_user_login(self):
        """短信验证码登录_type=APP登录(6) 微信登录(7) Pc登录(8)
        :param: phone == 13260062372
        :param: type == APP登录(6) 微信登录(7) Pc登录(8)
        :return:  code == 0
        """
        url = r"https://api.yunshuxie.com/yunshuxie-message-service/sms/get_phone_code"
        params_get_phone_code = {"platform": "0", "phone": "13260062372", "verType": "2"}  #1登录 ;2修改手机号
        string = urllib.urlencode(params_get_phone_code)
        s = string + self.salt
        md = hashlib.md5()
        md.update(s)
        md5 = md.hexdigest()
        data = string + "&sign=" + md5
        self.resp = self.session.post(url, data=data)
        dict_resp = json.loads(self.resp.content, encoding="utf8")
        expect = {"code": "0"}
       # print self.resp.content
        assert dict_resp["code"] == expect["code"], self.msg.format(Case="get_phone_code",Except=expect["code"], Really=dict_resp["code"])
        r = redis.Redis(host="172.17.1.44", port=6379, password="yunshuxie1029Password")
        redis_shell = "code_" + params_get_phone_code["verType"] + "_" + params_get_phone_code["phone"]
        capth = r.get(redis_shell)
        expect = {"code":"0"}
        url = r"https://api.yunshuxie.com/yunshuxie-passport-service/user/login"
        # PC登录
        params = {"userName": "13260062372","smsCode": capth, "type": "8"}
        string = urllib.urlencode(params)
        s = string + self.salt
        md = hashlib.md5()
        md.update(s)
        md5 = md.hexdigest()
        data = string + "&sign=" + md5
        self.resp = self.session.post(url, data=data)  # PC短信验证码登录
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        assert result["code"] == expect["code"], self.msg.format(Case=u"PC短信验证码登录",Except=expect["code"],
                                                                       Really=result["code"])
        # APP登录
        params = {"userName": "13260062372", "smsCode": capth, "type": "6"}
        string = urllib.urlencode(params)
        s = string + self.salt
        md = hashlib.md5()
        md.update(s)
        md5 = md.hexdigest()
        data = string + "&sign=" + md5
        self.resp = self.session.post(url, data=data)  # APP短信验证码登录
        print self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        assert result["code"] == expect["code"], self.msg.format(Case=u"APP短信验证码登录",Except=expect["code"],
                                                               Really=result["code"])
        # 微信登录
        params = {"userName": "13260062372", "smsCode": capth, "type": "7","wechatCode":"061Fz8no1PT6gj0chmno1E68no1Fz8nd"}
        string = urllib.urlencode(params)
        s = string + self.salt
        md = hashlib.md5()
        md.update(s)
        md5 = md.hexdigest()
        data = string + "&sign=" + md5
        self.resp = self.session.post(url, data=data)  # 微信短信验证码登录
        print self.resp.content
        result = json.loads(self.resp.content)
        assert result["code"] == expect["code"], self.msg.format(Case=u"微信短信验证码登录",Except=expect["code"],
                                                                        Really=result["code"])
    def test_03_user_login_error(self):
        """验证码错误
        :param: smsCode == 111111
        :return code == 101001"""
        url = r"https://api.yunshuxie.com/yunshuxie-passport-service/user/login"
        # PC登录
        params = {"userName": "13260062372", "smsCode": "111111", "type": "8"}  #错误的验证码
        string = urllib.urlencode(params)
        s = string + self.salt
        md = hashlib.md5()
        md.update(s)
        md5 = md.hexdigest()
        data = string + "&sign=" + md5
        self.resp = self.session.post(url, data=data)  # PC短信验证码登录
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        expect = {"code": "101001"}
        assert result["code"] == expect["code"], self.msg.format(Case=u"PC短信验证码登录", Except=expect["code"],
                                                                                Really=result["code"])
    def test_04_user_login_not_found(self):
        """用户不存在
        :param: userName == 1231234567
        :return: code == 201002
        """
        url = r"https://api.yunshuxie.com/yunshuxie-passport-service/user/login"
        # PC登录
        params = {"userName": "1231234567", "smsCode": "111111", "type": "8"}  # 错误的验证码
        string = urllib.urlencode(params)
        s = string + self.salt
        md = hashlib.md5()
        md.update(s)
        md5 = md.hexdigest()
        data = string + "&sign=" + md5
        self.resp = self.session.post(url, data=data)  # PC短信验证码登录
        print self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        expect = {"code": "201002"}
        assert result["code"] == expect["code"], self.msg.format(Case=u"PC短信验证码登录", Except=expect["code"],
                                                                 Really=result["code"])
    def test_05_user_login_pwd_error(self):
        """用户不存在
        :param: userName == 13260062372
        :return: code == 201003
        """
        url = r"https://api.yunshuxie.com/yunshuxie-passport-service/user/login"
        # PC登录
        params = {"userName": "13260062372", "pwd": "1111111", "type": "1"}  # 错误的验证码
        string = urllib.urlencode(params)
        s = string + self.salt
        md = hashlib.md5()
        md.update(s)
        md5 = md.hexdigest()
        data = string + "&sign=" + md5
        self.resp = self.session.post(url, data=data)  # PC短信验证码登录
        print self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        expect = {"code": "201003"}
        assert result["code"] == expect["code"], self.msg.format(Case=u"PC短信验证码登录", Except=expect["code"],
                                                                 Really=result["code"])


    @classmethod
    def tearDown(self):
        pass
if __name__ == "__main__":
    unittest.main()