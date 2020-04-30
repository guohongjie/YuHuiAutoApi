#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import unittest
import json
import hashlib
import redis
import urllib
from app.base.pythonProject.base.log import TestLog,fengefu,lianjiefu
from app.base.pythonProject.base.getConfig import ReadConfig
from app.base.pythonProject.base.py_redis import MyRedis
logging = TestLog().getlog()
class Ysx_Message_Service(unittest.TestCase):
    """短信服务"""
    @classmethod
    def setUpClass(self):
        """起始方法
        #:return:  cookies """
        s = ReadConfig()
        redis = MyRedis()
        env_flag = redis.str_get("yunshuxie_message_provider_env_flag")
        env_num = redis.str_get("yunshuxie_message_provider_env_num")
        self.redis_host = s.get_env("beta").split(":") if env_flag == "beta" else s.get_env("prod_stage").split(":")
        logging.info("self.redis_host :"+self.redis_host[0]+self.redis_host[1])
        self.session = requests.Session()
        request_retry = requests.adapters.HTTPAdapter(max_retries=3)
        self.session.mount("https://", request_retry)
        self.session.mount("http://", request_retry)
        cookie_dict = {'env_flag':env_flag,"env_num":env_num}  #设置环境号
        #cookie_dict = {'env_flag':env_flag,"env_num":env_num}  #设置环境号
        cookies = requests.utils.cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True)
        self.session.cookies = cookies
        self.header = {"Connection":"keep-alive"
        ,"Content-Type": "application/x-www-form-urlencoded",
          "Cache-Control":"no-cache",
          "User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 Safari/601.1 wechatdevtools/1.02.1904090 MicroMessenger/6.7.3 Language/zh_CN webview/15578306374265793 webdebugger port/22562"}
        self.session.headers = self.header
        self.salt = "mengmengda"
        self.msg = """\n        Expect:  {Expect}-*-\n        Really:  {Really}"""  # 校验HTTP返回代码
    def test_01_get_phone_code(self):
        """sms/get_phone_code_蓝创加入黑名单_阿里云平台发送短信<br/>https://api.yunshuxie.com/yunshuxie-message-service/sms/get_phone_code<br/>
        :param phone==18515850273
        :param verType==4
        :param platform==0
        :return code==0
        """
        url = r"https://api.yunshuxie.com/yunshuxie-message-service/sms/get_phone_code"
        params_get_phone_code = {"platform": "0", "phone": "18515850273", "verType": "4"}
        string = urllib.urlencode(params_get_phone_code)
        s = string + self.salt
        logging.info(url + lianjiefu + s + fengefu)
        md = hashlib.md5()
        md.update(s)
        md5 = md.hexdigest()
        data = string + "&sign=" + md5
        logging.info(url + lianjiefu + data + fengefu)
        print data
        self.resp = self.session.post(url, data=data)
        print self.resp.content
        logging.info(url + lianjiefu + self.resp.text +fengefu )
        dict_resp = json.loads(self.resp.content,encoding="utf8")
        expect = {u"message":u"操作成功",u"ts":u"1557918661013",u"data":{},u"code":u"0"}
        assert dict_resp[u"code"]==expect[u"code"],self.msg.format(Expect=expect[u"code"],Really=dict_resp[u"code"])
        assert dict_resp[u"message"]==expect[u"message"],self.msg.format(Expect=expect[u"message"],Really=dict_resp[u"message"])
    def test_01_get_phone_code(self):
        """sms / get_phone_code_注册<br/>https://api.yunshuxie.com/yunshuxie-message-service/sms/get_phone_code<br/>
        :param phone==13260062372
        :param platform==0
        :param verType==0
        :return code==0
        """
        url = r"https://api.yunshuxie.com/yunshuxie-message-service/sms/get_phone_code"
        params_get_phone_code = {"platform": "0", "phone": "18519118952", "verType": "0"}
        string = urllib.urlencode(params_get_phone_code)
        s = string + self.salt
        logging.info(url + lianjiefu + s + fengefu)
        md = hashlib.md5()
        md.update(s)
        md5 = md.hexdigest()
        data = string + "&sign=" + md5
        logging.info(url + lianjiefu + data + fengefu)
        print data
        self.resp = self.session.post(url, data=data)
        print self.resp.content
        logging.info(url + lianjiefu + self.resp.text +fengefu )
        dict_resp = json.loads(self.resp.content, encoding="utf8")
        expect = {u"message": u"操作成功", u"ts": u"1557918661013", u"data": {}, u"code": u"0"}
        assert dict_resp[u"code"] == expect[u"code"],self.msg.format(Expect=expect[u"code"],Really=dict_resp[u"code"])
        assert dict_resp[u"message"] == expect[u"message"],self.msg.format(Expect=expect[u"message"],Really=dict_resp[u"message"])
    def test_02_get_phone_code(self):
        """sms / get_phone_code_登录<br/>https://api.yunshuxie.com/yunshuxie-message-service/sms/get_phone_code<br/>
        :param phone==13260062372
        :param platform==0
        :param verType==1
        :return code==0
        """
        url = r"https://api.yunshuxie.com/yunshuxie-message-service/sms/get_phone_code"
        params_get_phone_code = {"platform": "0", "phone": "18515850273", "verType": "1"}
        string = urllib.urlencode(params_get_phone_code)
        s = string + self.salt
        logging.info(url + lianjiefu + s + fengefu)
        md = hashlib.md5()
        md.update(s)
        md5 = md.hexdigest()
        data = string + "&sign=" + md5
        logging.info(url + lianjiefu + data + fengefu)
        print data
        self.resp = self.session.post(url, data=data)
        print self.resp.content
        logging.info(url + lianjiefu + self.resp.text +fengefu )
        dict_resp = json.loads(self.resp.content, encoding="utf8")
        expect = {u"message": u"操作成功", u"ts": u"1557918661013", u"data": {}, u"code": u"0"}
        assert dict_resp[u"code"] == expect[u"code"],self.msg.format(Expect=expect[u"code"],Really=dict_resp[u"code"])
        assert dict_resp[u"message"] == expect[u"message"],self.msg.format(Expect=expect[u"message"],Really=dict_resp[u"message"])
    def test_03_get_phone_code(self):
        """sms / get_phone_code_订单<br/>https://api.yunshuxie.com/yunshuxie-message-service/sms/get_phone_code<br/>
        :param phone==13260062372
        :param platform==0
        :param verType==4
        :return code==0
        """
        url = r"https://api.yunshuxie.com/yunshuxie-message-service/sms/get_phone_code"
        params_get_phone_code = {"platform": "0", "phone": "13260062372", "verType": "4"}
        string = urllib.urlencode(params_get_phone_code)
        s = string + self.salt
        logging.info(url + lianjiefu + s + fengefu)
        md = hashlib.md5()
        md.update(s)
        md5 = md.hexdigest()
        data = string + "&sign=" + md5
        logging.info(url + lianjiefu + data + fengefu)
        print data
        self.resp = self.session.post(url, data=data)
        print self.resp.content
        logging.info(url + lianjiefu + self.resp.text +fengefu )
        dict_resp = json.loads(self.resp.content, encoding="utf8")
        expect = {u"message": u"操作成功", u"ts": u"1557918661013", u"data": {}, u"code": u"0"}
        assert dict_resp[u"code"] == expect[u"code"],self.msg.format(Expect=expect[u"code"],Really=dict_resp[u"code"])
        assert dict_resp[u"message"] == expect[u"message"],self.msg.format(Expect=expect[u"message"],Really=dict_resp[u"message"])
    def test_04_get_phone_code(self):
        """sms / get_phone_code_手机号格式错误<br/>https://api.yunshuxie.com/yunshuxie-message-service/sms/get_phone_code<br/>
        :param phone==132600623721123
        :param platform==0
        :param verType==4
        :return code==102001
        """
        url = r"https://api.yunshuxie.com/yunshuxie-message-service/sms/get_phone_code"
        params_get_phone_code = {"platform": "0", "phone": "132600623721123", "verType": "4"}
        string = urllib.urlencode(params_get_phone_code)
        s = string + self.salt
        logging.info(url + lianjiefu + s + fengefu)
        md = hashlib.md5()
        md.update(s)
        md5 = md.hexdigest()
        data = string + "&sign=" + md5
        logging.info(url + lianjiefu + data + fengefu)
        print data
        self.resp = self.session.post(url, data=data)
        print self.resp.content
        logging.info(url + lianjiefu + self.resp.text +fengefu )
        dict_resp = json.loads(self.resp.content, encoding="utf8")
        expect = {u"message":u"手机号码格式错误",u"ts":u"1557972149616",u"data":{},u"code":u"102001"}
        assert dict_resp[u"code"] == expect[u"code"],self.msg.format(Expect=expect[u"code"],Really=dict_resp[u"code"])
        assert dict_resp[u"message"] == expect[u"message"],self.msg.format(Expect=expect[u"message"],Really=dict_resp[u"message"])
    def test_05_get_phone_code(self):
        """sms / get_phone_code_系统异常<br/>https://api.yunshuxie.com/yunshuxie-message-service/sms/get_phone_code<br/>
        :param  platform==5
        :param  verType==8
        :return code==-1
        """
        url = r"https://api.yunshuxie.com/yunshuxie-message-service/sms/get_phone_code"
        params_get_phone_code = {"platform": "5", "phone": "13260062372", "verType": "8"}
        string = urllib.urlencode(params_get_phone_code)
        s = string + self.salt
        logging.info(url + lianjiefu + s + fengefu)
        md = hashlib.md5()
        md.update(s)
        md5 = md.hexdigest()
        data = string + "&sign=" + md5
        logging.info(url + lianjiefu + data + fengefu)
        print data
        self.resp = self.session.post(url, data=data)
        print self.resp.content
        logging.info(url + lianjiefu + self.resp.text +fengefu )
        dict_resp = json.loads(self.resp.content, encoding="utf8")
        expect = {u"message":u"系统异常",u"ts":u"1557973747744",u"data":{},u"code":u"-1"}
        assert dict_resp[u"code"] == expect[u"code"],self.msg.format(Expect=expect[u"code"],Really=dict_resp[u"code"])
        assert dict_resp[u"message"] == expect[u"message"],self.msg.format(Expect=expect[u"message"],Really=dict_resp[u"message"])
    def test_06_send_batch_message(self):
        """sms / send_batch_message_批量发送短信<br/>https://api.yunshuxie.com/yunshuxie-message-service/sms/send_batch_message<br/>
        :param phones=="13260062372,18515850273,178"
        :param contentType==1
        :param platform==0
        :param idiograph==云舒写
        :return code==0
        """
        url = r"https://api.yunshuxie.com/yunshuxie-message-service/sms/send_batch_message"
        params = {"contentType":"1","content":"打开短信，你会看到惊喜，献给正在工作的你！-致：我最爱的你(^o^)！",
                  "phones":"{phone1},{phone2},178".format(phone1="13260062372",phone2="18515850273"),"platform":"0",
                 "idiograph ":"云舒写"}#"云舒写"}#,"msgTemplate":"","msgVars":""}
        string = urllib.urlencode(params)
        s = string+self.salt
        logging.info(url + lianjiefu + s + fengefu)
        md = hashlib.md5()
        md.update(s)
        md5 = md.hexdigest()
        data = string+"&sign="+md5
        logging.info(url + lianjiefu + data + fengefu)
        print data
        self.resp = self.session.post(url,data=data)
        print self.resp.content
        logging.info(url + lianjiefu + self.resp.text +fengefu )
        dict_resp = json.loads(self.resp.content, encoding="utf8")
        expect = {u"message":u"操作成功",u"ts":u"1557991054584",u"data":{},u"code":u"0"}
        assert dict_resp[u"code"] == expect[u"code"],self.msg.format(Expect=expect[u"code"],Really=dict_resp[u"code"])
        assert dict_resp[u"message"] == expect[u"message"],self.msg.format(Expect=expect[u"message"],Really=dict_resp[u"message"])
    def test_07_send_message(self):
        """sms / send_message_发送单条短信<br/>https://api.yunshuxie.com/yunshuxie-message-service/sms/send_message<br/>
        :param phone==13260062372
        :param platform==0
        :param idiograph==云舒写
        :return code==0
        """
        url = r"https://api.yunshuxie.com/yunshuxie-message-service/sms/send_message"
        params = {"phone":"13260062372","content":"打开短信，你会看到惊喜，献给正在工作的你！-致：我最爱的你(^o^)！",
                  "platform":"0","idiograph":"云舒写"}
        string = urllib.urlencode(params)
        s = string + self.salt
        logging.info(url + lianjiefu + string + fengefu)
        md = hashlib.md5()
        md.update(s)
        md5 = md.hexdigest()
        data = string+"&sign="+md5
        logging.info(url + lianjiefu + data + fengefu)
        print data
        self.resp = self.session.post(url,data=data)
        print self.resp.content
        logging.info(url + lianjiefu + self.resp.text +fengefu )
        dict_resp = json.loads(self.resp.content, encoding="utf8")
        expect = {u"message": u"操作成功", u"ts": u"1557918661013", u"data": {}, u"code": u"0"}
        assert dict_resp[u"code"] == expect[u"code"],self.msg.format(Expect=expect[u"code"],Really=dict_resp[u"code"])
        assert dict_resp[u"message"] == expect[u"message"],self.msg.format(Expect=expect[u"message"],Really=dict_resp[u"message"])
    def test_08_vercode_check(self):
        """sms / vercode_check_验证码错误<br/>https://api.yunshuxie.com/yunshuxie-message-service/sms/vercode_check<br/>
        :param phone==13260062372
        :param verType==0
        :param code=="1234"
        :return code==101001
        """
        url = r"https://api.yunshuxie.com/yunshuxie-message-service/sms/vercode_check"
        params = {"phone": "13260062372", "verType": 0, "code": "1234"}
        string = urllib.urlencode(params)
        s = string + self.salt
        logging.info(url + lianjiefu + s + fengefu)
        md = hashlib.md5()
        md.update(s)
        md5 = md.hexdigest()
        data = string + "&sign=" + md5
        logging.info(url + lianjiefu + data + fengefu)
        print data
        self.resp = self.session.post(url, data=data)
        print self.resp.content
        logging.info(url + lianjiefu + self.resp.text +fengefu )
        dict_resp = json.loads(self.resp.content, encoding="utf8")
        expect = {u"message":u"验证码错误",u"ts":u"1557992688917",u"data":{},u"code":u"101001"}
        assert dict_resp[u"code"] == expect[u"code"],self.msg.format(Expect=expect[u"code"],Really=dict_resp[u"code"])
        assert dict_resp[u"message"] == expect[u"message"],self.msg.format(Expect=expect[u"message"],Really=dict_resp[u"message"])
    def test_09_vercode_check(self):
        """sms / vercode_check_校验验证码<br/>https://api.yunshuxie.com/yunshuxie-message-service/sms/get_phone_code<br/>
        :param phone==13260062372
        :param code==redis获取
        :param verType==0
        :return code==0
        """
        url = r"https://api.yunshuxie.com/yunshuxie-message-service/sms/get_phone_code"
        params_get_phone_code = {"platform": "0", "phone": "18519118952", "verType": "3"}
        string = urllib.urlencode(params_get_phone_code)
        s = string + self.salt
        logging.info(url + lianjiefu + s + fengefu)
        md = hashlib.md5()
        md.update(s)
        md5 = md.hexdigest()
        data = string + "&sign=" + md5
        logging.info(url + lianjiefu + data + fengefu)
        print data
        self.resp = self.session.post(url, data=data)
        print self.resp.content
        dict_resp = json.loads(self.resp.content, encoding="utf8")
        expect = {u"message": u"操作成功", u"ts": u"1557918661013", u"data": {}, u"code": u"0"}
        assert dict_resp[u"code"] == expect[u"code"], self.msg.format(Expect=expect[u"code"], Really=dict_resp[u"code"])
        assert dict_resp[u"message"] == expect[u"message"], self.msg.format(Expect=expect[u"message"],
                                                                            Really=dict_resp[u"message"])
        logging.info(url + lianjiefu + self.resp.text +fengefu )
        r = redis.Redis(host=self.redis_host[0], port=int(self.redis_host[1]), password="yunshuxie1029Password")
        redis_shell= "code_"+params_get_phone_code["verType"]+"_"+params_get_phone_code["phone"]
      #  redis_shell= "code_"+str(params_get_phone_code["verType"])+"_"+params_get_phone_code["phone"]
        logging.info(url + lianjiefu + redis_shell + fengefu)
        capth = r.get(redis_shell)
        url = r"https://api.yunshuxie.com/yunshuxie-message-service/sms/vercode_check"
        params = {"phone":params_get_phone_code["phone"],"verType":params_get_phone_code["verType"],"code": capth}  #错误验证码
        string = urllib.urlencode(params)
        s = string + self.salt
        logging.info(url + lianjiefu + s + fengefu)
        md = hashlib.md5()
        md.update(s)
        md5 = md.hexdigest()
        data = string + "&sign=" + md5
        logging.info(url + lianjiefu + data + fengefu)
        self.resp = self.session.post(url, data=data)
        print self.resp.content
        logging.info(url + lianjiefu + self.resp.text +fengefu )
        dict_resp = json.loads(self.resp.content, encoding="utf8")
        #print capth
        #print self.resp.content
        expect = {u"message": u"操作成功", u"ts": u"1557918661013", u"data": {}, u"code": u"0"}
        assert dict_resp[u"code"] == expect[u"code"],self.msg.format(Expect=expect[u"code"],Really=dict_resp[u"code"])
        assert dict_resp[u"message"] == expect[u"message"],self.msg.format(Expect=expect[u"message"],Really=dict_resp[u"message"])
    @classmethod
    def tearDownClass(self):
        """测试结束后执行,断言Req==Resp
        :return:  True OR False"""
        pass
if __name__ == "__main__":
    unittest.main()