#!/usr/bin/python
#-*-coding:utf-8-*-
import requests
import unittest
#!/usr/bin/python
#-*-coding:utf-8 -*-
import unittest
import re
import json
from requests import Session,Request
from getCookies import *
from py_redis import MyRedis
# from log import TestLog,fengefu,lianjiefu
# from getConfig import ReadConfig
# logging = TestLog().getlog()
get_cookie = 0
DATA,PARAMS = 0,0
headers = 0
class sheetName_Test(unittest.TestCase):
    #"{{sheetName}}"
    @classmethod
    def setUpClass(self):
        self.redis = MyRedis()
        env_flag = self.redis.str_get("wacc_home_env_flag")  #{{project}}
        env_num = self.redis.str_get("wacc_home_env_num")  #{{project}}
        get_dict_cookies = get_cookies("wacc_home",env_flag,env_num)  #{{project}}
        str_cookies = json.dumps(get_dict_cookies,encoding="utf8",ensure_ascii=False)
        self.redis.str_set("str_cookies",str_cookies)  #cookie存至redis
    # def test_01_test(self):
    #     dict_cookies = json.loads(self.redis.str_get("str_cookies"),encoding="utf8")
    #     self.session.cookies = requests.utils.cookiejar_from_dict(dict_cookies, cookiejar=None, overwrite=True)
    #    # print self.session.cookies
    #     header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","Accept": "application/json, text/javascript, */*; q=0.01","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9","Connection": "keep-alive","Host": "www.yunshuxie.com","Upgrade-Insecure-Requests": "1"}
    def test_order_apiNameEN(self):
        """{{caseDesc}}<br/>{{apiHost}}{{apiUrl}}<br/>"""
        dict_cookies = json.loads(self.redis.str_get("str_cookies"), encoding="utf8")
        data = DATA  #{{DATA}}
        url = "{{apiHost}}" + "{{apiUrl}}"
        caseHeaders = headers  #{{HEADERS}}
        #str_params = json.dumps(data, ensure_ascii=False, encoding="utf8")
        resp = requests.post(url=url, data=data, headers=caseHeaders, cookies=dict_cookies)
        str_cookies = json.dumps(resp.cookies.get_dict(),encoding="utf8",ensure_ascii=False)
        self.redis.str_set("str_cookies",str_cookies)  #更新cookie存至redis
    def test_order_apiNameEN(self):
        """{{caseDesc}}<br/>{{apiHost}}{{apiUrl}}<br/>"""
        dict_cookies = json.loads(self.redis.str_get("str_cookies"), encoding="utf8")
        params = PARAMS  #{{PARAMS}}
        url = "{{apiHost}}" + "{{apiUrl}}"
        caseHeaders = headers  #{{HEADERS}}
        #str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        resp = requests.get(url=url, params=params, headers=caseHeaders, cookies=dict_cookies)
        str_cookies = json.dumps(resp.cookies.get_dict(),encoding="utf8",ensure_ascii=False)
        self.redis.str_set("str_cookies",str_cookies)  #cookie存至redis
        #{{valueTrainsmit}}


    @classmethod
    def tearDownClass(self):
        pass


if __name__ == "__main__":
    unittest.main()
