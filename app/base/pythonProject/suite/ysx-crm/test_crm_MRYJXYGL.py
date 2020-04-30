#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import unittest
import json
# import sys
# sys.path.append("../../base")
from app.base.pythonProject.base.log import TestLog,fengefu,lianjiefu
from app.base.pythonProject.base.py_redis import MyRedis
from app.base.pythonProject.base.getCookies import get_ysx_crm_cookie
logging = TestLog().getlog()
class Ysx_Crm_MeiRiYiJuXueYuanGuanLi(unittest.TestCase):
    """CRM 每日一句学员管理"""
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
    def test_01_serviceteacher(self):
        """每日一句分配老师 <br/> http://admin.crm.yunshuxie.com/admin/writing_material/query/serviceteacher.htm<br/>{"teacherType": "1","limit": "3",<br/>"order": "asc","offset": "0"}
        :param: order == asc
        :param: limit == 3
        :param: offset == 0
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/admin/writing_material/query/serviceteacher.htm"
        params = {"teacherType": "1","limit": "3","order": "asc","offset": "0"}
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
    def test_02_manage_list(self):
        """活跃度统计报表 <br/>http://admin.crm.yunshuxie.com/v1/crm/daily/manage_list<br/> {"sort": "wechatTeacherId","order": "asc",<br/>"limit": "10","offset": "0"}
        :param: order == asc
        :param: limit == 10
        :param: offset == 0
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/crm/daily/manage_list"
        params = {"sort": "wechatTeacherId","order": "asc","limit": "10","offset": "0"}
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
    def test_03_single_manage_list(self):
        """个人活跃度统计 <br/> http://admin.crm.yunshuxie.com/v1/crm/daily/single_manage_list<br/>{"sort": "wechatTeacherId","order": "asc",<br/>"limit": "10","offset": "0"}
        :param: sort == wechatTeacherId
        :param: order == asc
        :param: limit == 10
        :param: offset == 0
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/crm/daily/single_manage_list"
        params = {"sort": "wechatTeacherId","order": "asc","limit": "10","offset": "0"}
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
    def test_04_daily_list(self):
        """学员学习明细表 <br/>http://admin.crm.yunshuxie.com/v1/crm/daily/list<br/> {"sort": "payDate","order": "DESC",<br/>"limit": "10","offset": "0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/crm/daily/list"
        params = {"sort": "payDate","order": "DESC","limit": "10","offset": "0"}
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
    def test_05_daily_list(self):
        """学员学习明细表 <br/>http://admin.crm.yunshuxie.com/v1/crm/daily/list<br/>{"type": "-1","phone":"", "isWechat": "-1",<br/>"isReading": "1","isWriting": "1","isWritingMaterial": "1","isClock": "1","lastLogin": "-1","lastClock": "2",<br/>"communicateNum":"", "sort": "payDate",<br/>"order": "DESC","limit": "10","offset": "0"}
        :return limit==0:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/crm/daily/list"
        params = {"type": "-1","phone":"", "isWechat": "-1","isReading": "1","isWriting": "1","isWritingMaterial": "1","isClock": "1","lastLogin": "-1","lastClock": "2","communicateNum":"", "sort": "payDate","order": "DESC","limit": "10","offset": "0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total":0,"rows":""}
        assert result.has_key("total")==expect.has_key("total"),self.msg.format(Expect=expect["total"],Really=result["total"])
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"],Really=result["rows"])
    def test_06_ysxwechatserviceteacher_list(self):
        """设备分配表 <br/> http://admin.crm.yunshuxie.com/ysxwechatserviceteacher/list<br/>{"_search":"false","nd":"1558581314505","limit":"10",<br/>"page":"1","sidx":"","order":"asc"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/ysxwechatserviceteacher/list"
        params = {"_search": "false","nd": "1558581314505","limit": "10","page": "1","sidx": "","order": "asc"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"code":0,"page":""}
        assert result["code"]==expect["code"],self.msg.format(Expect=expect["code"],Really=result["code"])
        assert result.has_key("page") == expect.has_key("page"), self.msg.format(Expect=expect["page"],Really=result["page"])
        # moocClassId = result["rows"][0]["moocClassId"]
        # url = r"https://admin.crm.yunshuxie.com/admin/writing_material/create_posters.htm"
        # params = {"moocClassId":moocClassId,"type":"1"}
        # self.resp = self.session.get(url=url, params=params)
        # result_moocClassId = len(eval(self.resp.content))
        # print self.resp.content
        # assert result_moocClassId > 0, self.msg.format(Expect=moocClassId, Really=result_moocClassId)
    def test_07_serviceteacher(self):
        """学员学习明细表 <br/> http://admin.crm.yunshuxie.com/v1/crm/daily/list<br/>{"isManage":"1","sort": "payDate",<br/>"order": "ASC","limit": "10","offset":"0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/crm/daily/list"
        params = {"isManage":"1","sort": "payDate","order": "ASC","limit": "10","offset":"0"}
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

    @classmethod
    def tearDownClass(self):
        pass

if __name__ == "__main__":
    unittest.main()