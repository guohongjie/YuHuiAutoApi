#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import unittest
import re
import json
from app.base.pythonProject.base.log import fengefu,lianjiefu,TestLog
from app.base.pythonProject.base.py_redis import MyRedis
logging = TestLog().getlog()
globals_values = ""
class YuWenHeXinSuYangShuQiZhiBoKe_Test(unittest.TestCase):
    """<br/>语文核心素养直播课->查询课程信息->查询优惠券-><br/>课程购买查询->个人购买全期课程"""
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
        #cookies = {"env_flag": "prod", "env_num": ""}
        self.session.cookies = requests.utils.cookiejar_from_dict(cookies)
        self.pattern = "{\"global.*}"
        self.msg = """\n        Expect:  {Expect}-*-\n        Really:  {Really}"""  # 校验HTTP返回代码
        globals()["globals_values"] = ""
    def test_01_query_summerPrice(self):
        """https://pay.yunshuxie.com/v6/springReadMethod/query/summerPrice.htm<br/>{"pt":"-1","callback":"Zepto1557307951251"}"""
        url = r"https://pay.yunshuxie.com/v6/springReadMethod/query/summerPrice.htm"
        params = {"pt": "-1","callback": "Zepto1557307951251"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        resp = self.session.get(url=url,params=params)
        logging.info(url + lianjiefu + resp.text + fengefu)
        print "课程价格查询:" + resp.content + "<br/>"
        result = json.loads(re.findall("{.*}",resp.content)[0], encoding="utf8")
        assert result["returnCode"] == "0", self.msg.format(Expect="0", Really=result["returnCode"])
        values = [course["productId"] for course in result["data"]]
        globals()["globals_values"] = values

    def test_02_query_summerGrade(self):
        """https://pay.yunshuxie.com/v6/springReadMethod/query/summerGrade.htm<br/>{"productId":productId,"callback":"Zepto1559024340760"}"""
        url = r"https://pay.yunshuxie.com/v6/springReadMethod/query/summerGrade.htm"
        productId_grade = {}
        for productId in globals_values:
            params = {"productId":productId,"callback":"Zepto1559024340760"}
            logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
            str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
            print str_params
            resp = self.session.get(url=url,params=params)
            logging.info(url + lianjiefu + resp.text + fengefu)
            print "课程年级查询:" + resp.content + "<br/>"
            result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
            assert result["returnCode"] == "0", self.msg.format(Expect="0", Really=result["returnCode"])
            productId_grade[productId] = result["data"]
        globals()["globals_values"] = productId_grade
    def test_03_query_summerCourse(self):
        """"""
        url = r"https://pay.yunshuxie.com/v6/springReadMethod/query/summerCourse.htm"
        list_params = []
        for productId in globals_values.keys():
            for course in globals_values[productId]:
                params = {"grade":course["grade"],"productId":productId,"callback":"Zepto1559024340763"}
                logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
                str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
                print str_params
                resp = self.session.get(url=url, params=params)
                logging.info(url + lianjiefu + resp.text + fengefu)
                print "课程日期查询:" + resp.content + "<br/>"
                result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
                params["data"] = result["data"]
                list_params.append(params)
                assert result["returnCode"] == "0", self.msg.format(Expect="0", Really=result["returnCode"])
        globals()["globals_values"] = list_params
    def test_04_query_repeat_purchase(self):
        """https://pay.yunshuxie.com/v6/springReadMethod/query/summerPay.htm<br/> {"phone":phonenum,"pId":"7486","callback":"__jp2"}"""
        url = r"https://pay.yunshuxie.com/v6/springReadMethod/query/summerPay.htm"
        for datas in globals_values:
            params = {"phone": self.phonenum,"productId": datas["productId"],"grade":datas["grade"],"callback": "__jp2"}
            logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
            str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
            print str_params
            resp = self.session.get(url=url, params=params)
            logging.info(url + lianjiefu + resp.text + fengefu)
            print "课程是否购买查询:" + resp.content + "<br/>"
            result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
            assert result["returnCode"] == "0", self.msg.format(Expect="0", Really=result["returnCode"])

    def test_05_order_create(self):
        """https://pay.yunshuxie.com/v6/order/create.htm<br/>{"phone":"phoneNum,"customizeGroupId":"-1","phId":productCourseHoursId,<br/>"gId":"-1",pId": productId,"pType": "1","productType": "76","channelId": "AliPay",<br/>"cSn":"","sk":"","grade":"","addressId":"-1","activityId":"-1"}"""
        url = r"https://pay.yunshuxie.com/v6/order/create.htm"  # 生成支付订单
        for course in globals_values:
            for course_data in course["data"]:
                for course_phId in course_data:
                    params = {"phone": self.phonenum, "phId": course_phId["productCourseHoursId"], "gId": "-1", "productId": course["productId"],"pType": "1", "productType": "76", "channelId": "AliPay", "cSn": "", "sk": "","grade":  course["grade"], "customizeGroupId": "", "addressId": "-1", "activityId": "-1"}
                    logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
                    str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
                    print str_params
                    resp = self.session.get(url=url,params=params)
                    print "课程购买【phId】：{phId}--【pId】：{pId}:".format(phId=course_phId["productCourseHoursId"],pId=course["productId"]) + resp.content + "<br/>"
                    logging.info(url + lianjiefu + resp.text + fengefu)
                    result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
                    assert result["returnCode"] == "0", self.msg.format(Expect="0", Really=result["returnCode"])
    def test_06_order_create(self):
        """https://pay.yunshuxie.com/v6/order/create.htm<br/>{"phone":"phoneNum,"customizeGroupId":"-1","phId":productCourseHoursId,<br/>"gId":"-1",pId": productId,"pType": "1","productType": "76","channelId": "WxPay",<br/>"cSn":"","sk":"","grade":"","addressId":"-1","activityId":"-1"}"""
        url = r"https://pay.yunshuxie.com/v6/order/create.htm"  # 生成支付订单
        for course in globals_values:
            for course_data in course["data"]:
                for course_phId in course_data:
                    params = {"phone": self.phonenum, "phId": course_phId["productCourseHoursId"], "gId": "-1", "productId": course["productId"],"pType": "1", "productType": "76", "channelId": "WxPay", "cSn": "", "sk": "","grade":  course["grade"], "customizeGroupId": "", "addressId": "-1", "activityId": "-1","code":"021ZaJtG17hM310SblvG1NZutG1ZaJtQ"}
                    logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
                    str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
                    print str_params
                    resp = self.session.get(url=url,params=params)
                    print "课程购买【phId】：{phId}--【pId】：{pId}:".format(phId=course_phId["productCourseHoursId"],pId=course["productId"]) + resp.content + "<br/>"
                    logging.info(url + lianjiefu + resp.text + fengefu)
                    result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
                    assert result["returnCode"] == "0", self.msg.format(Expect="0", Really=result["returnCode"])
    @classmethod
    def tearDownClass(self):
        globals().pop("globals_values")
if __name__ == "__main__":
    unittest.main()