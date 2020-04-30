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
    """CRM 销售统计"""
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
    def test_01_day_sales(self):
        """销售统计-销售日报 <br/>http://admin.crm.yunshuxie.com/v1/crm/day/sales.json<br/> {"limit": "10","sort": "nowDate","order":"asc","offset": "0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/crm/day/sales.json"
        params = {"limit": "10" ,"sort": "nowDate" ,"order" :"asc" ,"offset": "0"}
        logging.info(url + lianjiefu + json.dumps(params ,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url ,params=params)
        print self.resp.content
        result = json.loads(self.resp.content ,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total" :3 ,"rows" :""}
        assert result.has_key("total" )==expect.has_key("total") ,self.msg.format(Expect=expect["total"]
                                                                                   ,Really=result["total"])
        assert isinstance(result["total"] ,int )==True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"]
                                                                                 ,Really=result["rows"])
    def test_02_week_sales(self):
        """销售统计-销售周报 <br/> http://admin.crm.yunshuxie.com/v1/crm/week/sales<br/> {"limit": "10","sort": "prductName","order":"asc","offset": "0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/crm/week/sales"
        params = {"limit": "10" ,"sort": "prductName" ,"order" :"asc" ,"offset": "0"}
        logging.info(url + lianjiefu + json.dumps(params ,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url ,params=params)
        print self.resp.content
        result = json.loads(self.resp.content ,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total" :3 ,"rows" :""}
        assert result.has_key("total" )==expect.has_key("total") ,self.msg.format(Expect=expect["total"]
                                                                                   ,Really=result["total"])
        assert isinstance(result["total"] ,int )==True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"]
                                                                                 ,Really=result["rows"])
    def test_03_month_sales(self):
        """销售统计-销售月报-用户销售数据 <br/>http://admin.crm.yunshuxie.com/v1/crm/month/sales.json<br/> {"limit": "10","sort": "nowDate","order":"asc","offset": "0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/crm/month/sales.json"
        params = {"limit": "10" ,"sort": "nowDate" ,"order" :"asc" ,"offset": "0"}
        logging.info(url + lianjiefu + json.dumps(params ,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url ,params=params)
        print self.resp.content
        result = json.loads(self.resp.content ,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total" :3 ,"rows" :""}
        assert result.has_key("total" )==expect.has_key("total") ,self.msg.format(Expect=expect["total"]
                                                                                   ,Really=result["total"])
        assert isinstance(result["total"] ,int )==True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"]
                                                                                 ,Really=result["rows"])
    def test_04_mounth_statistics_list(self):
        """销售统计-销售月报-产品销售数据 <br/>http://admin.crm.yunshuxie.com/v1/crm/sales/mounth_statistics_list.json<br/> {"limit": "10","sort": "month","order":"asc","offset": "0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/crm/sales/mounth_statistics_list.json"
        params = {"limit": "10" ,"sort": "month" ,"order" :"asc" ,"offset": "0"}
        logging.info(url + lianjiefu + json.dumps(params ,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url ,params=params)
        print self.resp.content
        result = json.loads(self.resp.content ,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total" :3 ,"rows" :""}
        assert result.has_key("total" )==expect.has_key("total") ,self.msg.format(Expect=expect["total"]
                                                                                   ,Really=result["total"])
        assert isinstance(result["total"] ,int )==True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"]
                                                                                 ,Really=result["rows"])
    def test_05_mounth_sales_detail(self):
        """销售统计-销售月报-新老用户销售数据 <br/> http://admin.crm.yunshuxie.com/v1/crm/month/sales_detail<br/>{"limit": "10","sort": "nowDate","order":"asc","offset": "0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/crm/month/sales_detail"
        params = {"limit": "10" ,"sort": "nowDate" ,"order" :"asc" ,"offset": "0"}
        logging.info(url + lianjiefu + json.dumps(params ,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url ,params=params)
        print self.resp.content
        result = json.loads(self.resp.content ,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total" :3 ,"rows" :""}
        assert result.has_key("total" )==expect.has_key("total") ,self.msg.format(Expect=expect["total"]
                                                                                   ,Really=result["total"])
        assert isinstance(result["total"] ,int )==True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"]
                                                                                 ,Really=result["rows"])
    def test_06_year_sales(self):
        """销售统计-销售年报 <br/>http://admin.crm.yunshuxie.com/v1/crm/year/sales.json<br/> {"limit": "10", "sort": "nowDate", "order": "asc", "offset": "0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/crm/year/sales.json"
        params = {"limit": "10", "sort": "nowDate", "order": "asc", "offset": "0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url, params=params)
        print self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total": 3, "rows": ""}
        assert result.has_key("total") == expect.has_key("total"), self.msg.format(Expect=expect["total"],
                                                                                   Really=result["total"])
        assert isinstance(result["total"], int) == True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"],
                                                                                 Really=result["rows"])
    def test_07_platinum_day_study(self):
        """销售统计-年卡销售数据 <br/>http://admin.crm.yunshuxie.com/v1/platinum/day_study<br/> {"limit": "10", "sort": "payDate", "order": "DESC", "offset": "0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/platinum/day_study"
        params = {"limit": "10", "sort": "payDate", "order": "DESC", "offset": "0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url, params=params)
        print self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total": 3, "rows": ""}
        assert result.has_key("total") == expect.has_key("total"), self.msg.format(Expect=expect["total"],
                                                                                   Really=result["total"])
        assert isinstance(result["total"], int) == True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"],
                                                                                 Really=result["rows"])
    def test_08_online_offline(self):
        """销售统计-热门课程销售排行榜-当天 <br/> http://admin.crm.yunshuxie.com/ysxserviceuser/get/sales/ranking/online/offline.html<br/>{"startDate": date,"endDate": date,"order":"desc"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/ysxserviceuser/get/sales/ranking/online/offline.html"
        date = time.strftime("%Y-%m-%d" ,time.localtime(time.time()))
        params = {"startDate": date ,"endDate": date ,"order" :"desc"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url, params=params)
        print self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total": 3, "rows": ""}
        assert result.has_key("total") == expect.has_key("total"), self.msg.format(Expect=expect["total"],
                                                                                   Really=result["total"])
        assert isinstance(result["total"], int) == True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"],
                                                                                 Really=result["rows"])
    def test_09_ranking_list(self):
        """销售统计-热门课程销售排行榜-当天-查看《每日一句》明细 <br/> http://admin.crm.yunshuxie.com/v1/sale/performance/sales/ranking/list<br/>{"productName": "每日一句","startDate": "2019-05-23","endDate": "2019-05-23",<br/>"deptId": "-1","sort": "userId","order": "DESC","limit": "10","offset": "0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/sale/performance/sales/ranking/list"
        date = time.strftime("%Y-%m-%d" ,time.localtime(time.time()))
        params = {"productName": "每日一句" ,"startDate": date ,"endDate": date ,"deptId": "-1" ,"sort": "userId"
                  ,"order": "DESC" ,"limit": "10" ,"offset": "0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url, params=params)
        print self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total": 3, "rows": ""}
        assert result.has_key("total") == expect.has_key("total"), self.msg.format(Expect=expect["total"],
                                                                                   Really=result["total"])
        assert isinstance(result["total"], int) == True
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"],
                                                                                 Really=result["rows"])
    def test_10_get_echarts(self):
        """销售统计-热门课程销售排行榜-当天-查看图表 <br/>http://admin.crm.yunshuxie.com/ysxserviceuser/get/echarts<br/>{"startDate":date,"endDate":date}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/ysxserviceuser/get/echarts"
        date = time.strftime("%Y-%m-%d" ,time.localtime(time.time()))
        params = {"startDate" :"2019-01-01" ,"endDate" :"2019-12-31"}
        #params = {"startDate" :date ,"endDate" :date}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url, params=params)
        print self.resp.content
        result = json.loads(self.resp.content, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"fourNovelsNum": "", "oneToOneNum": ""}
        assert result.has_key("fourNovelsNum") == expect.has_key("fourNovelsNum"), self.msg.format(Expect=expect["fourNovelsNum"],
                                                                                                   Really=result["fourNovelsNum"])
        assert result.has_key("oneToOneNum") == expect.has_key("oneToOneNum"), self.msg.format(Expect=expect["oneToOneNum"],
                                                                                               Really=result["oneToOneNum"])
    @classmethod
    def tearDownClass(self):
        pass

if __name__ == "__main__":
    unittest.main()