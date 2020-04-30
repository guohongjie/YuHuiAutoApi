#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import unittest
import re
import json
from bs4 import BeautifulSoup
import time
import sys
#sys.path.append("./app/base/pythonProject/base")
#sys.path.append("../../base")
from app.base.pythonProject.base.log import TestLog,fengefu,lianjiefu
from app.base.pythonProject.base.getConfig import ReadConfig
logging = TestLog().getlog()
class JingPinKeCheng_Test(unittest.TestCase):

    """每日积累"""
    @classmethod
    def setUpClass(self):
        """起始方法
        #:return:  cookies """
        s = ReadConfig()
        env_flag = s.get_env("env_flag")
        env_num = s.get_env("env_num")
        self.phoneNum = s.get_params("phoneNum")
        self.cookies = requests.cookies.RequestsCookieJar()
        self.cookies.set('env_flag', env_flag)  #设置测试环境
        self.cookies.set("env_num",env_num)  #设置环境号
        self.headers = {"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 Safari/601.1 wechatdevtools/1.02.1904090 MicroMessenger/6.7.3 Language/zh_CN webview/15565269850789002 webdebugger port/34092"}
        ysx_JingPinHaoKe_url = r"https://c.yunshuxie.com/class_all.html"
        self.resp = requests.get(url= ysx_JingPinHaoKe_url, headers= self.headers,cookies= self.cookies)
        logging.info(ysx_JingPinHaoKe_url + lianjiefu + self.resp.text +fengefu )
        self.cookies.update(self.resp.cookies)
        pattern = "{\"global.*}"
        self.result = re.findall(pattern, self.resp.content)[0]
        self.course_info = json.loads(self.result, encoding="utf8")["class_all"]["response"]["data"]["productList"]
       # productList = filter(lambda course: [m for m in course if m["productType" == u"每日一句"]],
        #                     self.course_info[1])  # 提取每日一句
        self.productDict = {}
        for  list_course in self.course_info:
            self.list_course = []
            for course in list_course:
                #print course["productType"]
                if course["productType"] == u"每日一句":
                    #print course["productName"]
                    self.productList = []
                    self.productName_html = {}
                    saleUrl = course["saleUrl"]
                    productName = course["productName"]
                    productPosters = course["productPosters"]
                    banerPosters = course["banerPosters"]
                    self.productName_html["productName"] = productName
                    self.productName_html["saleUrl"] = saleUrl
                    self.productName_html["productPosters"] = productPosters
                    self.productName_html["banerPosters"] = banerPosters
                    self.productList.append(self.productName_html)
                elif course["productType"] == u"名著读写线上课":
                    # print course["productName"]
                    self.productList = []
                    self.productName_html = {}
                    saleUrl = course["saleUrl"]
                    productName = course["productName"]
                    productPosters = course["productPosters"]
                    banerPosters = course["banerPosters"]
                    self.productName_html["productName"] = productName
                    self.productName_html["saleUrl"] = saleUrl
                    self.productName_html["productPosters"] = productPosters
                    self.productName_html["banerPosters"] = banerPosters
                    self.productList.append(self.productName_html)
                elif course["productType"] == u"名著读写面授课":
                    self.productList = []
                    self.productName_html = {}
                    saleUrl = course["saleUrl"]
                    productName = course["productName"]
                    productPosters = course["productPosters"]
                    banerPosters = course["banerPosters"]
                    self.productName_html["productName"] = productName
                    self.productName_html["saleUrl"] = saleUrl
                    self.productName_html["productPosters"] = productPosters
                    self.productName_html["banerPosters"] = banerPosters
                    self.productList.append(self.productName_html)
                elif course["productType"] == u"应试必备课程":
                    self.productList = []
                    self.productName_html = {}
                    saleUrl = course["saleUrl"]
                    productName = course["productName"]
                    productPosters = course["productPosters"]
                    banerPosters = course["banerPosters"]
                    self.productName_html["productName"] = productName
                    self.productName_html["saleUrl"] = saleUrl
                    self.productName_html["productPosters"] = productPosters
                    self.productName_html["banerPosters"] = banerPosters
                    self.productList.append(self.productName_html)
                self.list_course.append(self.productList )
            self.productDict[course["productType"]] =self.list_course
            #[{"saleUrl": url ,"productName": str ,"resp": html }]
        self.msg = """\n        Except:  {Except}-*-\n        Really:  {Really}"""  #校验HTTP返回代码

    def test_7_MZDXXSK_xzxtk(self):
        """名著读写线上课 - -《写作系统课》课程信息-个人购买"""
        for project in self.productDict[u"名著读写线上课"]:
            for course_info in project:
                if course_info["productName"] == u"写作系统课":
                    self.resp = requests.get(course_info["saleUrl"],headers=self.headers,cookies=self.cookies)
                    logging.info(course_info["saleUrl"] + lianjiefu + self.resp.text + fengefu)
                    productPosters_resp = requests.get(course_info["productPosters"],headers=self.headers,cookies=self.cookies)
                    logging.info(course_info["productPosters"] + lianjiefu + productPosters_resp.text + fengefu)
                    banerPosters_resp = requests.get(course_info["banerPosters"],headers=self.headers,cookies=self.cookies)
                    logging.info(course_info["banerPosters"] + lianjiefu + banerPosters_resp.text + fengefu)
                    assert self.resp.status_code == 200
                    assert productPosters_resp.status_code == 200
                    assert banerPosters_resp.status_code == 200
                    url = r"https://account.yunshuxie.com/v1/validate/wap/newplat_code_reset.htm?phone={phone}&type=2".format(phone=self.phoneNum)
                    account_resp = requests.get(url=url,headers=self.headers,cookies=self.cookies)  # 获取验证码，自动完成{"msg":"验证码为123456"}
                    logging.info(url + lianjiefu + account_resp.text + fengefu)
                    url = r"https://wap.yunshuxie.com/v1/member_standard_product/get_member_standard_detailv2.json"
                    params = {"memberCourseType":"2","type":"1","memberGrade":"3","phone":self.phoneNum,"callback":"__jp0"}
                    self.resp = requests.get(url=url,headers=self.headers,params=params,cookies=self.cookies)
                    result = json.loads(re.findall("{.*}", self.resp.content)[0], encoding="utf8")
                    assert result["returnCode"] == "0",self.msg.format(Except="0",Really=result["returnCode"])
                    url = r"https://pay.yunshuxie.com/v6/order/order_param.htm"
                    productHoursId = result["data"]["courseList"][0]["productHoursId"]
                    productId = result["data"]["courseList"][0]["productId"]
                    params = {"memberCourseType":"2","type":"1","phIds":productHoursId,"memberGrade":"3","phone":self.phoneNum}
                    url = r"https://pay.yunshuxie.com/v6/order/create2.htm"
                    params = {"phone":self.phoneNum,"pIds":productHoursId,"phIds":productId,
                              "pType":"1","productType":"1","memberCourseType":"2","type":"1","channelId":"AliPay",
                              "memberGrade":"3","sk":"null","cSn":"","addressId":"-1","activityId":"-1","customizeGroupId":"-1"}
                    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
                    self.resp = requests.get(url=url,headers=headers,params=params ,cookies=self.cookies)   #生成支付订单
                    print self.resp.content
                    logging.info(url + lianjiefu + self.resp.text + fengefu)
                    result = json.loads(re.findall("{.*}", self.resp.content)[0], encoding="utf8")
                    assert result["returnCode"] == "0",self.msg.format(Except="0",Really=result["returnCode"])
    def test_8_MZDXXSK_zwydyjpxgk(self):
        """名著读写线上课 - -《作文一对一精批细改课》课程信息-个人购买"""
        for project in self.productDict[u"名著读写线上课"]:
            for course_info in project:
                if course_info["productName"] == u"作文一对一精批细改课":
                    self.resp = requests.get(course_info["saleUrl"],headers=self.headers,cookies=self.cookies)
                    logging.info(course_info["saleUrl"] + lianjiefu + self.resp.text + fengefu)
                    productPosters_resp = requests.get(course_info["productPosters"],headers=self.headers,cookies=self.cookies)
                    logging.info(course_info["productPosters"] + lianjiefu + productPosters_resp.text + fengefu)
                    banerPosters_resp = requests.get(course_info["banerPosters"],headers=self.headers,cookies=self.cookies)
                    logging.info(course_info["banerPosters"] + lianjiefu + banerPosters_resp.text + fengefu)
                    assert self.resp.status_code == 200
                    assert productPosters_resp.status_code == 200
                    assert banerPosters_resp.status_code == 200
                    url = r"https://pay.yunshuxie.com/v6/order/query/product_course.htm"
                    params = {"grade":"3","callback":"Zepto1557730451559"}
                    self.resp = requests.get(url=url,headers=self.headers,params=params,cookies=self.cookies)
                    result = json.loads(re.findall("{.*}", self.resp.content)[0], encoding="utf8")
                    assert result["returnCode"] == "0",self.msg.format(Except="0",Really=result["returnCode"])
                    productCourseHoursId = result["data"][0]["productCourseHoursId"]
                    productCourseId = result["data"][0]["productCourseId"]
                    productId = result["data"][0]["productId"]
                    url = r"https://account.yunshuxie.com/v1/validate/wap/newplat_code_reset.htm?phone={phone}&type=2".format(phone=self.phoneNum)
                    account_resp = requests.get(url=url,headers=self.headers,cookies=self.cookies)  # 获取验证码，自动完成{"msg":"验证码为123456"}
                    logging.info(url + lianjiefu + account_resp.text + fengefu)
                    url = r"https://pay.yunshuxie.com/v6/order/query/product_price.htm"
                    params = {"phone":self.phoneNum,"pId":productId,"callback":"__jp2"}
                    self.resp = requests.get(url=url,headers=self.headers,params=params,cookies=self.cookies)
                    result = json.loads(re.findall("{.*}", self.resp.content)[0], encoding="utf8")
                    url = "https://pay.yunshuxie.com/v6/order/create.htm"
                    params = {"phone":self.phoneNum,"pIds":productCourseHoursId,"gId":"-1",
                              "pId":productId,"pType":"1","productType":"66","type":"1","channelId":"AliPay",
                              "grade":"三年级","sk":"null","cSn":"","addressId":"-1"}
                    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
                    self.resp = requests.get(url=url,headers=headers,params=params ,cookies=self.cookies)   #生成支付订单
                    print self.resp.content
                    logging.info(url + lianjiefu + self.resp.text + fengefu)
                    result = json.loads(re.findall("{.*}", self.resp.content)[0], encoding="utf8")
                    assert result["returnCode"] == "0",self.msg.format(Except="0",Really=result["returnCode"])
    @classmethod
    def tearDownClass(self):
        """测试结束后执行,断言Req==Resp
        :return:  True OR False"""
        pass
if __name__ == "__main__":
    unittest.main()