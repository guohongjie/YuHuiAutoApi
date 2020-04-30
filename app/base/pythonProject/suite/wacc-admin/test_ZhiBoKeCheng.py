#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import unittest
import re
import json
from requests_toolbelt import MultipartEncoder
from app.base.pythonProject.base.log import TestLog,fengefu,lianjiefu
from app.base.pythonProject.base.py_redis import MyRedis
logging = TestLog().getlog()
class zhiBoKeCheng_Test(unittest.TestCase):
    #"course_schema"
    @classmethod
    def setUpClass(self):
        """起始方法
        #:return:  cookies """
        redis = MyRedis()
        env_flag = redis.str_get("uploadFile_env_flag")
        env_num = redis.str_get("uploadFile_env_num")
        userName = redis.str_get("username")
        pwd = redis.str_get("pwd")
        self.cookies = requests.cookies.RequestsCookieJar()
        self.cookies.set('env_flag', env_flag)  #设置测试环境
        self.cookies.set("env_num",env_num)  #设置环境号
        data = {"userName":userName,"pwd":pwd}
        self.url = "https://www.yunshuxie.com"+"/v5/web/account/login.htm"
        caseHeaders = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","Accept": "application/json, text/javascript, */*; q=0.01","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9","Connection": "keep-alive","Host": "www.yunshuxie.com","Upgrade-Insecure-Requests": "1"}
        self.resp = requests.post(self.url, data=data, headers=caseHeaders ,cookies=self.cookies)  #登录admin测试环境,记录cookies
        print self.resp.content
        #logging.info(self.url + lianjiefu + self.resp.text + fengefu)
        self.cookies.update(self.resp.cookies)
    def test_1_TianJiaZhiBKeCheng(self):
        """添加直播课程<br/>https://admin.yunshuxie.com/v1/admin/big_live/save_biglive_course.json<br/>"""
        self.caseStatusCode = 200
        self.caseExpectDatas ={"returnCode":"0","returnMsg":"操作成功","data":{"bigliveCourseNameLike":"","bigliveRemarks":"","orderBy":"","beginDateChar":"2019-04-23","endDate":"2019-04-23 00:00:00","endDateBegin":"","endDateCharAll":"2019-04-23 00:00:00","beginDate":"2019-04-23 00:00:00","creadeDate":"2019-04-25 16:40:00","teacherName":"","updateDateEnd":"","teacherNameLike":"","endDateChar":"2019-04-23","bigliveDescribe":"自动化测试","bigliveCourseName":"自动化测试","imgUrlLike":"","coureseUrlLike":"","createUserId":"1203933","creadeDateBegin":"","updateDateCharAll":"","creadeDateChar":"2019-04-25","updateDate":"","imgUrl":"https://oss-ysx-pic.yunshuxie.com/pdf/2019/04/25/15/1556178195842fsavyl.png","bigliveDescribeLike":"","updateDateBegin":"","endDateEnd":"","bigliveCourseId":"51","beginDateCharAll":"2019-04-23 00:00:00","beginDateEnd":"","coureseUrl":"自动化测试","updateDateChar":"","bigliveType":"-1","beginDateBegin":"","bigliveRemarksLike":"","creadeDateCharAll":"2019-04-25 16:40:00","creadeDateEnd":""}}
        params = {"bigliveCourseId":"-1","file": "","imgUrl":r"https://oss-ysx-pic.yunshuxie.com/pdf/2019/04/25/15/1556178195842fsavyl.png",
        "bigliveCourseName":"自动化测试","bigliveCourseName": "自动化测试","bigliveType": "-1",
        "beginDates": "2019-04-23 00:00:00","endDates": "2019-04-23 00:00:00","coureseUrl": "自动化测试","bigliveDescribe": "自动化测试",
        "beginDates": "2019-04-23 00:00:00","endDates": "2019-04-23 00:00:00"}
        self.url = r"https://admin.yunshuxie.com/v1/admin/big_live/save_biglive_course.json"
        method = "GET"
        caseHeaders = {"Origin":	"https://admin.yunshuxie.com", "Accept-Encoding":"gzip, deflate, br","Host":"admin.yunshuxie.com",
          "Accept-Language":"zh-CN,zh;q=0.9",
          "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
          "Content-Type":"multipart/form-data;boundary=----WebKitFormBoundary99ZuWoGJvTEtpr5b",
          "Accept":"application/json, text/javascript, */*; q=0.01",
          "Cache-Control":"no-cache","X-Requested-With":"XMLHttpRequest","Connection":"keep-alive",
          "Referer":"https://admin.yunshuxie.com//v1/admin/big_live/goto/edit_biglive_course.htm?initialWidth=1007&childId=example-538&parentTitle=%E4%BA%91%E8%88%92%E5%86%99%E5%90%8E%E5%8F%B0%E7%AE%A1%E7%90%86%E7%B3%BB%E7%BB%9F&parentUrl=https%3A%2F%2Fadmin.yunshuxie.com%2Fcommon_index%2Findex.htm"}
        data = MultipartEncoder(params)
        caseHeaders["Content-Type"] = data.content_type
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = requests.post(self.url, data=data, headers=caseHeaders,cookies=self.cookies)
        print self.resp.content
        #logging.info(self.url + lianjiefu + self.resp.text + fengefu)
        msg = """
        Expect:  {Expect}-*-
        Really:  {Really}"""  #校验HTTP返回代码
        assert self.caseStatusCode==self.resp.status_code,msg.format(Expect=self.caseStatusCode,Really=self.resp.status_code)
        respMsg = self.resp.content  #返回值
        caseExpectDatas = self.caseExpectDatas  #xls 校验值
        def assertKey(value1,value2):
            dictvalue1 = value1
            dictvalue2 = value2
            if type(dictvalue2).__name__ == "dict":
                for key,value in dictvalue2.items():
                    if dictvalue1.has_key(key):
                        if type(value).__name__ == "dict":
                            assertKey(dictvalue1[key],dictvalue2[key])
                        elif type(value).__name__ == "list":
                            assertKey(dictvalue1[key],dictvalue2[key])
                    else:
                        msg = """\n        Expect:  {Expect}-*-\n        Really:  {Really}"""
                        return key
            elif type(dictvalue2).__name__ == "list":
                for list_index in range(len(dictvalue2)):
                    assertKey(dictvalue1[list_index],dictvalue2[list_index])
        value1 = self.caseExpectDatas
        value2 = json.loads(re.match(".*?({.*}).*", self.resp.content, re.S).group(1))
        keyValue = assertKey(value1,value2)
        if keyValue:
            assert keyValue=="Error",msg.format(Expect=keyValue,Really="Error")
        #print self.resp.content
    def test_2_ShanChuZhiBoKeCheng(self):
        """查询直播课程,并删除直播课程<br/>https://admin.yunshuxie.com/v1/admin/big_live/delete_bigliveCourse.htm<br/>"""
        self.caseStatusCode = 200
        self.url = r"https://admin.yunshuxie.com/v1/admin/big_live/query_biglive_course_list.json"
        params = {"bigliveCourseId": "-1","bigliveCourseName": "%E8%87%AA%E5%8A%A8%E5%8C%96%E6%B5%8B%E8%AF%95","order": "asc","limit": "10","offset": "0","_": "1556182101548"}
        caseHeaders = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","X-Requested-With": "XMLHttpRequest"}
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = requests.get(url=self.url,params=params,headers=caseHeaders,cookies=self.cookies)
        print self.resp.content
        #logging.info(self.url + lianjiefu + self.resp.text + fengefu)
        dict_resp = json.loads(self.resp.content)
        self.url = r"https://admin.yunshuxie.com/v1/admin/big_live/delete_bigliveCourse.htm"
        self.caseExpectDatas = {u"returnCode":u"0","returnMsg":u"操作成功",u"data":{}}
        for bigliveCourseId in  [query_msg["bigliveCourseId"] for query_msg in dict_resp["rows"]]:
            self.resp = requests.post(url=self.url,data={"bigliveCourseId":bigliveCourseId},headers=caseHeaders,cookies=self.cookies)
            print self.resp.content
            #logging.info(self.url + lianjiefu + self.resp.text + fengefu)
            respMsg = self.resp.content  # 返回值
            caseExpectDatas = self.caseExpectDatas  # xls 校验值
            msg = """\n        Expect:  {Expect}-*-\n        Really:  {Really}"""  #校验HTTP返回代码
            assert self.caseStatusCode == self.resp.status_code, msg.format(Expect=self.caseStatusCode,
                                                                       Really=self.resp.status_code)

            assert caseExpectDatas == json.loads(self.resp.content,encoding="utf8"),msg.format(Expect=caseExpectDatas,
                                                                       Really=self.resp.content)
    @classmethod
    def tearDownClass(self):
        """测试结束后执行,断言Req==Resp
        :return:  True OR False"""
        
        pass
if __name__ == "__main__":
    unittest.main()