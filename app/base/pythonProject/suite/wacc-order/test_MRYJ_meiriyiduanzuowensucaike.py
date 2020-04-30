#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import unittest
import re
import json
import redis as red
from app.base.pythonProject.base.log import fengefu,lianjiefu,TestLog
from app.base.pythonProject.base.py_redis import MyRedis
#from app.base.pythonProject.base.getConfig import ReadConfig
logging = TestLog().getlog()
globals_values = ""
class MeiRiYiDuanZuWenSuCaiKe_Test(unittest.TestCase):
    """<br/>每日一段古诗文素材课->销售查询->查询课程信息-><br/>查询1-2年级课程->查询3-4年级课程->查询5-6年级课程-><br/>查询优惠券-><br/>课程购买查询->发送验证码->校验验证码->个人购买全期课程"""
    @classmethod
    def setUpClass(self):
        #s = ReadConfig()
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
        # self.redis_host = s.get_env("beta").split(":") if self.env_flag == "beta" else s.get_env("prod_stage").split(":")
        # r = red.Redis(host=self.redis_host[0], port=int(self.redis_host[1]), password="yunshuxie1029Password")
        # r.set("021ZaJtG17hM310SblvG1NZutG1ZaJtQ",'o38sIv_7FQInsBKJEUExn7wYxoHc&21_bk4dQIEFnYz5w8zJwDqan84UFmV_XVKEO5MJf7fv1pGR8tRH2MAtxpk0Pc1SqDwe5S90CE6TQo1wd346qEA5FQ')

        globals()["globals_values"] = ""
    def test_01_query_saleman(self):
        """https://pay.yunshuxie.com/v6/order/query/saleman.htm<br/>"{"sk":"null","callback":"Zepto1558926534750"}"""
        url = r"https://pay.yunshuxie.com/v6/order/query/saleman.htm"
        params = {"sk":"null","callback":"Zepto1558926534750"}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        resp = self.session.get(url=url,params=params)
        logging.info(url + lianjiefu + resp.text + fengefu)
        print "查询销售人员:"+resp.content +"<br/>"
        result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
        expect = {"returnCode": "15", "returnMsg": "操作成功", "data": ""}
        assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],Really=result["returnCode"])
        assert result["returnCode"] == "15" or result["returnCode"] == 15
        assert result.has_key("returnMsg")
        assert result.has_key("data")
    def test_02_WM_pay_hours(self):
        """https://wap.yunshuxie.com/v3/WM/pay/hours.htm<br/>{"callback": "Zepto1557217444367"}"""
        url = r"https://wap.yunshuxie.com/v3/WM/pay/hours.htm"
        params = {"callback": "Zepto1557217444367"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        resp = self.session.get(url=url, params=params)
        logging.info(url + lianjiefu + resp.text + fengefu)
        print "获取课程信息:"+resp.content +"<br/>"
        result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
        values = [[result["data"]["hours"][m]["productHoursId"],result["data"]["hours"][m]["productId"]] for m in range(len(result["data"]["hours"]))]
        assert result["returnCode"] == "0", self.msg.format(Expect="0", Really=result["returnCode"])
        assert result["data"] != {}, self.msg.format(Expect=resp.content, Really=result["returnCode"])
        globals()["globals_values"] = values
    def test_03_query_wm_course(self):
        """https://pay.yunshuxie.com/v6/order/query/wm_course.htm<br/>1-2年级<br/>{"code":"071qgt2Y18js711PIG0Y1vrK2Y1qgt2j","memberId":"",<br/>"phone":"","grade":",1,2,","callback":"Zepto1558946587441"}"""
        url = r"https://pay.yunshuxie.com/v6/order/query/wm_course.htm"
        params = {"code":"021ZaJtG17hM310SblvG1NZutG1ZaJtQ","memberId":"","phone":"","grade":",1,2,","callback":"Zepto1558946587441"}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        resp = self.session.get(url=url,params=params)
        logging.info(url + lianjiefu + resp.text + fengefu)
        print "查询1-2年级:"+resp.content +"<br/>"
        result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
        assert result["returnCode"] == "0", self.msg.format(Expect="0", Really=result["returnCode"])
        assert result["data"] != {}
    def test_04_query_wm_course(self):
        """https://pay.yunshuxie.com/v6/order/query/wm_course.htm<br/> 3-4年级<br/>{"code":"071qgt2Y18js711PIG0Y1vrK2Y1qgt2j","memberId":"",<br/>"phone":"","grade":",3,4,","callback":"Zepto1558946587441"}"""
        url = r"https://pay.yunshuxie.com/v6/order/query/wm_course.htm"
        params = {"code":"021ZaJtG17hM310SblvG1NZutG1ZaJtQ","memberId":"","phone":"","grade":",3,4,","callback":"Zepto1558946587441"}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        resp = self.session.get(url=url,params=params)
        logging.info(url + lianjiefu + resp.text + fengefu)
        print "查询3-4年级:"+resp.content +"<br/>"
        result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
        assert result["returnCode"] == "0", self.msg.format(Expect="0", Really=result["returnCode"])
        assert result["data"] != {}
    def test_05_query_wm_course(self):
        """https://pay.yunshuxie.com/v6/order/query/wm_course.htm<br/> 5-6年级<br/>{"code":"071qgt2Y18js711PIG0Y1vrK2Y1qgt2j","memberId":"",<br/>"phone":"","grade":",5,6,","callback":"Zepto1558946587441"}"""
        url = r"https://pay.yunshuxie.com/v6/order/query/wm_course.htm"
        params = {"code":"021ZaJtG17hM310SblvG1NZutG1ZaJtQ","memberId":"","phone":"","grade":",5,6,","callback":"Zepto1558946587441"}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        resp = self.session.get(url=url,params=params)
        logging.info(url + lianjiefu + resp.text + fengefu)
        print "查询5-6年级:"+resp.content +"<br/>"
        result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
        assert result["returnCode"] == "0", self.msg.format(Expect="0", Really=result["returnCode"])
        assert result["data"] != {}
    def test_06_query_use_list(self):
        """https://pay.yunshuxie.com/v1/coupon/query/use_list.htm<br/>{"phone":phonenum,"productId":product[1],"activityType":"1","callback":"__jp1"}"""
        url = r"https://pay.yunshuxie.com/v1/coupon/query/use_list.htm"
        for product in globals_values:
            params = {"phone":self.phonenum,"productId":product[1],"activityType":"1","callback":"__jp1"}
            logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
            str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
            print str_params
            resp = self.session.get(url=url,params=params)
            logging.info(url + lianjiefu + resp.text + fengefu)
            print "查询优惠券:" + resp.content + "<br/>"
            result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
            assert result["returnCode"] == "0", self.msg.format(Expect="0", Really=result["returnCode"])
            assert result.has_key("data"), self.msg.format(Expect=resp.content, Really=result["returnCode"])
    def test_07_order_query_wm_is_pay(self):
        """https://pay.yunshuxie.com/v6/order/query/wm_is_pay.htm<br/>{"phone":phonenum,"productCourseHourId": product[0],"callback": "__jp6"}"""
        url = r"https://pay.yunshuxie.com/v6/order/query/wm_is_pay.htm"
        for product in globals_values:
            params = {"phone": self.phonenum, "productCourseHourId": product[0], "callback": "__jp6"}
            logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
            str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
            print str_params
            resp = self.session.get(url=url,params=params)
            logging.info(url + lianjiefu + resp.text + fengefu)
            print "查询是否已购买:" + resp.content + "<br/>"
            result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
            assert result["returnCode"] == "0", self.msg.format(Expect="0", Really=result["returnCode"])
    def test_08_address_default(self):
        """https://account.yunshuxie.com/v1/address/default.htm<br/>{"phone":phoneNum, "callback": "__jp7"}"""
        url = r"https://account.yunshuxie.com/v1/address/default.htm"
        params = {"phone": self.phonenum, "callback": "__jp7"}
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        resp = self.session.get(url=url,params=params)
        logging.info(url + lianjiefu + resp.text + fengefu)
        print "加载地址:" + resp.content + "<br/>"
        result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
        assert result["returnCode"] == "0", self.msg.format(Expect="0", Really=result["returnCode"])
        assert result["data"] != {}, self.msg.format(Expect=resp.content, Really=result["returnCode"])
    def test_09_address_default(self):
        """https://account.yunshuxie.com/v1/address/default.htm<br/>{"phone":phoneNum, "callback": "__jp7"}"""
        url = r"https://account.yunshuxie.com/v1/address/default.htm"
        params = {"phone": self.phonenum, "callback": "__jp7"}
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        resp = self.session.get(url=url,params=params)
        logging.info(url + lianjiefu + resp.text + fengefu)
        print "加载地址:" + resp.content + "<br/>"
        result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
        assert result["returnCode"] == "0", self.msg.format(Expect="0", Really=result["returnCode"])
        assert result["data"] != {}, self.msg.format(Expect=resp.content, Really=result["returnCode"])
    def test_10_get_create_order(self):
        """https://pay.yunshuxie.com/v6/order/create.htm<br/><br/>{"phone":phonenum,"customizeGroupId":"-1",<br/>"ysxOpenId":"osxBJ6MQ69yOMyhCejqj55SdKzyI","phId":productHoursId,<br/>Id":"-1","pId":productId,"pType":"1","productType":"17","channelId":"AliPay","cSn":"",<br/>"sk":"","grade":"","addressId":"-1","activityId":"-1"}"""
        url = r"https://pay.yunshuxie.com/v6/order/create.htm"
        for productHoursId,productId in globals_values:
            params = {"phone": "{}".format(self.phonenum), "customizeGroupId": "-1",
                  "ysxOpenId": "osxBJ6MQ69yOMyhCejqj55SdKzyI", "phId": productHoursId,
                  "gId": "-1", "pId": productId, "pType": "1", "productType": "17", "channelId": "AliPay", "cSn": "",
                  "sk": "", "grade": "", "addressId": "-1", "activityId": "-1"}
            logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
            str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
            print str_params
            resp = self.session.get(url=url,params=params)  # 生成支付订单
            logging.info(url + lianjiefu + resp.text + fengefu)
            print "购买phId={phId}:pId={pId} 课程{resp}<br/>".format(phId=productHoursId,pId=productId,resp=resp.content)
            result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
            assert result["returnCode"] == "0", self.msg.format(Expect="0", Really=result["returnCode"])
            assert result["data"] != {}, self.msg.format(Expect=resp.content, Really=result["returnCode"])
    def test_11_get_create_order(self):
        """https://pay.yunshuxie.com/v6/order/create.htm<br/><br/>{"phone":phonenum,"customizeGroupId":"-1",<br/>"ysxOpenId":"osxBJ6MQ69yOMyhCejqj55SdKzyI","phId":productHoursId,<br/>Id":"-1","pId":productId,"pType":"1","productType":"17","channelId":"WxPay","cSn":"",<br/>"sk":"","grade":"","addressId":"-1","activityId":"-1"}"""
        url = r"https://pay.yunshuxie.com/v6/order/create.htm"
        for productHoursId,productId in globals_values:
            params = {"phone": "{}".format(self.phonenum), "customizeGroupId": "-1",
                  "ysxOpenId": "osxBJ6MQ69yOMyhCejqj55SdKzyI", "phId": productHoursId,"code":"021ZaJtG17hM310SblvG1NZutG1ZaJtQ",
                  "gId": "-1", "pId": productId, "pType": "1", "productType": "17", "channelId": "WxPay", "cSn": "",
                  "sk": "", "grade": "", "addressId": "-1", "activityId": "-1"}
            logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
            str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
            print str_params
            resp = self.session.get(url=url,params=params)  # 生成支付订单
            logging.info(url + lianjiefu + resp.text + fengefu)
            print "购买phId={phId}:pId={pId} 课程{resp}<br/>".format(phId=productHoursId,pId=productId,resp=resp.content)
            result = json.loads(re.findall("{.*}", resp.content)[0], encoding="utf8")
            assert result["returnCode"] == "0", self.msg.format(Expect="0", Really=result["returnCode"])
            assert result["data"] != {}, self.msg.format(Expect=resp.content, Really=result["returnCode"])
    @classmethod
    def tearDownClass(self):
        globals().pop("globals_values")
if __name__ == "__main__":
    unittest.main()