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
class ZuoWenJingPiXiGai_Test(unittest.TestCase):
    """<br/>作文一对一精批细改课->查询课程信息->查询活动是否发起-><br/>课程购买查询->个人购买全期课程"""
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
    def test_02_query_product_course(self):
        """https://pay.yunshuxie.com/v6/order/query/product_course.htm<br/>{"grade":3,"callback":"Zepto1560245513360"}"""
        url = r"https://pay.yunshuxie.com/v6/order/query/product_course.htm"
        grade_phlId_pcId_proId = {}
        for grade in range(3,10):
            params = {"grade":grade,"callback":"Zepto1560245513360"}
            str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
            print str_params
            resp = self.session.get(url=url,params=params)
            logging.info(url + lianjiefu + resp.text + fengefu)
            print "活动查询:" + resp.content + "<br/>"
            result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
            assert result["returnCode"] == "0", self.msg.format(Expect="0", Really=result["returnCode"])
            grade_phlId_pcId_proId[grade] = result["data"]
        globals()["globals_values"] = grade_phlId_pcId_proId
    def test_03_order_query_product_price(self):
        """https://pay.yunshuxie.com/v6/order/query/product_price.htm<br/>{"callback":"__jp2","phone":self.phonenum,"pId":couser["productId"]}"""
        url = r"https://pay.yunshuxie.com/v6/order/query/product_price.htm"
        for product in globals_values.values():
            for couser in product:
                params = {"callback":"__jp2","phone":self.phonenum,"pId":couser["productId"]}
                str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
                print str_params
                resp = self.session.get(url=url,params=params)
                logging.info(url + lianjiefu + resp.text + fengefu)
                print "查看pid={}课程价格:".format(couser["productId"]) + resp.content + "<br/>"
                result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
                assert result["returnCode"] == "0", self.msg.format(Expect="0", Really=result["returnCode"])

    def test_04_order_create_AliPay(self):  # 获得订单参数 productHoursId productId
        """https://pay.yunshuxie.com/v6/order/create.htm<br/>{"phone":self.phonenum,"pIds":productId,"phIds":productHoursId,"pType":"1",<br/>"productType":"1","memberCourseType":"1","type":"1","memberGrade":"1",<br/>"sk":"","cSn":"","addressId":"-1","activityId":"-1",<br/>"customizeGroupId":"-1","channelId":"AliPay"}"""
        url = r"https://pay.yunshuxie.com/v6/order/create.htm"
        grade = {3: u"三年级", 4: u"四年级", 5: u"五年级", 6: u"六年级", 7: u"七年级", 8: u"八年级", 9: u"九年级"}
        for grade_num, datas in globals_values.items():
            for courser in datas:
                params = {"phone": self.phonenum, "phId": courser["productCourseHoursId"], "gId": "-1",
                          "pId": courser["productId"],
                          "pType": "1", "productType": "66", "channelId": "AliPay", "cSn": "", "sk": "",
                          "grade": grade[grade_num], "addressId": "-1"}
                str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
                print str_params
                resp = self.session.get(url=url, params=params)
                print "生成订单:" + resp.content + "<br/>"
                logging.info(url + lianjiefu + resp.text + fengefu)
                result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
                assert result["returnCode"] == "0", self.msg.format(Expect="0", Really=result["returnCode"])
    def test_07_order_create_WxPay(self):  # 获得订单参数 productHoursId productId
        """https://pay.yunshuxie.com/v6/order/create2.htm<br/>{"phone":self.phonenum,"pIds":productId,"phIds":productHoursId,"pType":"1",<br/>"productType":"1","memberCourseType":"1","type":"1","memberGrade":"1",<br/>"sk":"","cSn":"","addressId":"-1","activityId":"-1",<br/>"customizeGroupId":"-1","channelId":"AliPay"}"""
        url = r"https://pay.yunshuxie.com/v6/order/create.htm"
        grade = {3:"三年级",4:"四年级",5:"五年级",6:"六年级",7:"七年级",8:"八年级",9:"九年级"}
        for grade_num,datas in globals_values.items():
            for courser in datas:
                params = {"phone":self.phonenum,"phId":courser["productCourseHoursId"] ,
                          "gId":-1,"pId":courser["productId"] ,"pType":1,"productType":66,
                          "channelId":"WxPay","cSn":"","code":"021ZaJtG17hM310SblvG1NZutG1ZaJtQ",
                          "sk":"","grade":"","addressId":"-1"}
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
