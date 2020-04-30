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
        self.msg = u"""\n   {Case}     Except:  {Except}-*-\n        Really:  {Really}"""  # 校验HTTP返回代码
        # self.redis_host = s.get_env("beta").split(":") if env_flag == "beta" else s.get_env("prod_stage").split(":")
        r = redis.Redis(host="172.17.1.44", port=6379, password="yunshuxie1029Password")
        self.captcha = "111111"
        params_get_phone_code = {"platform": "0", "phone": "13260062372", "verType": "2"}  # 1登录 ;2修改手机号

        redis_shell = "code_" + params_get_phone_code["verType"] + "_" + params_get_phone_code["phone"]
        r.set(redis_shell, self.captcha)  # 设置验证码 111111
        r.expire(redis_shell, "30")  # 设置失效时间
        login_url = r"https://api.yunshuxie.com/yunshuxie-passport-service/user/login"
        # PC登录
        params = {"userName": "13260062372", "smsCode": self.captcha, "type": "8"}
        string = urllib.urlencode(params)
        s = string + self.salt
        md = hashlib.md5()
        md.update(s)
        md5 = md.hexdigest()
        data = string + "&sign=" + md5
        self.resp = self.session.post(login_url, data=data)  # PC短信验证码登录
        self.login = json.loads(self.resp.content, encoding="utf8")
    def test_01_user_info(self):
        """phone,memberId查询用户信息
        :param: userName = 13260062372
        :param: capth = 111111
        :return code == 0
            """
        expect = {"code": "0"}
        memberId = self.login["data"]["memberId"]
        phone = self.login["data"]["phone"]
        url = r"https://api.yunshuxie.com/yunshuxie-passport-service/user/user_info"
        params = {"memberId":memberId,"phone":phone}
        string = urllib.urlencode(params)
        s = string + self.salt
        md = hashlib.md5()
        md.update(s)
        md5 = md.hexdigest()
        data = string + "&sign=" + md5
        self.resp = self.session.post(url, data=data)  # PC短信验证码登录
        print self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        assert result["code"] == expect["code"], self.msg.format(Case=u"用户信息查询", Except=expect["code"],
                                                                 Really=result["code"])
    def test_02_user_modify_phone(self):
        expect = {"code": "0"}
        memberId = self.login["data"]["memberId"]
        url = r"https://api.yunshuxie.com/yunshuxie-passport-service/user/modify_phone"
        params = {"memberId": memberId, "newPhone": "1812343143","verificationCode":self.captcha}
        string = urllib.urlencode(params)
        s = string + self.salt
        md = hashlib.md5()
        md.update(s)
        md5 = md.hexdigest()
        data = string + "&sign=" + md5
        self.resp = self.session.post(url, data=data)  # PC短信验证码登录
        print self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        assert result["code"] == expect["code"], self.msg.format(Case=u"修改手机号", Except=expect["code"],
                                                                 Really=result["code"])

    @classmethod
    def tearDown(self):
        pass
if __name__ == "__main__":
    unittest.main()