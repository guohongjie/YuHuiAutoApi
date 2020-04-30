#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import unittest
import json
import time
# import sys
# sys.path.append("../../base")
from app.base.pythonProject.base.log import TestLog,fengefu,lianjiefu
from app.base.pythonProject.base.py_redis import MyRedis
from app.base.pythonProject.base.getCookies import get_ysx_crm_cookie
logging = TestLog().getlog()
class Ysx_Crm_XSHD(unittest.TestCase):
    """CRM 销售活动"""
    @classmethod
    def setUpClass(self):
        redis = MyRedis()
        env_flag = redis.str_get("ysx_crm_env_flag")
        env_num = redis.str_get("ysx_crm_env_num")
        self.session = requests.Session()
        cookies = get_ysx_crm_cookie(env_flag,env_num)
        header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","Accept": "application/json, text/javascript, */*; q=0.01","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9","Connection": "keep-alive","Upgrade-Insecure-Requests": "1"}
        self.msg = """\n        Expect:  {Expect}-*-\n        Really:  {Really}"""  # 校验HTTP返回代码
        self.session.headers = header
        self.session.cookies = cookies
    def test_01_custom_group_list(self):
        """自定义团报工具-活动列表 <br/> http://admin.crm.yunshuxie.com/custom_group/get/custom_group_list.htm<br/>{"limit": "10","sort": "createDate","order":"DESC","offset": "0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/custom_group/get/custom_group_list.htm"
        params = {"limit": "10","sort": "createDate","order":"DESC","offset": "0"}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total":3,"rows":""}
        assert result.has_key("total")==expect.has_key("total"),self.msg.format(Expect=expect["total"],Really=result["total"])
        assert isinstance(result["total"],int)==True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"],Really=result["rows"])
    def test_02_custom_group_toaudit_list(self):
        """自定义团报工具-审核工具-待审核 <br/> http://admin.crm.yunshuxie.com/custom_group/get/custom_group_toaudit_list.htm<br/>{"customStatus":"2","sort":"createDate",<br/>"order":"DESC","limit":"20","offset":"0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/custom_group/get/custom_group_toaudit_list.htm"
        params = {"customStatus":"2","sort":"createDate","order":"DESC","limit":"20","offset":"0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total":0,"rows":""}
        assert result.has_key("total")==expect.has_key("total"),self.msg.format(Expect=expect["total"],Really=result["total"])
        assert isinstance(result["total"],int)==True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"],Really=result["rows"])
    def test_03_custom_group_toaudit_list(self):
        """自定义团报工具-审核工具-已审核 <br/>http://admin.crm.yunshuxie.com/custom_group/get/custom_group_toaudit_list.htm<br/> {"customStatus":"2","sort":"createDate",<br/>"order":"DESC","limit":"20","offset":"0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/custom_group/get/custom_group_toaudit_list.htm"
        params = {"customStatus": "3", "sort": "createDate", "order": "DESC", "limit": "20", "offset": "0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url, params=params)
        print self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total": 0, "rows": ""}
        assert result.has_key("total") == expect.has_key("total"), self.msg.format(Expect=expect["total"],
                                                                                   Really=result["total"])
        assert isinstance(result["total"], int) == True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"],
                                                                                 Really=result["rows"])
    def test_04_ysxlogistics_list(self):
        """物流管理-物流列表 <br/>http://admin.crm.yunshuxie.com/ysxlogistics/list<br/>{"_search": "false","nd": "1558593868835",<br/>"limit": "10","page":"1","sidx":"","order":"asc"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/ysxlogistics/list"
        params = {"_search": "false","nd": "1558593868835","limit": "10","page":"1","sidx":"","order":"asc"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"code":0,"page":""}
        assert result["code"]==expect["code"],self.msg.format(Expect=expect["code"],Really=result["code"])
        assert result.has_key("page") == expect.has_key("page"), self.msg.format(Expect=expect["rows"],Really=result["rows"])
    def test_05_ysxprize_list(self):
        """物流管理-物流列表 <br/>http://admin.crm.yunshuxie.com/ysxprize/list<br/>{"_search": "false","nd": "1558593868835",<br/>"limit": "10","page":"1","sidx":"","order":"asc"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/ysxprize/list"
        params = {"_search": "false","nd": "1558594133641","limit": "10","page":"1","sidx":"","order":"asc"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"code": 0, "page": ""}
        assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"], Really=result["code"])
        assert result.has_key("page") == expect.has_key("page"), self.msg.format(Expect=expect["rows"],
                                                                                 Really=result["rows"])
    def test_06_query_product_info(self):
        """销售物料-课程管理 <br/>http://admin.crm.yunshuxie.com/syssalesmaterial/query_product_info<br/>{"_search": "false","nd": "1558593868835",<br/>"limit": "10","page":"1","sidx":"","order":"asc"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/syssalesmaterial/query_product_info"
        params = {"order": "asc","limit": "10","offset":"0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total":0,"rows":""}
        assert result.has_key("total")==expect.has_key("total"),self.msg.format(Expect=expect["total"],Really=result["total"])
        assert isinstance(result["total"],int)==True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"],Really=result["rows"])
    def test_07_sales_tag_list(self):
        """销售物料-标签管理 <br/>http://admin.crm.yunshuxie.com/syssalesmaterial/sales_tag_list<br/>{"_search": "false","nd": "1558593868835",<br/>"limit": "10","page":"1","sidx":"","order":"asc"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/syssalesmaterial/sales_tag_list"
        params = {"sort":"orderId","order": "asc","limit": "10","offset":"0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total":0,"rows":""}
        assert result.has_key("total")==expect.has_key("total"),self.msg.format(Expect=expect["total"],Really=result["total"])
        assert isinstance(result["total"],int)==True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"],Really=result["rows"])
    def test_08_sales_product_list(self):
        """销售物料-海报管理 <br/>http://admin.crm.yunshuxie.com/syssalesmaterial/sales_product_list<br/>{"sort":"postersId","order": "asc","limit": "10","offset":"0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/syssalesmaterial/sales_product_list"
        params = {"sort":"postersId","order": "asc","limit": "10","offset":"0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total":0,"rows":""}
        assert result.has_key("total")==expect.has_key("total"),self.msg.format(Expect=expect["total"],Really=result["total"])
        assert isinstance(result["total"],int)==True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"],Really=result["rows"])
    def test_09_recharge_list(self):
        """充值管理-话费充值审核 <br/>http://admin.crm.yunshuxie.com/v1/recharge/list<br/>{"sort":"orderId","order": "DESC","limit": "10","offset":"0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/recharge/list"
        params = {"sort":"orderId","order": "DESC","limit": "10","offset":"0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total":0,"rows":""}
        assert result.has_key("total")==expect.has_key("total"),self.msg.format(Expect=expect["total"],Really=result["total"])
        assert isinstance(result["total"],int)==True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"],Really=result["rows"])
    def test_10_recharge_phone_already_list(self):
        """充值管理-话费到账查询 <br/>http://admin.crm.yunshuxie.com/v1/recharge/phone_already_list<br/>{"sort":"orderId","order": "DESC","limit": "10","offset":"0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/recharge/phone_already_list"
        params = {"sort":"orderId","order": "DESC","limit": "10","offset":"0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total":0,"rows":""}
        assert result.has_key("total")==expect.has_key("total"),self.msg.format(Expect=expect["total"],Really=result["total"])
        assert isinstance(result["total"],int)==True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"],Really=result["rows"])
    def test_11_recharge_invate_list(self):
        """充值管理-邀请审核 <br/> http://admin.crm.yunshuxie.com/v1/recharge/invate_list<br/>{"sort":"orderId","order": "DESC","limit": "10","offset":"0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/recharge/invate_list"
        params = {"sort":"orderId","order": "DESC","limit": "10","offset":"0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total":0,"rows":""}
        assert result.has_key("total")==expect.has_key("total"),self.msg.format(Expect=expect["total"],Really=result["total"])
        assert isinstance(result["total"],int)==True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"],Really=result["rows"])
    def test_12_recharge_invate_already_list(self):
        """充值管理-邀请到账查询 <br/>http://admin.crm.yunshuxie.com/v1/recharge/invate_already_list<br/>{"sort":"orderId","order": "DESC","limit": "10","offset":"0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/recharge/invate_already_list"
        params = {"sort":"orderId","order": "DESC","limit": "10","offset":"0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total":0,"rows":""}
        assert result.has_key("total")==expect.has_key("total"),self.msg.format(Expect=expect["total"],Really=result["total"])
        assert isinstance(result["total"],int)==True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"],Really=result["rows"])
    def test_13_recharge_cashback_list(self):
        """充值管理-返现审核 <br/>http://admin.crm.yunshuxie.com/v1/recharge/cashback_list<br/>{"sort":"orderId","order": "DESC","limit": "10","offset":"0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/recharge/cashback_list"
        params = {"sort":"orderId","order": "DESC","limit": "10","offset":"0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total":0,"rows":""}
        assert result.has_key("total")==expect.has_key("total"),self.msg.format(Expect=expect["total"],Really=result["total"])
        assert isinstance(result["total"],int)==True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"],Really=result["rows"])
    def test_14_recharge_cashback_already_list(self):
        """充值管理-邀请到账查询 <br/>http://admin.crm.yunshuxie.com/v1/recharge/cashback_already_list<br/>{"sort":"orderId","order": "DESC","limit": "10","offset":"0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/recharge/cashback_already_list"
        params = {"sort":"orderId","order": "DESC","limit": "10","offset":"0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total":0,"rows":""}
        assert result.has_key("total")==expect.has_key("total"),self.msg.format(Expect=expect["total"],Really=result["total"])
        assert isinstance(result["total"],int)==True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"],Really=result["rows"])
    def test_15_recharge_sale_invate_already_list(self):
        """充值管理-销售查询邀请返现记录 <br/>http://admin.crm.yunshuxie.com/v1/recharge/sale_invate_already_list<br/>{"sort":"orderId","order": "DESC","limit": "10","offset":"0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/recharge/sale_invate_already_list"
        params = {"sort":"orderId","order": "DESC","limit": "10","offset":"0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total":0,"rows":""}
        assert result.has_key("total")==expect.has_key("total"),self.msg.format(Expect=expect["total"],Really=result["total"])
        assert isinstance(result["total"],int)==True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"],Really=result["rows"])
    def test_16_recharge_original_cashback_list(self):
        """充值管理-原路返现<br/>http://admin.crm.yunshuxie.com/v1/recharge/original_cashback_list<br/>{"sort":"orderId","order": "DESC","limit": "10","offset":"0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/recharge/original_cashback_list"
        params = {"sort":"orderId","order": "DESC","limit": "10","offset":"0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total":0,"rows":""}
        assert result.has_key("total")==expect.has_key("total"),self.msg.format(Expect=expect["total"],Really=result["total"])
        assert isinstance(result["total"],int)==True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"],Really=result["rows"])
    def test_17_recharge_sale_cashback_already_list(self):
        """充值管理-销售查询活动返现记录<br/>http://admin.crm.yunshuxie.com/v1/recharge/sale_cashback_already_list<br/>{"sort":"orderId","order": "DESC","limit": "10","offset":"0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/recharge/sale_cashback_already_list"
        params = {"sort":"orderId","order": "DESC","limit": "10","offset":"0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total":0,"rows":""}
        assert result.has_key("total")==expect.has_key("total"),self.msg.format(Expect=expect["total"],Really=result["total"])
        assert isinstance(result["total"],int)==True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"],Really=result["rows"])
    def test_18_recharge_sale_phone_already_list(self):
        """充值管理-销售查询话费充值记录<br/> http://admin.crm.yunshuxie.com/v1/recharge/sale_phone_already_list<br/>{"sort":"orderId","order": "DESC","limit": "10","offset":"0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/recharge/sale_phone_already_list"
        params = {"sort":"orderId","order": "DESC","limit": "10","offset":"0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total":0,"rows":""}
        assert result.has_key("total")==expect.has_key("total"),self.msg.format(Expect=expect["total"],Really=result["total"])
        assert isinstance(result["total"],int)==True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"],Really=result["rows"])
    def test_19_recharge_new_year_scholarships_cashback_list(self):
        """充值管理-新年奖学金审核<br/>http://admin.crm.yunshuxie.com/v1/recharge/new_year_scholarships/cashback_list<br/>{"sort":"orderId","order": "DESC","limit": "10","offset":"0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/recharge/new_year_scholarships/cashback_list"
        params = {"sort":"orderId","order": "DESC","limit": "10","offset":"0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total":0,"rows":""}
        assert result.has_key("total")==expect.has_key("total"),self.msg.format(Expect=expect["total"],Really=result["total"])
        assert isinstance(result["total"],int)==True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"],Really=result["rows"])
    def test_20_recharge_new_year_scholarships_already_list(self):
        """充值管理-新年奖学金到账查询<br/>http://admin.crm.yunshuxie.com/v1/recharge/new_year_scholarships_already_list<br/>{"sort":"orderId","order": "DESC","limit": "10","offset":"0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/recharge/new_year_scholarships_already_list"
        params = {"sort":"orderId","order": "DESC","limit": "10","offset":"0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total":0,"rows":""}
        assert result.has_key("total")==expect.has_key("total"),self.msg.format(Expect=expect["total"],Really=result["total"])
        assert isinstance(result["total"],int)==True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"],Really=result["rows"])
    def test_21_ysx_sales_product_list(self):
        """课程商城-课程商城<br/>http://admin.crm.yunshuxie.com/ysx_sales_product/list.json<br/>{"page":"1","limit":"10"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/ysx_sales_product/list.json"
        params = {"page":"1","limit":"30"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url,data=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"code":0,"count":"","data":""}
        assert result["code"]==expect["code"],self.msg.format(Expect=expect["code"],Really=result["code"])
        assert result.has_key("data")==expect.has_key("data"),self.msg.format(Expect=expect["data"],Really=result["data"])
        assert isinstance(result["count"],int)==True
    def test_22_shopping_card_query_shopping_card(self):
        """购书券管理-购书券查询<br/>http://admin.crm.yunshuxie.com/v1/crm/shopping_card/query_shopping_card<br/>{"sort":"orderSn","order":"DESC","limit":"10","offset":"0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/crm/shopping_card/query_shopping_card"
        params = {"sort":"orderSn","order":"DESC","limit":"10","offset":"0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url,data=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total":0,"rows":""}
        assert result.has_key("total")==expect.has_key("total"),self.msg.format(Expect=expect["total"],Really=result["total"])
        assert isinstance(result["total"],int)==True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"],Really=result["rows"])
    def test_23_shopping_card_query_shopping_card(self):
        """购书券管理-购书券退回管理<br/>http://admin.crm.yunshuxie.com/v1/crm/shopping_card/query_shopping_card<br/>{"sort":"orderSn","order":"DESC","limit":"10","offset":"0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/crm/shopping_card/query_shopping_card"
        params = {"sort":"orderSn","order":"DESC","limit":"10","offset":"0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url,data=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total":0,"rows":""}
        assert result.has_key("total")==expect.has_key("total"),self.msg.format(Expect=expect["total"],Really=result["total"])
        assert isinstance(result["total"],int)==True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"],Really=result["rows"])
    def test_24_coupon_activity_list(self):
        """代金券管理-代金券活动列表 <br/>http://admin.crm.yunshuxie.com/v1/crm/coupon_activity/list<br/>{"limit": "10","sort": "couponActivityId","order":"DESC","offset": "0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/crm/coupon_activity/list"
        params = {"limit": "10","sort": "couponActivityId","order":"DESC","offset": "0"}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total":3,"rows":""}
        assert result.has_key("total")==expect.has_key("total"),self.msg.format(Expect=expect["total"],Really=result["total"])
        assert isinstance(result["total"],int)==True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"],Really=result["rows"])
    def test_25_custom_group_list(self):
        """代金券管理-发布代金券->代金券审核通过->失效 <br/> http://admin.crm.yunshuxie.com/v1/crm/coupon_activity/edit<br/>{"couponActivityName": name,"couponInstructions": "测试_自动化测试创建_%d"%(time.time()),<br/>"couponTotalAmount": "199","couponSingleAmount": "199","couponDailyLimit": "5",<br/>"limitPersonReceive": "20","activityStartDate": "2019-05-01 00%3A00%3A00",<br/>"activityEndDate": "2019-05-01 00%3A00%3A00","couponType":"1","limitAmount":"",<br/>"effectiveType": "1","validityDays": "1","validatyEndDate": "",<br/>"validatyStartDate": "","courseApplyType": "1","courseApply": "-1",<br/>"sendMode": "2","activityStatus": "","couponActivityId":""}<br/>{"couponActivityId": couponActivityId,"activityStatus": "3"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/crm/coupon_activity/edit"
        name = "测试_自动化测试_%d"%(time.time())
        params = {"couponActivityName": name,
                  "couponInstructions": "测试_自动化测试创建_%d"%(time.time()),
                  "couponTotalAmount": "199",
                  "couponSingleAmount": "199","couponDailyLimit": "5",
                  "limitPersonReceive": "20","activityStartDate": "2019-05-01 00%3A00%3A00",
                  "activityEndDate": "2019-05-01 00%3A00%3A00","couponType":"1","limitAmount":"",
                  "effectiveType": "1","validityDays": "1","validatyEndDate": "",
                  "validatyStartDate": "","courseApplyType": "1","courseApply": "-1",
                  "sendMode": "2","activityStatus": "","couponActivityId":""}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url,data=params)
        print "创建代金券:",self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"returnCode":0,"data":""}
        assert result["returnCode"]==expect["returnCode"],self.msg.format(Expect=expect["returnCode"],Really=result["returnCode"])
        assert isinstance(result["returnCode"],int)==True
        assert result.has_key("data") == expect.has_key("data"), self.msg.format(Expect=expect["data"],Really=result["data"])
        url = r"http://admin.crm.yunshuxie.com/v1/crm/coupon_activity/test_list" # 查询代金券 couponActivityId
        params = {"couponActivityName":name,"couponActivityNumber":"","activityStatus":"1","sort":"couponActivityId","order":"DESC","limit":"10","offset":"0"}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url, data=params)
        result = json.loads(self.resp.content, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        couponActivityId = result["rows"][0]["couponActivityId"]
        url = r"http://admin.crm.yunshuxie.com/v1/crm/coupon_activity/edit"  #审核代金券
        params = {"couponActivityId": couponActivityId,"activityStatus": "3"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url, data=params)
        print "审核代金券:",self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        expect = {"returnCode": 0, "data": ""}
        assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                             Really=result["returnCode"])
        assert isinstance(result["returnCode"], int) == True
        assert result.has_key("data") == expect.has_key("data"), self.msg.format(Expect=expect["data"],
                                                                                 Really=result["data"])
        url = r"http://admin.crm.yunshuxie.com/v1/crm/coupon_activity/edit"  # 失效代金券
        params = {"couponActivityId": couponActivityId,"activityStatus": "4"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url, data=params)
        print "失效代金券:",self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                             Really=result["returnCode"])
        assert isinstance(result["returnCode"], int) == True
        assert result.has_key("data") == expect.has_key("data"), self.msg.format(Expect=expect["data"],
                                                                                 Really=result["data"])
    def test_26_custom_group_list(self):
        """代金券管理-发布代金券->代金券审核拒绝 <br/>http://admin.crm.yunshuxie.com/v1/crm/coupon_activity/edit<br/>http://admin.crm.yunshuxie.com/v1/crm/coupon_activity/test_list<br/> http://admin.crm.yunshuxie.com/v1/crm/coupon_activity/edit<br/>{"couponActivityName": name,"couponInstructions": "测试_自动化测试创建_%d"%(time.time()),<br/>"couponTotalAmount": "199","couponSingleAmount": "199","couponDailyLimit": "5",<br/>"limitPersonReceive": "20","activityStartDate": "2019-05-01 00%3A00%3A00",<br/>"activityEndDate": "2019-05-01 00%3A00%3A00","couponType":"1","limitAmount":"",<br/>"effectiveType": "1","validityDays": "1","validatyEndDate": "",<br/>"validatyStartDate": "","courseApplyType": "1","courseApply": "-1",<br/>"sendMode": "2","activityStatus": "","couponActivityId":""}<br/>{"couponActivityId": couponActivityId,"activityStatus": "4"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/crm/coupon_activity/edit"
        name = "测试_自动化测试_%d"%(time.time())
        params = {"couponActivityName": name,
                  "couponInstructions": "测试_自动化测试创建_%d"%(time.time()),
                  "couponTotalAmount": "199",
                  "couponSingleAmount": "199","couponDailyLimit": "5",
                  "limitPersonReceive": "20","activityStartDate": "2019-05-01 00%3A00%3A00",
                  "activityEndDate": "2019-05-01 00%3A00%3A00","couponType":"1","limitAmount":"",
                  "effectiveType": "1","validityDays": "1","validatyEndDate": "",
                  "validatyStartDate": "","courseApplyType": "1","courseApply": "-1",
                  "sendMode": "2","activityStatus": "","couponActivityId":""}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url,data=params)
        print "创建代金券:",self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"returnCode":0,"data":""}
        assert result["returnCode"]==expect["returnCode"],self.msg.format(Expect=expect["returnCode"],Really=result["returnCode"])
        assert isinstance(result["returnCode"],int)==True
        assert result.has_key("data") == expect.has_key("data"), self.msg.format(Expect=expect["data"],Really=result["data"])
        url = r"http://admin.crm.yunshuxie.com/v1/crm/coupon_activity/test_list" # 查询代金券 couponActivityId
        params = {"couponActivityName":name,"couponActivityNumber":"","activityStatus":"1","sort":"couponActivityId","order":"DESC","limit":"10","offset":"0"}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url, data=params)
        print "查询代金券:", self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        couponActivityId = result["rows"][0]["couponActivityId"]
        url = r"http://admin.crm.yunshuxie.com/v1/crm/coupon_activity/edit"  #审核代金券
        params = {"couponActivityId": couponActivityId,"activityStatus": "4"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url, data=params)
        print "审核代金券:",self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        expect = {"returnCode": 0, "data": ""}
        assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                             Really=result["returnCode"])
        assert isinstance(result["returnCode"], int) == True
        assert result.has_key("data") == expect.has_key("data"), self.msg.format(Expect=expect["data"],
                                                                                 Really=result["data"])
    def test_27_custom_group_list(self):
        """代金券管理-发布代金券->代金券审核通过->失效->恢复 <br/> http://admin.crm.yunshuxie.com/v1/crm/coupon_activity/edit<br/>http://admin.crm.yunshuxie.com/v1/crm/coupon_activity/test_list<br/> http://admin.crm.yunshuxie.com/v1/crm/coupon_activity/edit<br/>{"couponActivityName": name,"couponInstructions": "测试_自动化测试创建_%d"%(time.time()),<br/>"couponTotalAmount": "199","couponSingleAmount": "199","couponDailyLimit": "5",<br/>"limitPersonReceive": "20","activityStartDate": "2019-05-01 00%3A00%3A00",<br/>"activityEndDate": "2019-05-01 00%3A00%3A00","couponType":"1","limitAmount":"",<br/>"effectiveType": "1","validityDays": "1","validatyEndDate": "",<br/>"validatyStartDate": "","courseApplyType": "1","courseApply": "-1",<br/>"sendMode": "2","activityStatus": "","couponActivityId":""}<br/>{"couponActivityId": couponActivityId,"activityStatus": "3"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/crm/coupon_activity/edit"
        name = "测试_自动化测试_%d"%(time.time())
        params = {"couponActivityName": name,
                  "couponInstructions": "测试_自动化测试创建_%d"%(time.time()),
                  "couponTotalAmount": "199",
                  "couponSingleAmount": "199","couponDailyLimit": "5",
                  "limitPersonReceive": "20","activityStartDate": "2019-05-01 00%3A00%3A00",
                  "activityEndDate": "2019-05-01 00%3A00%3A00","couponType":"1","limitAmount":"",
                  "effectiveType": "1","validityDays": "1","validatyEndDate": "",
                  "validatyStartDate": "","courseApplyType": "1","courseApply": "-1",
                  "sendMode": "2","activityStatus": "","couponActivityId":""}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url,data=params)
        print "发布代金券:",self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"returnCode":0,"data":""}
        assert result["returnCode"]==expect["returnCode"],self.msg.format(Expect=expect["returnCode"],Really=result["returnCode"])
        assert isinstance(result["returnCode"],int)==True
        assert result.has_key("data") == expect.has_key("data"), self.msg.format(Expect=expect["data"],Really=result["data"])
        url = r"http://admin.crm.yunshuxie.com/v1/crm/coupon_activity/test_list" # 查询代金券 couponActivityId
        params = {"couponActivityName":name,"couponActivityNumber":"","activityStatus":"1","sort":"couponActivityId","order":"DESC","limit":"10","offset":"0"}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url, data=params)
        result = json.loads(self.resp.content, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        couponActivityId = result["rows"][0]["couponActivityId"]
        url = r"http://admin.crm.yunshuxie.com/v1/crm/coupon_activity/edit"  #审核代金券
        params = {"couponActivityId": couponActivityId,"activityStatus": "3"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url, data=params)
        print "审核代金券:",self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        expect = {"returnCode": 0, "data": ""}
        assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                             Really=result["returnCode"])
        assert isinstance(result["returnCode"], int) == True
        assert result.has_key("data") == expect.has_key("data"), self.msg.format(Expect=expect["data"],
                                                                                 Really=result["data"])
        url = r"http://admin.crm.yunshuxie.com/v1/crm/coupon_activity/edit"  # 失效代金券
        params = {"couponActivityId": couponActivityId,"activityStatus": "4"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url, data=params)
        print "失效代金券:",self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                             Really=result["returnCode"])
        assert isinstance(result["returnCode"], int) == True
        assert result.has_key("data") == expect.has_key("data"), self.msg.format(Expect=expect["data"],
                                                                                 Really=result["data"])
        url = r"http://admin.crm.yunshuxie.com/v1/crm/coupon_activity/edit"  # 恢复代金券
        params = {"couponActivityId": couponActivityId, "activityStatus": "5"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url, data=params)
        print "恢复代金券:",self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                             Really=result["returnCode"])
        assert isinstance(result["returnCode"], int) == True
        assert result.has_key("data") == expect.has_key("data"), self.msg.format(Expect=expect["data"],
                                                                                 Really=result["data"])
    def test_28_coupon_list(self):
        """代金券管理-查询用户代金券 <br/>http://admin.crm.yunshuxie.com/v1/coupon/list<br/> {"limit": "10","sort": "createDate","order":"DESC","offset": "0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/coupon/list"
        params = {"limit": "10","sort": "createDate","order":"DESC","offset": "0"}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total":3,"rows":""}
        assert result.has_key("total")==expect.has_key("total"),self.msg.format(Expect=expect["total"],Really=result["total"])
        assert isinstance(result["total"],int)==True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"],Really=result["rows"])

    @classmethod
    def tearDownClass(self):
        pass

if __name__ == "__main__":
    unittest.main()