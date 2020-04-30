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
class Ysx_Crm_KanTuXieHuaXueYuanGuanLi(unittest.TestCase):
    """CRM 看图写话学员管理"""
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
    def test_01_idiomServiceteacher(self):
        """看图写话分配老师 <br/> http://admin.crm.yunshuxie.com/admin/writing_material/query/idiomServiceteacher.htm<br/>{"teacherType": "11","limit": "10",<br/>"order": "asc","offset": "0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/admin/writing_material/query/idiomServiceteacher.htm"
        params = {"teacherType": "11","limit": "10","order": "asc","offset": "0"}
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
    def test_02_daily_list(self):
        """看图写话日报 <br/> http://admin.crm.yunshuxie.com/v1/elementary_course/query/daily_list.json</br/>{"type":"73","sort":"nowDate","order":"asc","limit":"32","offset":"0"}
        :param: order == asc
        :param: limit == 10
        :param: offset == 0
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/elementary_course/query/daily_list.json"
        params = {"type":"73","sort":"nowDate","order":"asc","limit":"32","offset":"0"}
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
    def test_03_daily_list(self):
        """体验课日报 <br/> http://admin.crm.yunshuxie.com/v1/elementary_course/query/daily_list.json<br/>{"type":"78","sort":"nowDate","order":"asc","limit":"32","offset":"0"}
        :param: order == asc
        :param: limit == 10
        :param: offset == 0
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/v1/elementary_course/query/daily_list.json"
        params = {"type":"78","sort":"nowDate","order":"asc","limit":"32","offset":"0"}
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
    def test_04_idiom_classdetail(self):
        """看图写话班级统计数据 <br/> http://admin.crm.yunshuxie.com/admin/writing_material/idiom_classdetail.json<br/>{"teacherType":"11","sort":"nowDate",<br/>"order":"asc","limit":"20","offset":"0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/admin/writing_material/idiom_classdetail.json"
        params = {"teacherType":"11","sort":"nowDate","order":"asc","limit":"20","offset":"0"}
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
    def test_05_picture_basic_distribution(self):
        """看图写话设备分配 <br/> http://admin.crm.yunshuxie.com/admin/writing_material/query/picture_basic_distribution.json<br/>{"teacherType":"11","sort":"nowDate",</br>"order":"asc","limit":"20","offset":"0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/admin/writing_material/query/picture_basic_distribution.json"
        params = {"teacherType":"11","sort":"nowDate","order":"asc","limit":"20","offset":"0"}
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
    def test_06_pictureStudent_detail(self):
        """看图写话学员学习明细表 <br/>http://admin.crm.yunshuxie.com/admin/writing_material/pictureStudent_detail.json<br/> {"sort": "nowDate","order": "asc",<br/>"limit": "10","offset": "0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/admin/writing_material/pictureStudent_detail.json"
        params = {"sort": "nowDate","order": "asc","limit": "10","offset": "0"}
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
    def test_07_picAuditionStudent_detail(self):
        """体验课学员明细 <br/> http://admin.crm.yunshuxie.com/admin/writing_material/picAuditionStudent_detail.json<br/>{"sort":"nowDate",</br>"order":"asc","limit":"10","offset":"0"}
        :return True:
        """
        url = r"http://admin.crm.yunshuxie.com/admin/writing_material/picAuditionStudent_detail.json"
        params = {"sort":"nowDate","order":"asc","limit":"10","offset":"0","_":"1558603211137"}
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