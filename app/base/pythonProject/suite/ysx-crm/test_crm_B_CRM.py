#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import unittest
import json
import time
# import sys
# sys.path.append("../../base")
from app.base.pythonProject.base.log import fengefu,lianjiefu,TestLog
from app.base.pythonProject.base.py_redis import MyRedis
from app.base.pythonProject.base.getCookies import get_ysx_crm_cookie
logging = TestLog().getlog()
class Ysx_Crm_B_CRM(unittest.TestCase):
    """CRM B端CRM"""
    @classmethod
    def setUpClass(self):
        redis = MyRedis()
        self.env_flag = redis.str_get("ysx_crm_env_flag")
        self.env_num = redis.str_get("ysx_crm_env_num")
        self.session = requests.Session()
        cookies = get_ysx_crm_cookie(self.env_flag,self.env_num)
        header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","Accept": "application/json, text/javascript, */*; q=0.01","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9","Connection": "keep-alive","Upgrade-Insecure-Requests": "1"}
        self.msg = """\n        Expect:  {Expect}-*-\n        Really:  {Really}"""  # 校验HTTP返回代码
        self.session.headers = header
        self.session.cookies = cookies
    def test_01_statistics_yearCardList(self):
        """B端CRM->名著导读课程管理->统计报表->班级详情->跟踪记录(写跟踪beta测试)<br/>http://admin.crm.yunshuxie.com/v1/yearcard/statistics/yearCardList.htm<br/>{"startDate": "2018-01-01 00%3A00%3A00","endDate": "2019-12-31 00%3A00%3A00",<br/>"schoolName":"","teacherPhone":"", "teacherName": "","teacherStartDate": "2018-01-01 00%3A00%3A00",<br/>"teacherEndDate": "2019-12-31 00%3A00%3A00","userName":"" ,"province": "北京",<br/>"city": "北京市","district":"","sort": "classId",<br/>"order": "asc","limit": "10","offset": "0"}
        :return: True
        """
        url = r"http://admin.crm.yunshuxie.com/v1/yearcard/statistics/yearCardList.htm"
        params = {"startDate": "2018-01-01 00%3A00%3A00","endDate": "2019-12-31 00%3A00%3A00",
                  "schoolName":"","teacherPhone":"", "teacherName": "",
                  "teacherStartDate": "2018-01-01 00%3A00%3A00","teacherEndDate": "2019-12-31 00%3A00%3A00",
                  "userName":"" ,"province": "北京","city": "北京市","district":"","sort": "classId",
                  "order": "asc","limit": "10","offset": "0"}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params,ensure_ascii=False,encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"rows":"","total":""}
        assert result.has_key("rows")==expect.has_key("rows"),self.msg.format(Expect=expect.has_key("rows"),Really=result.has_key("rows"))
        assert result.has_key("total") == expect.has_key("total"), self.msg.format(Expect=expect.has_key("total"),
                                                                             Really=result.has_key("total"))
        classId = result["rows"][0]["classId"]
        memberId = result["rows"][0]["teacherMember"]
        phone = result["rows"][0]["teacherPhone"]
        url = r"http://admin.crm.yunshuxie.com/v1/yearcard/statistics/classDetailsList.htm"
        params = {"classId": classId,"sort": "memberId","order": "asc","limit": "10","offset": "0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url, params=params)
        print self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"rows": "", "total": ""}
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect.has_key("rows"),
                                                                                 Really=result.has_key("rows"))
        assert result.has_key("total") == expect.has_key("total"), self.msg.format(Expect=expect.has_key("total"),
                                                                                   Really=result.has_key("total"))
        if (self.env_flag == "beta") or (self.env_flag == "BETA"):
            url = r"http://admin.crm.yunshuxie.com/v1/teacher/statistics/save/follow_record.json"
            date = time.time()
            params = {"phone": phone,"memberId": memberId,"content": "自动化测试%d"%(date)}
            logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
            str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
            print str_params
            self.resp = self.session.get(url=url, params=params)
            print self.resp.content
            result = json.loads(self.resp.content, encoding="utf8")
            logging.info(url + lianjiefu + self.resp.text + fengefu)
            expect = {"returnMsg": "", "returnCode": 0}
            assert result.has_key("returnCode") == expect.has_key("returnCode"), self.msg.format(Expect=expect.has_key("returnCode"),Really=result.has_key("returnCode"))
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],Really=result["returnCode"])
            assert result.has_key("returnMsg") == expect.has_key("returnMsg"), self.msg.format(Expect=expect.has_key("returnMsg"),
                                                                                       Really=result.has_key("returnMsg"))
    def test_02_statistics_saleList(self):
        """
        B端CRM->名著导读课程管理->流量绩效->累计移除学生数<br/>http://admin.crm.yunshuxie.com/v1/yearcard/statistics/saleList.htm<br/>{"sort": "classId","order": "asc","limit": "10","offset": "0"}<br/>{"userId": userId,"sort": "classId","order": "asc","limit": "10","offset": "0"}
        :return: True
        """
        url = r"http://admin.crm.yunshuxie.com/v1/yearcard/statistics/saleList.htm"
        params = {"sort": "classId","order": "asc","limit": "10","offset": "0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        self.resp = self.session.get(url=url, params=params)
        print self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"rows": "", "total": ""}
        userId = result["rows"][0]["userId"]
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect.has_key("rows"),
                                                                                 Really=result.has_key("rows"))
        assert result.has_key("total") == expect.has_key("total"), self.msg.format(Expect=expect.has_key("total"),
                                                                                   Really=result.has_key("total"))
        url = r"http://admin.crm.yunshuxie.com/v1/teacher/statistics/query/delete_Detail.htm"
        params = {"userId": userId,"sort": "classId","order": "asc","limit": "10","offset": "0"}
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect.has_key("rows"),
                                                                                 Really=result.has_key("rows"))
        assert result.has_key("total") == expect.has_key("total"), self.msg.format(Expect=expect.has_key("total"),
                                                                                   Really=result.has_key("total"))
    def test_03_statistics_grade_list(self):
        """
        B端CRM->名著导读课程管理->年级汇总报表<br/>http://admin.crm.yunshuxie.com/v1/yearcard/statistics/grade_list.htm<br/>{"sort": "classId","order": "asc","limit": "50","offset": "0"}
        :return: True
        """
        url = r"http://admin.crm.yunshuxie.com/v1/yearcard/statistics/grade_list.htm"
        params = {"sort": "classId","order": "asc","limit": "50","offset": "0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        self.resp = self.session.get(url=url, params=params)
        print self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"rows": "", "total": ""}
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect.has_key("rows"),
                                                                                 Really=result.has_key("rows"))
        assert result.has_key("total") == expect.has_key("total"), self.msg.format(Expect=expect.has_key("total"),
                                                                                   Really=result.has_key("total"))
    def test_04_statistics_daily_reports_list(self):
        """
        B端CRM->名著导读课程管理->日报<br/>http://admin.crm.yunshuxie.com/v1/yearcard/statistics/daily_reports_list.htm<br/>{"sort": "classId","order": "asc","limit": "50","offset": "0"}
        :return: True
        """
        url = r"http://admin.crm.yunshuxie.com/v1/yearcard/statistics/daily_reports_list.htm"
        params = {"sort": "classId","order": "asc","limit": "10","offset": "0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        self.resp = self.session.get(url=url, params=params)
        print self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"rows": "", "total": ""}
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect.has_key("rows"),
                                                                                 Really=result.has_key("rows"))
        assert result.has_key("total") == expect.has_key("total"), self.msg.format(Expect=expect.has_key("total"),
                                                                                   Really=result.has_key("total"))
    def test_05_statistics_daily_reports_Sum(self):
        """
        B端CRM->名著导读课程管理->日报<br/>http://admin.crm.yunshuxie.com/v1/yearcard/statistics/daily_reports_Sum.json<br/>
        :return: True
        """
        url = r"http://admin.crm.yunshuxie.com/v1/yearcard/statistics/daily_reports_Sum.json"
        self.resp = self.session.get(url=url)
        print self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"returnCode": 0, "data": ""}
        assert result.has_key("returnCode") == expect.has_key("returnCode"), self.msg.format(Expect=expect.has_key("returnCode"), Really=result.has_key("returnCode"))
        assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],Really=result["returnCode"])
        assert result.has_key("data") == expect.has_key("data"), self.msg.format(Expect=expect.has_key("data"),Really=result.has_key("data"))
    def test_06_organ_query_channeler_list(self):
        """
        B端CRM->渠道商->每日一句->学校详情<br/>http://admin.crm.yunshuxie.com/v1/bcrm/organ/query/channeler_list<br/>http://admin.crm.yunshuxie.com/v1/bcrm/organ/query/school_list<br/>{"sort": "organId", "order": "asc", "limit": "10", "offset": "0"}
        :return: True
        """
        url = r"http://admin.crm.yunshuxie.com/v1/bcrm/organ/query/channeler_list"
        params = {"sort": "organId", "order": "asc", "limit": "10", "offset": "0"}
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"rows": "", "total": ""}
        organId = result["rows"][0]["organId"]
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect.has_key("rows"),
                                                                                 Really=result.has_key("rows"))
        assert result.has_key("total") == expect.has_key("total"), self.msg.format(Expect=expect.has_key("total"),
                                                                                   Really=result.has_key("total"))
        url = r"http://admin.crm.yunshuxie.com/v1/bcrm/organ/query/school_list"
        params = {"parentOrganId": organId,"sort": "organId","order": "asc","limit": "10","offset": "0"}
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"rows": "", "total": ""}
        organId = result["rows"][0]["organId"]
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect.has_key("rows"),
                                                                                 Really=result.has_key("rows"))
        assert result.has_key("total") == expect.has_key("total"), self.msg.format(Expect=expect.has_key("total"),
                                                                                   Really=result.has_key("total"))
    def test_07_organ_query_channeler_Sum(self):
        """
        B端CRM->渠道商->每日一句<br/>http://admin.crm.yunshuxie.com/v1/bcrm/organ/query/channeler_Sum.json<br/>
        :return: True
        """
        url = r"http://admin.crm.yunshuxie.com/v1/bcrm/organ/query/channeler_Sum.json"
        self.resp = self.session.get(url=url)
        print self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"returnCode": 0, "data": ""}
        assert result.has_key("returnCode") == expect.has_key("returnCode"), self.msg.format(Expect=expect.has_key("returnCode"),Really=result.has_key("returnCode"))
        assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],Really=result["returnCode"])
        assert result.has_key("data") == expect.has_key("data"), self.msg.format(Expect=expect.has_key("data"),Really=result.has_key("data"))
    def test_08_yearcard_query_channeler_list(self):
        """B端CRM->渠道商->名著导读课->学校详情<br/>http://admin.crm.yunshuxie.com/v1/agent/yearcard/query/channeler_list<br/>{"sort": "organId", "order": "asc", "limit": "10", "offset": "0"}<br/>{"parentOrganId": organId,"sort": "organId","order": "asc","limit": "10","offset": "0"}
        :return: True
        """
        url = r"http://admin.crm.yunshuxie.com/v1/agent/yearcard/query/channeler_list"
        params = {"sort": "organId", "order": "asc", "limit": "10", "offset": "0"}
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"rows": 0, "total": ""}
        organId = result["rows"][0]["organId"]
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(
            Expect=expect.has_key("rows"),
            Really=result.has_key("rows"))
        assert result.has_key("total") == expect.has_key("total"), self.msg.format(Expect=expect.has_key("total"),
                                                                                 Really=result.has_key("total"))
        url = r"http://admin.crm.yunshuxie.com/v1/agent/yearcard/query/school_list"
        params = {"parentOrganId": organId,"sort": "organId","order": "asc","limit": "10","offset": "0"}
        self.resp = self.session.get(url=url, params=params)
        print self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"rows": 0, "total": ""}
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(
            Expect=expect.has_key("rows"),
            Really=result.has_key("rows"))
        assert result.has_key("total") == expect.has_key("total"), self.msg.format(Expect=expect.has_key("total"),
                                                                                   Really=result.has_key("total"))


    @classmethod
    def tearDownClass(self):
        pass

if __name__ == "__main__":
    unittest.main()