#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import unittest
import re
import json
from app.base.pythonProject.base.log import TestLog,fengefu,lianjiefu
from app.base.pythonProject.base.py_redis import MyRedis
logging = TestLog().getlog()
globals_values = ""
class XieZuoXiTongKe_Test(unittest.TestCase):
    """<br/>写作系统课->查询课程信息->查询活动是否发起-><br/>课程购买查询->个人购买全期课程"""
    @classmethod
    def setUpClass(self):
        redis = MyRedis()
        self.env_flag = redis.str_get("wacc_order_env_flag")
        self.env_num = redis.str_get("wacc_order_env_num")
        self.phonenum = redis.str_get("make_user_phones")
        self.session = requests.Session()
        request_retry = requests.adapters.HTTPAdapter(max_retries=3)
        self.session.mount("https://", request_retry)
        self.session.mount("http://", request_retry)
        header = {"Connection": "keep-alive", "Content-Type": "application/x-www-form-urlencoded",
                  "Cache-Control": "no-cache",
                  "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 Safari/601.1 wechatdevtools/1.02.1904090 MicroMessenger/6.7.3 Language/zh_CN webview/15578306374265793 webdebugger port/22562"}
        self.session.headers = header
        cookies = {"env_flag": self.env_flag, "env_num": self.env_num}
        self.session.cookies = requests.utils.cookiejar_from_dict(cookies)
        self.pattern = "{\"global.*}"
        self.msg = """\n        Expect:  {Expect}-*-\n        Really:  {Really}"""  # 校验HTTP返回代码
        globals()["globals_values"] = ""
    def test_01_query_activity(self):
        """https://pay.yunshuxie.com/v6/order/special/experience/activity.htm<br/>{"activityId":"3024","memberCourseType":"2","callback":"Zepto1560236625603"}"""
        url = r"https://pay.yunshuxie.com/v6/order/special/experience/activity.htm"
        params = {"activityId":"3024","memberCourseType":"2","callback":"Zepto1560236625603"}
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        resp = self.session.get(url=url,params=params)
        logging.info(url + lianjiefu + resp.text + fengefu)
        print "月课程查询:" + resp.content + "<br/>"
        result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
        assert result["returnCode"] == "0", self.msg.format(Expect="0", Really=result["returnCode"])
    def test_02_check_course_valid(self):
        """https://pay.yunshuxie.com/v6/order/check/course/valid.htm<br/>{"memberCourseType":"2","sk":"null","callback":"Zepto1560239495394"}"""
        url = r"https://pay.yunshuxie.com/v6/order/check/course/valid.htm"
        params = {"memberCourseType":"2","sk":"null","callback":"Zepto1560239495394"}
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        resp = self.session.get(url=url,params=params)
        logging.info(url + lianjiefu + resp.text + fengefu)
        print "活动查询:" + resp.content + "<br/>"
        result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
        if result["returnCode"] == "15":
            assert result["returnCode"] == "15", self.msg.format(Expect="0", Really=result["returnCode"])
        else: #活动开启
            assert result["returnCode"] == "0", self.msg.format(Expect="0", Really=result["returnCode"])
    def test_03_order_check_newStu(self):
        """https://pay.yunshuxie.com/v6/order/check/newStu.htm<br/>{"callback":"jQuery22409106770349628588_1560240210128","phone":self.phonenum,<br/>"memberCourseType":"1"}"""
        url = r"https://pay.yunshuxie.com/v6/order/check/newStu.htm"
        params = {"callback":"jQuery22409106770349628588_1560240210128","phone":self.phonenum,"memberCourseType":"2"}
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        resp = self.session.get(url=url,params=params)
        logging.info(url + lianjiefu + resp.text + fengefu)
        print "查看用户是否购买课程:" + resp.content + "<br/>"
        result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
        assert result["returnCode"] == "0", self.msg.format(Expect="0", Really=result["returnCode"])
    def test_04_get_member_standard_detailv(self): #获得课程信息 productHoursId productId
        """https://wap.yunshuxie.com/v1/member_standard_product/get_member_standard_detailv2.json<br/>{"memberCourseType":"1","type":"1","memberGrade":"1","week":"7",<br/>"phone":"18519118952","callback":"__jp0"}"""
        url = r"https://wap.yunshuxie.com/v1/member_standard_product/get_member_standard_detailv2.json"
        params = {"memberCourseType":"2","type":"1","memberGrade":"3","phone":self.phonenum,"callback":"__jp0"}
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        resp = self.session.get(url=url,params=params)
        logging.info(url + lianjiefu + resp.text + fengefu)
        print "半年课程查询:" + resp.content + "<br/>"
        result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
        assert result["returnCode"] == "0", self.msg.format(Expect="0", Really=result["returnCode"])
        values =[[course["productHoursId"],course["productId"]] for course in result["data"]["courseList"]]
        globals()["globals_values"] = values
    def test_05_order_param(self):  # 获得订单参数 productHoursId productId
        """https://pay.yunshuxie.com/v6/order/order_param.htm<br/>{"memberCourseType":"1","type":"1","memberGrade":"1","week":"7",<br/>"phone":"18519118952","callback":"__jp0"}"""
        url = r"https://pay.yunshuxie.com/v6/order/order_param.htm"
        for productHoursId,productId in globals_values:
            params = {"memberCourseType":"2","type":"1","phIds":productHoursId,"memberGrade":"3","phone":self.phonenum,"callback":"__jp0"}
            str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
            print str_params
            resp = self.session.get(url=url, params=params)
            logging.info(url + lianjiefu + resp.text + fengefu)
            print "订单参数:" + resp.content + "<br/>"
            result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
            assert result["returnCode"] == "0", self.msg.format(Expect="0", Really=result["returnCode"])
    def test_06_order_create2_AliPay(self):  # 获得订单参数 productHoursId productId
        """https://pay.yunshuxie.com/v6/order/create2.htm<br/>{"phone":self.phonenum,"pIds":productId,"phIds":productHoursId,"pType":"1",<br/>"productType":"1","memberCourseType":"1","type":"1","memberGrade":"1",<br/>"sk":"","cSn":"","addressId":"-1","activityId":"-1",<br/>"customizeGroupId":"-1","channelId":"AliPay"}"""
        url = r"https://pay.yunshuxie.com/v6/order/create2.htm"
        for productHoursId,productId in globals_values:
            params = {"phone": self.phonenum, "pIds": productId, "phIds": productHoursId, "pType": "1", "productType": "1",
                      "memberCourseType": "2","type": "1", "memberGrade": "3", "sk": "", "cSn": "", "addressId": "-1", "activityId": "-1",
                      "customizeGroupId": "-1", "channelId": "AliPay"}
            str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
            print str_params
            resp = self.session.get(url=url, params=params)
            print "生成订单:" + resp.content + "<br/>"
            logging.info(url + lianjiefu + resp.text + fengefu)
            result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
            assert result["returnCode"] == "0", self.msg.format(Expect="0", Really=result["returnCode"])
    def test_07_order_create2_WxPay(self):  # 获得订单参数 productHoursId productId
        """https://pay.yunshuxie.com/v6/order/create2.htm<br/>{"phone":self.phonenum,"pIds":productId,"phIds":productHoursId,"pType":"1",<br/>"productType":"1","memberCourseType":"1","type":"1","memberGrade":"1",<br/>"sk":"","cSn":"","addressId":"-1","activityId":"-1",<br/>"customizeGroupId":"-1","channelId":"WxPay"}"""
        url = r"https://pay.yunshuxie.com/v6/order/create2.htm"
        for productHoursId,productId in globals_values:
            params = {"phone":self.phonenum,"pIds":productId,"phIds":productHoursId,"pType":"1",
                      "productType":"1","memberCourseType":"2","type":"1",
                      "memberGrade":"3","code":"021ZaJtG17hM310SblvG1NZutG1ZaJtQ",
                      "sk":"","cSn":"","addressId":"-1","activityId":"3024","customizeGroupId":"-1","channelId":"WxPay"}
            str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
            print str_params
            resp = self.session.get(url=url, params=params)
            print "生成订单:" + resp.content + "<br/>"
            logging.info(url + lianjiefu + resp.text + fengefu)
            result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
            assert result["returnCode"] == "0", self.msg.format(Expect="0", Really=result["returnCode"])
    @classmethod
    def tearDownClass(self):
        globals().pop("globals_values")
if __name__ == "__main__":
    unittest.main()
