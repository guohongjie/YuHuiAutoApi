#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import unittest
import json
import redis
from requests_toolbelt import MultipartEncoder
from app.base.pythonProject.base.log import TestLog,fengefu,lianjiefu
from app.base.pythonProject.base.getConfig import ReadConfig
from app.base.pythonProject.base.getCookies import get_ysx_crm_cookie,get_wacc_admin_cookie
logging = TestLog().getlog()
class Ysx_Make_User(unittest.TestCase):
    """短信服务"""
    @classmethod
    def setUpClass(self):
        """起始方法
        #:return:  cookies """
        s = ReadConfig()
        self.admin_pwd = s.get_admin("pwd")
        self.admin_usernmae = s.get_admin("username")
        self.redis = redis.Redis(host="localhost",port=6379)
        self.env_flag = self.redis.get("make_user_env_flag")
        self.env_num = self.redis.get("make_user_env_num")
        self.phoneNumList = self.redis.get("make_user_phones")
        self.employeeTypes = self.redis.get("make_user_employeetypes")
        self.userNames = ",".join(["测试_"+userName for userName in self.phoneNumList.split(",")])
        self.session = requests.Session()
        request_retry = requests.adapters.HTTPAdapter(max_retries=3)
        self.session.mount("https://", request_retry)
        self.session.mount("http://", request_retry)
        cookie_dict = {'env_flag':self.env_flag,"env_num":self.env_num}  #设置环境号
        #cookie_dict = {'env_flag':"beta","env_num":"2"}  #设置环境号
        cookies = requests.utils.cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True)
        self.session.cookies = cookies
        self.header = {"User-Agent":
                           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
                       "Accept": "application/json, text/javascript, */*; q=0.01",
                       "Accept-Encoding": "gzip, deflate, br",
                       "Accept-Language": "zh-CN,zh;q=0.9",
                       "Connection": "keep-alive"
            ,"Host": "admin.yunshuxie.com","Upgrade-Insecure-Requests": "1"}
        self.session.headers = self.header
        self.salt = "mengmengda"
        self.msg = """\n        Expect:  {Expect}-*-\n        Really:  {Really}"""  # 校验HTTP返回代码
    def test_01_make_user(self):
        """make_user_admin平台创建测试用户
        """
        resp_cookies = get_wacc_admin_cookie(self.env_flag,self.env_num)
        if resp_cookies['code'] != 200:
            raise Exception,"登录失败,请检查admin登录配置!"
        else:
            url = r"https://admin.yunshuxie.com/v1/admin/account/add/user.json"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","X-Requested-With": "XMLHttpRequest","Accept": "application/json, text/javascript, */*; q=0.01","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9","Cache-Control": "no-cache","Connection": "keep-alive","Content-Type": "multipart/form-data; boundary=----WebKitFormBoundaryF7Lcp4O5PcTcLugw"}
            userName = ["测试_"+userName for userName in self.phoneNumList.split(",")]
            userPhone = self.phoneNumList.split(",")
            employeeTypes = self.employeeTypes.split(",")
            for index in range(len(userName)):
                datas = {"memberIcon": "", "pwd": "test123456",
                         "email": "automation@yunshuxie.com", "weiboName": "",
                         "nickName": userName[index], "qq": "",
                         "interest": "", "phone":userPhone[index] , "weichatNum": "",
                         "remark": "自动化测试",
                         "memberType": employeeTypes[index],
                         "ChoiceOfTeacher": "默认分组",
                         "ChoiceOfTeacher": "默认分组",
                         "readRole": "0", "ChoiceOfTeacher": "云舒写教育科技",
                         "button": ""}
                data = MultipartEncoder(datas)
                headers["Content-Type"] = data.content_type
                self.session.headers = headers
                logging.info(url + lianjiefu + json.dumps(datas,ensure_ascii=False) + fengefu)
                str_params = json.dumps(datas,ensure_ascii=False,encoding="utf8")
                print str_params
                self.resp = self.session.post(url, data=data)
                print self.resp.content
                logging.info(url + lianjiefu + self.resp.text + fengefu)
                result = json.loads(self.resp.content)
                assert result["returnCode"] == "0",self.msg.format(Expect="0",Really=result["returnCode"])
    def test_02_add_TestUser(self):
        """make_user_CRM平台备注测试用户
        """
        url = r"https://admin.crm.yunshuxie.com/test/account/management/insert/test/account"
        resp_cookies = get_ysx_crm_cookie(self.env_flag,self.env_num)
        headers = {"Accept": "application/json, text/javascript, */*; q=0.01","Accept-Encoding": "gzip, deflate","Accept-Language": "zh-CN,zh;q=0.9","Cache-Control": "no-cache","Connection": "keep-alive","Content-Type": "application/x-www-form-urlencoded; charset=UTF-8","Pragma": "no-cache","Referer": "http://admin.crm.yunshuxie.com/test/account/management/goto/insert/test/account","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","X-Requested-With": "XMLHttpRequest"}
        self.session.headers = headers
        if resp_cookies['code'] != 200:
            raise Exception,"登录失败,请检查登录配置"
        else:
            self.session.cookies = resp_cookies["cookies"]
            for phone in self.phoneNumList.split(","):
                data = {"phones": phone ,"userNames": "测试_{phone}".format(phone=phone),"employeeTypes": 0}
                str_params = json.dumps(data, ensure_ascii=False, encoding="utf8")
                print str_params
                logging.info(url + lianjiefu + json.dumps(data,ensure_ascii=False) + fengefu)
                self.resp = self.session.post(url, data=data)
                print self.resp.content
                logging.info(url + lianjiefu + self.resp.text + fengefu)
                result = json.loads(self.resp.content)
                assert result["returnCode"] == 0,self.msg.format(Expect="0",Really=result["returnCode"])
    @classmethod
    def tearDownClass(self):
        """测试结束后执行,断言Req==Resp
        :return:  True OR False"""
        del self.redis
if __name__ == "__main__":
    unittest.main()