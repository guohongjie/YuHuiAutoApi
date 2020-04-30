#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import unittest
import json
from app.base.pythonProject.base.log import TestLog,fengefu,lianjiefu
from app.base.pythonProject.base.py_redis import fromRedis
from app.base.pythonProject.base.getCookies import get_app_cookie,get_wacc_admin_cookie
import time
#logging = TestLog().getlog()
class BearWord_Student_and_Teacher_Test(unittest.TestCase):
    """<br>首页，账号登录<br>1.用户登录-我的作品展示列表<br>2.用户登录-我的作品展示列表&优秀作品&未点评&已点评<br>5.查询总结语列表<br>6.用户登录-评价老师接口（查看教师已点评的课程作品）（遍历进入课程，获取是否已分配服务老师）（找到存在服务老师的数据，进行评价）<br>7.教师登录：推荐/取消推荐优秀作业-取消推荐<br>8.教师登录：作业退回接口-教师端<br>9.教师登录：驳回接口-教师端"""
    @classmethod
    @fromRedis(getKey=["wacc_mobile_env_flag","wacc_mobile_env_num","make_user_phones"])
    def setUpClass(self,getKey):
        self.env_flag = getKey["wacc_mobile_env_flag"]
        self.env_num = getKey["wacc_mobile_env_num"]
        self.phone = getKey["make_user_phones"]
        self.timestamp = "%d" % (time.time())
        self.session = requests.Session()
        cookies = {"env_flag": self.env_flag,
                   "env_num": self.env_num}  # get_app_cookie(self.env_flag,self.env_num) #未进行登录展示接口
        self.header = {"Connection": "keep-alive", "Content-Type": "application/x-www-form-urlencoded",
                       "User-Agent": "BearWord/1.0.0 (iPhone; iOS 12.3.1; Scale/3.00)"}
        self.msg = """\n        Expect:  {Expect}-*-\n        Really:  {Really}"""  # 校验HTTP返回代码
        self.session.headers = self.header
        self.session.cookies = requests.utils.cookiejar_from_dict(cookies)
    def test_01_bear_student_myWorkList(self):
        """用户登录-我的作品展示列表<br>http://mobile.yunshuxie.com/v1/bear/student/myWorkList.htm<br/>{"type":"4"全部作品,"page":"1"}"""
        url = r"http://mobile.yunshuxie.com" + r"/v1/bear/student/myWorkList.htm"
        params = {"type": "4", "page": "1"}
        cookies = get_app_cookie("罐罐熊APP",self.env_flag, self.env_num, user=self.phone)
        # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = requests.post(url=url, headers=self.header, data=params, cookies=cookies)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        # logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"returnCode": "0"}
        if result["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
    def test_02_bear_student_myWorkList(self):
        """用户登录-我的作品展示列表<br>http://mobile.yunshuxie.com/v1/bear/student/myWorkList.htm<br/>{"type":"3"优秀作品,"page":"1"}"""
        url = r"http://mobile.yunshuxie.com" + r"/v1/bear/student/myWorkList.htm"
        params = {"type": "3", "page": "1"}
        cookies = get_app_cookie("罐罐熊APP",self.env_flag, self.env_num, user=self.phone)
        # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = requests.post(url=url, headers=self.header, cookies=cookies, data=params)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        # logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"returnCode": "0"}
        if result["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
    def test_03_bear_student_myWorkList(self):
        """用户登录-我的作品展示列表<br>http://mobile.yunshuxie.com/v1/bear/student/myWorkList.htm<br/>{"type":"2"未点评,"page":"1"}"""
        url = r"http://mobile.yunshuxie.com" + r"/v1/bear/student/myWorkList.htm"
        params = {"type": "2", "page": "1"}
        cookies = get_app_cookie("罐罐熊APP",self.env_flag, self.env_num, user=self.phone)
        # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = requests.post(url=url, headers=self.header, cookies=cookies, data=params)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        # logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"returnCode": "0"}
        if result["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
    def test_04_bear_student_myWorkList(self):
        """用户登录-我的作品展示列表<br>http://mobile.yunshuxie.com/v1/bear/student/myWorkList.htm<br/>{"type":"1"已点评,"page":"1"}"""
        url = r"http://mobile.yunshuxie.com" + r"/v1/bear/student/myWorkList.htm"
        params = {"type": "1", "page": "1"}
        cookies = get_app_cookie("罐罐熊APP",self.env_flag, self.env_num, user=self.phone)
        # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = requests.post(url=url, headers=self.header, cookies=cookies, data=params)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        # logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"returnCode": "0"}
        if result["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
    def test_05_bear_student_summary(self):
        """用户登录-查询总结语列表<br>http://mobile.yunshuxie.com/v1/bear/student/summary.htm<br/>"""
        url = r"http://mobile.yunshuxie.com" + r"/v1/bear/student/myWorkList.htm"
        cookies = get_app_cookie("罐罐熊APP",self.env_flag, self.env_num, user=self.phone)
        params = {"type": "4"}
        self.resp = requests.post(url=url, headers=self.header, cookies=cookies, data=params)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        # logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"returnCode": "0"}
        if result["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
    def test_06_bear_student_commentTeacher(self):
        """用户登录-评价老师接口<br>http://mobile.yunshuxie.com/v1/bear/student/commentTeacher.htm<br/>"""
        url = r"http://mobile.yunshuxie.com" + r"/v1/bear/student/myWorkList.htm"
        params = {"type": "1", "page": "1"}  # 查看教师已点评的课程作品
        cookies = get_app_cookie("罐罐熊APP",self.env_flag, self.env_num, user=self.phone)
        # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        self.resp = requests.post(url=url, headers=self.header, cookies=cookies, data=params)
        result = json.loads(self.resp.text, encoding="utf8")
        # logging.info(url + lianjiefu + self.resp.text + fengefu)
        workId_list = []
        if result["data"]["list"]:
            for m in result["data"]["list"]:
                workId_list.append(m["workId"])
            # 查看课程作品，判断是否存在teacherId
            for workId in workId_list:
                url = r"http://mobile.yunshuxie.com" + "/v1/bear/student/workInfo.htm"
                params = {"workId": workId, "deviceId": "629a5eb2a857f86dadaa043b414984f2"}
                # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
                str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
                self.resp = requests.post(url=url, headers=self.header, cookies=cookies, data=params)
                result = json.loads(self.resp.text, encoding="utf8")
                # logging.info(url + lianjiefu + self.resp.text + fengefu)
                if result["data"]["teacherId"] != "":
                    workId = result["data"]["workId"]
                    teacherId = result["data"]["teacherId"]
                    break
                else:
                    print u"未存在已点评已分配教师的作品数据"
                    raise Exception, u"未存在已点评已分配教师的作品数据"
            url = r"http://mobile.yunshuxie.com" + r"/v1/bear/student/commentTeacher.htm"
            params = {"workId": workId, "teacherId": teacherId, "commentContent": "测试评价教师功能", "commentStar": "5",
                      "isApp": "2"}
            str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
            print str_params
            #logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
            cookies = get_app_cookie("罐罐熊APP",self.env_flag, self.env_num, user=self.phone)
            self.resp = requests.post(url=url, headers=self.header, cookies=cookies, data=params)
            print self.resp.text
            result = json.loads(self.resp.text, encoding="utf8")
            # logging.info(url + lianjiefu + self.resp.text + fengefu)
            expect = {"returnCode": "0"}
            if result["returnCode"] == "0" or result["returnCode"] == 0:
                assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                     Really=result["returnCode"])
            else:
                assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                     Really=result["returnCode"])
        else:
            print u"未存在教师已点评的课程作品数据"
            raise Exception, u"未存在教师已点评的课程作品数据"
    @fromRedis(getKey=["bearWord_timelineId"])
    def test_07_v1_bear_teacher_recommend_job(self,getKey):
        """老师端：推荐/取消推荐优秀作业-取消推荐<br>https://mobile.yunshuxie.com/v1/bear/teacher/recommend_job.htm.htm<br>{"timeLineId":"","excellence":"0"}"""
        bearWord_timelineId = getKey["bearWord_timelineId"]
        if bearWord_timelineId:
            url = r"https://mobile.yunshuxie.com"+r"/v1/bear/teacher/recommend_job.htm"
            params = {"timeLineId":bearWord_timelineId,"excellence":"0"}
            # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
            str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
            print str_params
            cookies = get_app_cookie("罐罐熊APP",self.env_flag, self.env_num, self.phone)
            self.session.cookies = cookies
            self.resp = self.session.post(url=url,data=params)
            print self.resp.text
            result = json.loads(self.resp.text, encoding="utf8")
            #logging.info(url + lianjiefu + self.resp.content + fengefu)
            expect = {"returnCode": "0"}
            if result["returnCode"] == "0" or result["returnCode"] == 0:
                assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                     Really=result["returnCode"])
            else:
                assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                     Really=result["returnCode"])
        else:
            print u"当前教师未存在待批改作业"
            raise Exception,u"当前教师未存在待批改作业"
    @fromRedis(getKey=["bearWord_workId"])
    def test_08_bear_teacher_reject_job(self,getKey):
        """作业退回接口-教师端<br>https://mobile.yunshuxie.com/v1/bear/teacher/return_job.htm<br/>{"timeLineId":""}"""
        if self.env_flag != "beta":
            print u"当前运行环境非beta,跳过打卡接口"
        else:
            workId = getKey["bearWord_workId"]
            if workId:
                url = r"http://mobile.yunshuxie.com" + "/v1/bear/teacher/return_job.htm"
                params = {"timeLineId":workId}
                #logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
                str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
                print str_params
                self.resp = self.session.post(url=url, data=params)
                print self.resp.text
                result = json.loads(self.resp.text, encoding="utf8")
                #logging.info(url + lianjiefu + self.resp.text + fengefu)
                expect = {"returnCode": "0"}
                if result["returnCode"] == "0" or result["returnCode"] == 0:
                    assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                         Really=result["returnCode"])
                else:
                    assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                         Really=result["returnCode"])
            else:
                print u"当前页面不存在章节数据"
                raise Exception, u"当前页面不存在章节数据"
    @fromRedis(getKey=["bearWord_workId"])
    def test_09_bear_teacher_reject_job(self,getKey):
        """ 驳回接口-教师端<br>https://mobile.yunshuxie.com/v1/bear/teacher/reject_job.htm<br/>{"timeLineId":"","reasonId":"","status":""}"""
        if self.env_flag != "beta":
            print u"当前运行环境非beta,跳过打卡接口"
        else:
            workId = getKey["bearWord_workId"]
            if workId:
                url = r"http://mobile.yunshuxie.com" + "/v1/bear/teacher/reject_job.htm"
                params = {"timeLineId":workId,"reasonId":"1","status":"1"}
                #logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
                str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
                print str_params
                self.resp = self.session.post(url=url, data=params)
                print self.resp.text
                result = json.loads(self.resp.text, encoding="utf8")
                #logging.info(url + lianjiefu + self.resp.text + fengefu)
                expect = {"returnCode": "0"}
                if result["returnCode"] == "0" or result["returnCode"] == 0:
                    assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                         Really=result["returnCode"])
                else:
                    assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                         Really=result["returnCode"])
            else:
                print u"当前页面不存在章节数据"
                raise Exception, u"当前页面不存在章节数据"

    @classmethod
    def tearDownClass(self):
        pass
