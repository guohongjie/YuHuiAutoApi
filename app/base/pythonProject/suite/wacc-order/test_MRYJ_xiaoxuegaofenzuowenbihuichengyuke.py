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
class XiaoXuegfzwbhcyk_Test(unittest.TestCase):
    """<br/>小学高分作文必会成语课->查询课程信息->查询优惠券-><br/>课程购买查询->个人购买全期课程"""
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
        header = {"Connection": "keep-alive","Content-Type": "application/x-www-form-urlencoded","Cache-Control": "no-cache",
                  "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 Safari/601.1 wechatdevtools/1.02.1904090 MicroMessenger/6.7.3 Language/zh_CN webview/15578306374265793 webdebugger port/22562"}
        self.session.headers = header
        cookies = {"env_flag": self.env_flag, "env_num": self.env_num}
        self.session.cookies = requests.utils.cookiejar_from_dict(cookies)
        self.pattern = "{\"global.*}"
        self.msg = """\n        Expect:  {Expect}-*-\n        Really:  {Really}"""  # 校验HTTP返回代码
        globals()["globals_values"] = ""
    def test_01_query_basic_course_id(self):
        """https://pay.yunshuxie.com/v6/basicCourse/query/basic_course_id.htm<br/>{"cType": "72","callback":"Zepto1557217118071"}"""
        url = r"https://pay.yunshuxie.com/v6/basicCourse/query/basic_course_id.htm"
        params = {"cType": "72","callback":"Zepto1557217118071"}
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        resp = self.session.get(url=url,params=params)
        logging.info(url + lianjiefu + resp.text + fengefu)
        print "课程查询:" + resp.content + "<br/>"
        result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
        assert result["returnCode"] == "0", self.msg.format(Expect="0", Really=result["returnCode"])
        values = [[course["productCourseHoursId"],course["productId"]] for course in result["data"]]
        globals()["globals_values"] = values
    def test_02_coupon_query_use_list(self):
        """https://pay.yunshuxie.com/v2/coupon/query/use_list.htm<br/>{"phone":self.phonenum,"productId":"7486","activityType":"-1","callback":"__jp0"}"""
        url = r"https://pay.yunshuxie.com/v1/coupon/query/use_list.htm"
        params = {"phone":self.phonenum,"productId":"7486","activityType":"-1","callback":"__jp0"}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        resp = self.session.get(url=url,params=params)
        print "优惠券查询:" + resp.content + "<br/>"
        logging.info(url + lianjiefu + resp.text + fengefu)
        result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
        expect = {"returnCode": "0", "returnMsg": "操作成功", "data": ""}
        assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],Really=result["returnCode"])
        assert result["returnCode"] == "0" or result["returnCode"] == 0
        assert result.has_key("returnMsg")
        assert result.has_key("data")
    def test_03_query_repeat_purchase(self):
        """https://pay.yunshuxie.com/v6/order/query/repeat_purchase.htm<br/> {"phone":self.phonenum,"pId":"7486","callback":"__jp2"}"""
        url = r"https://pay.yunshuxie.com/v6/order/query/repeat_purchase.htm"
        params = {"phone":self.phonenum,"pId":"7486","callback":"__jp2"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        resp = self.session.get(url=url, params=params)
        print "课程是否购买查询:" + resp.content + "<br/>"
        logging.info(url + lianjiefu + resp.text + fengefu)
        result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
        expect = {"returnCode": "0", "returnMsg": "操作成功", "data": ""}
        assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                             Really=result["returnCode"])
        assert result["returnCode"] == "0" or result["returnCode"] == 0
        assert result.has_key("returnMsg")
        assert result["data"] != {}
        assert result.has_key("data")
    def test_04_order_create(self):
        """https://pay.yunshuxie.com/v6/order/create.htm<br/>{"phone":"phoneNum,"customizeGroupId":"-1","phId":productCourseHoursId,<br/>"gId":"-1",pId": productId,"pType": "1","productType": "72","channelId": "AliPay",<br/>"cSn":"","sk":"","grade":"","addressId":"-1","activityId":"-1"}"""
        url = r"https://pay.yunshuxie.com/v6/order/create.htm"  # 生成支付订单
        for productCourseHoursId,productId  in globals_values:
            params = {"phone": self.phonenum, "customizeGroupId": "-1",
                      "phId": productCourseHoursId, "gId": "-1", "pId": productId, "pType": "1", "productType": 72,
                      "channelId": "AliPay", "cSn": "", "sk": "", "grade": "4", "addressId": "-1", "activityId": "-1"}
            logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
            str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
            print str_params
            resp = self.session.get(url=url,params=params)
            print "课程购买【phId】：{phId}--【pId】：{pId}:".format(phId=productCourseHoursId,pId=productId) + resp.content + "<br/>"
            logging.info(url + lianjiefu + resp.text + fengefu)
            result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
            assert result["returnCode"] == "0", self.msg.format(Expect="0", Really=result["returnCode"])
    def test_05_order_create(self):
        """https://pay.yunshuxie.com/v6/order/create.htm<br/>{"phone":"phoneNum,"customizeGroupId":"-1","phId":productCourseHoursId,<br/>"gId":"-1",pId": productId,"pType": "1","productType": "72","channelId": "WxPay",<br/>"cSn":"","sk":"","grade":"","addressId":"-1","activityId":"-1"}"""
        url = r"https://pay.yunshuxie.com/v6/order/create.htm"  # 生成支付订单
        for productCourseHoursId,productId  in globals_values:
            params = {"phone": self.phonenum, "customizeGroupId": "-1","code":"021ZaJtG17hM310SblvG1NZutG1ZaJtQ",
                      "phId": productCourseHoursId, "gId": "-1", "pId": productId, "pType": "1", "productType": 72,
                      "channelId": "WxPay", "cSn": "", "sk": "", "grade": "4", "addressId": "-1", "activityId": "-1"}
            logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
            str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
            print str_params
            resp = self.session.get(url=url,params=params)
            print "课程购买【phId】：{phId}--【pId】：{pId}:".format(phId=productCourseHoursId,pId=productId) + resp.content + "<br/>"
            logging.info(url + lianjiefu + resp.text + fengefu)
            result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
            assert result["returnCode"] == "0", self.msg.format(Expect="0", Really=result["returnCode"])
    @classmethod
    def tearDownClass(self):
        globals().pop("globals_values")
if __name__ == "__main__":
    unittest.main()