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
class Ysx_Crm_MeiRiYiDuanZuoWenSuCaiKe(unittest.TestCase):
    """CRM 每日一段作文素材课"""
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
    def test_01_writing_material_order(self):
        """素材课日报查询 <br/> http://admin.crm.yunshuxie.com/admin/writing_material/query/writing_material_order.json<br/>{"sort": "nowDate","order": "asc","limit": "3",<br/>"offset": "0","_": "1558510544182"}
        :param: sort == nowDate
        :param: order == asc
        :param: limit == 3
        :param: offset == 0
        :return limit==3:
        """
        url = r"http://admin.crm.yunshuxie.com/admin/writing_material/query/writing_material_order.json"
        params = {"sort": "nowDate","order": "asc","limit": "3","offset": "0","_": "1558510544182"}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total":3,"rows":""}
        assert result["total"]==expect["total"],self.msg.format(Expect=expect["total"],Really=result["total"])
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"],Really=result["rows"])
    def test_02_writing_material_order(self):
        """素材课日报查询 <br/> http://admin.crm.yunshuxie.com/admin/writing_material/query/writing_material_order.json<br/>{"sort": "nowDate","order": "asc",<br/>"limit": "0","offset": "0","_": "1558510544182"}
        :param: sort == nowDate
        :param: order == asc
        :param: limit == 3
        :param: offset == 0
        :return limit==0:
        """
        url = r"http://admin.crm.yunshuxie.com/admin/writing_material/query/writing_material_order.json"
        params = {"sort": "nowDate","order": "asc","limit": "0","offset": "0","_": "1558510544182"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total":0,"rows":""}
        assert result["total"]==expect["total"],self.msg.format(Expect=expect["total"],Really=result["total"])
        assert result.has_key("rows") == expect.has_key("rows"), self.msg.format(Expect=expect["rows"],Really=result["rows"])
    def test_03_writing_equipment_distribution(self):
        """素材课设备分配表 <br/> http://admin.crm.yunshuxie.com/admin/writing_material/query/writing_equipment_distribution.json<br/>{"sort": "nowDate","order": "asc",<br/> "limit": "1","offset": "0","_": "1558510544182"}
        :param: sort == nowDate
        :param: order == asc
        :param: limit == 3
        :param: offset == 0
        :return limit==0:
        """
        url = r"http://admin.crm.yunshuxie.com/admin/writing_material/query/writing_equipment_distribution.json"
        params = {"sort": "nowDate","order": "asc","limit": "1","offset": "0","_": "1558510544182"}
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
    def test_04_writing_student_detail(self):
        """素材课学员明细 <br/>http://admin.crm.yunshuxie.com/admin/writing_material/student_detail<br/>{"type": "-1","phone":"", "saleName":"", "moocClassName":"",<br/> "courseHoursTitle":"","wecahtNum": "bjhyysx2","friend": "1",<br/> "sort": "nowDate","order": "asc","limit": "1",<br/> "offset": "0","_": "1558516779198"}
        :return limit==0:
        """
        url = r"http://admin.crm.yunshuxie.com/admin/writing_material/student_detail"
        params = {"type": "-1","phone":"", "saleName":"", "moocClassName":"", "courseHoursTitle":"","wecahtNum": "bjhyysx2","friend": "1","sort": "nowDate","order": "asc","limit": "1","offset": "0","_": "1558516779198"}
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
    def test_05_writing_student_detail(self):
        """素材课学员明细 <br/>http://admin.crm.yunshuxie.com/admin/writing_material/student_detail<br/>{"type": "1","phone":"", "saleName":"", "moocClassName":"",<br/> "courseHoursTitle":"","wecahtNum": "bjhyysx2","friend": "0",<br/> "sort": "nowDate","order": "asc","limit": "1","offset": "0","_": "1558516779198"}
        :return limit==0:
        """
        url = r"http://admin.crm.yunshuxie.com/admin/writing_material/student_detail"
        params = {"type": "1","phone":"", "saleName":"", "moocClassName":"", "courseHoursTitle":"","wecahtNum": "bjhyysx2","friend": "0","sort": "nowDate","order": "asc","limit": "1","offset": "0","_": "1558516779198"}
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
    def test_06_writing_class_detail(self):
        """素材课学员明细 <br/>http://admin.crm.yunshuxie.com/admin/writing_material/class_detail<br/>{"className":"","saleName":"","sort":"nowDate",<br/>"order":"asc","limit": "1","offset": "0","_": "1558517996751"}
        :return limit==0:
        """
        url = r"http://admin.crm.yunshuxie.com/admin/writing_material/class_detail"
        params = {"className": "","saleName": "","sort": "nowDate","order": "asc","limit": "1","offset": "0","_": "1558517996751"}
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
        # moocClassId = result["rows"][0]["moocClassId"]
        # url = r"https://admin.crm.yunshuxie.com/admin/writing_material/create_posters.htm"
        # params = {"moocClassId":moocClassId,"type":"1"}
        # self.resp = self.session.get(url=url, params=params)
        # result_moocClassId = len(eval(self.resp.content))
        # print self.resp.content
        # assert result_moocClassId > 0, self.msg.format(Expect=moocClassId, Really=result_moocClassId)
    def test_07_serviceteacher(self):
        """素材课分配老师 <br/>http://admin.crm.yunshuxie.com/admin/writing_material/query/serviceteacher.json<br/>{"sort": "userId","order": "asc",<br/> "limit": "10","offset":"0"}
        :return limit==0:
        """
        url = r"http://admin.crm.yunshuxie.com/admin/writing_material/query/serviceteacher.json"
        params = {"sort": "userId","order": "asc","limit": "10","offset":"0"}
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
    def test_08_new_member_activity(self):
        """素材课每周新增用户活跃度<br/>http://admin.crm.yunshuxie.com/admin/writing_material/new_member_activity<br/>{"startDate": "","endDate": "","sort": "dates",<br/>"order": "DESC","limit": "10","offset": "0"}
        :return rows&total:
        """
        url = r"http://admin.crm.yunshuxie.com/admin/writing_material/new_member_activity"
        params = {"startDate": "","endDate": "","sort": "dates","order": "DESC","limit": "10","offset": "0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total":0,"rows":""}
        assert result.has_key("total")==expect.has_key("total"),self.msg.format(Expect=expect["total"],Really=result["total"])
        assert result.has_key("rows")==expect.has_key("rows"),self.msg.format(Expect=expect["rows"],Really=result["rows"])
    def test_09_sales(self):
        """素材课分年级销售情况<br/>http://admin.crm.yunshuxie.com/admin/writing_material/sales<br/>{"sort": "dates","order": "DESC",<br/>"limit": "1","offset": "0"}
        :return rows&total:
        """
        url = r"http://admin.crm.yunshuxie.com/admin/writing_material/sales"
        params = {"sort": "dates","order": "DESC","limit": "1","offset": "0"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.get(url=url,params=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"total":0,"rows":""}
        assert result.has_key("total")==expect.has_key("total"),self.msg.format(Expect=expect["total"],Really=result["total"])
        assert result.has_key("rows")==expect.has_key("rows"),self.msg.format(Expect=expect["rows"],Really=result["rows"])

    @classmethod
    def tearDownClass(self):
        pass

if __name__ == "__main__":
    unittest.main()