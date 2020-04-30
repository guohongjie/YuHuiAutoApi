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
class BearWord_Teacher_Test(unittest.TestCase):
    """<br>首页,教师端操作<br>1.admin平台-运营管理-罐罐熊管理-添加罐罐熊老师-查询用户手机号<br>2.admin-添加用户手机号为教师<br>3.APP-个人中心-开启通知并判断是否教师角色<br>4.罐罐熊-教师端-个人中心-接收作业开关-关闭<br>5.罐罐熊-教师端-个人中心-接收作业开关-开启<br>6.admin-查询用户作业详情<br>7.admin-用户指定分配服务老师<br>8.admin-用户重新分配指定分配服务老师<br>9.老师端：待批改列表<br>10.老师端：用户作业详情<br>11.老师端：驳回理由列表<br>12.老师端：校验用户是否重新提交作业<br>13.老师端：上传批改语音接口<br>14.老师端：批改作业保存<br>15.老师端：批改记录<br>16.老师端：推荐/取消推荐优秀作业--推荐"""
    @classmethod
    @fromRedis(getKey=["wacc_mobile_env_flag","wacc_mobile_env_num","make_user_phones"])
    def setUpClass(self,getKey):
        self.env_flag = "beta"#getKey["wacc_mobile_env_flag"]
        self.env_num = "1"#getKey["wacc_mobile_env_num"]
        self.phone = getKey["make_user_phones"]
        self.timestamp = "%d"%(time.time())
        self.session = requests.Session()
        header = {"Connection": "keep-alive", "Content-Type": "application/x-www-form-urlencoded","User-Agent": "BearWord/1.0.0 (iPhone; iOS 12.3.1; Scale/3.00)"}
        self.msg = """\n        Expect:  {Expect}-*-\n        Really:  {Really}"""  # 校验HTTP返回代码
        self.session.headers = header
    @fromRedis(setKey=["bearWord_Teacher_memberId"])
    def test_01_admin_bear_course_query_bearUser_list(self):
        """admin平台-运营管理-罐罐熊管理-添加罐罐熊老师-查询用户手机号<br>https://admin.yunshuxie.com/v1/bear_course/query/bearUser_list.json<br/>
        """
        cookies = get_wacc_admin_cookie(self.env_flag,self.env_num)
        url = r"https://admin.yunshuxie.com"+"/v1/bear_course/query/bearUser_list.json"
        header = {"Accept": "application/json, text/javascript, */*; q=0.01",
                  "Accept-Encoding": "gzip, deflate, br",
                  "Accept-Language": "zh-CN,zh;q=0.9",
                  "Cache-Control": "no-cache", "Connection": "keep-alive",
                  "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                  "Origin": "https://admin.yunshuxie.com",
                  "Pragma": "no-cache", "Referer": "https://admin.yunshuxie.com/",
                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
                  "X-Requested-With": "XMLHttpRequest"}
        params = {"memberId":"","phone":self.phone,"sort":"memberId","order":"asc"}
        #logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = requests.get(url=url, params=params,headers=header,cookies=cookies)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        #logging.info(url + lianjiefu + self.resp.content + fengefu)
        print result["rows"]
        if result["rows"]:
            return [result["rows"][0]["memberId"]]
        else:
            print u"查询用户无数据"
            raise Exception,u"查询用户无数据"
    @fromRedis(getKey=["bearWord_Teacher_memberId"])
    def test_02_admin_bear_course_add_bearTeacher(self,getKey):
        """admin平台-运营管理-罐罐熊管理-添加罐罐熊老师-添加用户手机号为老师<br>https://admin.yunshuxie.com/v1/bear_course/add_bearTeacher.htm<br/>
        """
        bearWord_Teacher_memberId = getKey["bearWord_Teacher_memberId"]
        if bearWord_Teacher_memberId:
            cookies = get_wacc_admin_cookie(self.env_flag,self.env_num)
            url = r"https://admin.yunshuxie.com"+"/v1/bear_course/add_bearTeacher.htm"
            header = {"Accept": "application/json, text/javascript, */*; q=0.01",
                      "Accept-Encoding": "gzip, deflate, br",
                      "Accept-Language": "zh-CN,zh;q=0.9",
                      "Cache-Control": "no-cache", "Connection": "keep-alive",
                      "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                      "Origin": "https://admin.yunshuxie.com",
                      "Pragma": "no-cache", "Referer": "https://admin.yunshuxie.com/",
                      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
                      "X-Requested-With": "XMLHttpRequest"}
            teacherType = "2"
            params = {"memberId":bearWord_Teacher_memberId,"teacherType": teacherType} #teacherType==2,测试老师
            #logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
            str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
            print str_params
            self.resp = requests.get(url=url, params=params,headers=header,cookies=cookies)
            print self.resp.text
            result = json.loads(self.resp.text, encoding="utf8")
            #logging.info(url + lianjiefu + self.resp.content + fengefu)
        else:

            print u"查询用户无数据"
            raise Exception,u"查询用户无数据"
    def test_03_v1_bear_main_personData(self):
        """App个人中心数据-是否开启通知和是否是老师<br>https://mobile.yunshuxie.com/v1/bear/main/personData.htm<br>"""
        url = r"https://mobile.yunshuxie.com" + r"/v1/bear/main/personData.htm"
        cookies = get_app_cookie("罐罐熊APP",self.env_flag, self.env_num, self.phone)
        self.session.cookies = cookies
        self.resp = self.session.post(url=url)
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
    def test_04_v1_bear_teacher_bear_teacher(self):
        """罐罐熊-教师端-个人中心-接收作业开关-关闭<br>https://mobile.yunshuxie.com"+r"/v1/bear/teacher/recieve_teacher.htm<br>{"recieveStatus":"0"}"""
        url = r"https://mobile.yunshuxie.com"+r"/v1/bear/teacher/recieve_teacher.htm"
        params = {"recieveStatus":"0"}
        # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        cookies = get_app_cookie("罐罐熊APP",self.env_flag,self.env_num,self.phone)
        self.session.cookies = cookies
        self.resp = self.session.post(url=url, data=params)
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
    def test_05_v1_bear_teacher_bear_teacher(self):
        """罐罐熊-教师端-个人中心-接收作业开关-开启<br>https://mobile.yunshuxie.com"+r"/v1/bear/teacher/recieve_teacher.htm<br>{"recieveStatus":"1"}"""
        url = r"https://mobile.yunshuxie.com"+r"/v1/bear/teacher/recieve_teacher.htm"
        params = {"recieveStatus":"1"}
        # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        cookies = get_app_cookie("罐罐熊APP",self.env_flag,self.env_num,self.phone)
        self.session.cookies = cookies
        self.resp = self.session.post(url=url, data=params)
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
    @fromRedis(setKey=["admin_bearWord_workId"])
    def test_06_admin_bear_course_query_bearMmeber_timeLine(self):
        """admin平台-查询用户详情<br>https://admin.yunshuxie.com/v1/bear_course/query/bearMmeber_timeLine.json"""
        url = r"https://admin.yunshuxie.com"+r"/v1/bear_course/query/bearMmeber_timeLine.json"
        params ={"timeLineType":"11","phone":self.phone,"timeLineStatus": "6","beginDate": "",
                 "endDate":"","teacherPhone": "","order": "asc","limit": "10","offset": "0"}
        # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        cookies = get_wacc_admin_cookie(self.env_flag, self.env_num)
        header = {"Accept": "application/json, text/javascript, */*; q=0.01",
                  "Accept-Encoding": "gzip, deflate, br",
                  "Accept-Language": "zh-CN,zh;q=0.9",
                  "Cache-Control": "no-cache", "Connection": "keep-alive",
                  "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                  "Origin": "https://admin.yunshuxie.com",
                  "Pragma": "no-cache", "Referer": "https://admin.yunshuxie.com/",
                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
                  "X-Requested-With": "XMLHttpRequest"}
        self.resp = requests.get(url=url,params=params,headers=header,cookies=cookies)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        if result["rows"]:
            return [result["rows"][0]["timeLineId"]]
        else:
            raise Exception,u"当前用户未存在测试作业数据"
    @fromRedis(getKey=["bearWord_workId"])
    def test_07_admin_bear_course_batch_job_assgin(self,getKey):
        """admin平台-分配指定服务老师<br>https://admin.yunshuxie.com/v1/bear_course/batch_job_assgin.htm"""
        workId = getKey["bearWord_workId"]
        url = r"https://admin.yunshuxie.com"+r"/v1/bear_course/batch_job_assgin.htm"
        params ={"timelineIds": workId,"teacherPhone": self.phone,"assginJobStatus": "0"}
        # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        cookies = get_wacc_admin_cookie(self.env_flag, self.env_num)
        header = {"Accept": "application/json, text/javascript, */*; q=0.01",
                  "Accept-Encoding": "gzip, deflate, br",
                  "Accept-Language": "zh-CN,zh;q=0.9",
                  "Cache-Control": "no-cache", "Connection": "keep-alive",
                  "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                  "Origin": "https://admin.yunshuxie.com",
                  "Pragma": "no-cache", "Referer": "https://admin.yunshuxie.com/",
                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
                  "X-Requested-With": "XMLHttpRequest"}
        self.resp = requests.post(url=url,data=params,headers=header,cookies=cookies)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        expect = {"returnCode": "0"}
        if result["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
    @fromRedis(getKey=["admin_bearWord_workId"])
    def test_08_admin_bear_course_batch_job_assgin(self,getKey):
        """admin平台-重新分配指定服务老师<br>https://admin.yunshuxie.com/v1/bear_course/batch_job_assgin.htm"""
        workId = getKey["admin_bearWord_workId"]
        url = r"https://admin.yunshuxie.com"+r"/v1/bear_course/batch_job_assgin.htm"
        params ={"timelineIds": workId,"teacherPhone": self.phone,"assginJobStatus": "3"}
        # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        cookies = get_wacc_admin_cookie(self.env_flag, self.env_num)
        header = {"Accept": "application/json, text/javascript, */*; q=0.01",
                  "Accept-Encoding": "gzip, deflate, br",
                  "Accept-Language": "zh-CN,zh;q=0.9",
                  "Cache-Control": "no-cache", "Connection": "keep-alive",
                  "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                  "Origin": "https://admin.yunshuxie.com",
                  "Pragma": "no-cache", "Referer": "https://admin.yunshuxie.com/",
                  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
                  "X-Requested-With": "XMLHttpRequest"}
        self.resp = requests.post(url=url,data=params,headers=header,cookies=cookies)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        expect = {"returnCode": "0"}
        if result["returnCode"] == "0" or result["returnCode"] == 0:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
    @fromRedis(setKey=["bearWord_timelineId"])
    def test_09_v1_bear_teacher_not_correct_list(self):
        """老师端：待批改列表<br>https://mobile.yunshuxie.com/v1/bear/teacher/not_correct_list.htm<br>{"page":"","pageSize":""}"""
        url =r"https://mobile.yunshuxie.com"+r"/v1/bear/teacher/not_correct_list.htm"
        params = {"page":"1","pageSize":"10"}
        # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        cookies = get_app_cookie("罐罐熊APP",self.env_flag, self.env_num, self.phone)
        self.session.cookies = cookies
        self.resp = self.session.post(url=url, data=params)
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
        if result["data"]["notCorrectJobList"]:
            return [result["data"]["notCorrectJobList"][0]["timelineId"]]
        else:
            print u"当前教师未存在待批改作业"
            raise Exception,u"当前教师未存在待批改作业"
    @fromRedis(setKey=["bearWord_submitUpdateDate"],getKey=["bearWord_timelineId"])
    def test_10_v1_bear_teacher_bear_task(self,getKey):
        """老师端：用户作业详情<br>https://mobile.yunshuxie.com/v1/bear/teacher/bear_task.htm<br>{"timeLineId":""}"""
        bearWord_timelineId = getKey["bearWord_timelineId"]
        if bearWord_timelineId:
            url = r"https://mobile.yunshuxie.com" + r"/v1/bear/teacher/bear_task.htm"
            params = {"timeLineId":bearWord_timelineId}
            # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
            str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
            print str_params
            cookies = get_app_cookie("罐罐熊APP",self.env_flag, self.env_num, self.phone)
            self.session.cookies = cookies
            self.resp = self.session.post(url=url, data=params)
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
            if result["data"]:#["notCorrectJobList"]:
                # bearWord_timelineId = self.redis.str_set("bearWord_timelineId",
                #                                          result["data"]["notCorrectJobList"][0]["timelineId"])
                if result["data"]["submitUpdateDate"] !="":
                    return [result["data"]["submitUpdateDate"]]
        else:
            print u"当前教师未存在待批改作业"
            raise Exception,u"当前教师未存在待批改作业"
    def test_11_v1_bear_teacher_get_reject_reason_list(self):
        """驳回理由列表<br>https://mobile.yunshuxie.com/v1/bear/teacher/get_reject_reason_list.htm<br>"""
        url = r"https://mobile.yunshuxie.com" + r"/v1/bear/teacher/get_reject_reason_list.htm"
        cookies = get_app_cookie("罐罐熊APP",self.env_flag, self.env_num, self.phone)
        self.session.cookies = cookies
        self.resp = self.session.post(url=url)
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
    @fromRedis(getKey=["bearWord_timelineId","bearWord_submitUpdateDate"])
    def test_12_v1_bear_teacher_check_timeLineSatus(self,getKey):
        """老师端：校验用户是否重新提交作业<br>https://mobile.yunshuxie.com/v1/bear/teacher/check_timeLineSatus.htm<br>{"timeLineId":"","submitUpdateDate":""}"""
        bearWord_timelineId = getKey["bearWord_timelineId"]
        bearWord_submitUpdateDate = getKey["bearWord_submitUpdateDate"]
        if bearWord_timelineId:
            url = r"https://mobile.yunshuxie.com" + r"/v1/bear/teacher/check_timeLineSatus.htm"
            cookies = get_app_cookie("罐罐熊APP",self.env_flag, self.env_num, self.phone)
            params = {"timeLineId":bearWord_timelineId,"submitUpdateDate":bearWord_submitUpdateDate}
            # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
            str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
            print str_params
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
            raise Exception, u"当前教师未存在待批改作业"
    @fromRedis(setKey=["bearWord_mp3_link"])
    def test_13_v1_bear_teacher_upload_voice(self):
        """上传批改语音接口<br>https://mobile.yunshuxie.com/v1/bear/teacher/upload_voice.htm<br>files=binary"""
        url = r"https://mobile.yunshuxie.com/v1/bear/teacher/upload_voice.htm"
        cookies = get_app_cookie("罐罐熊APP",self.env_flag, self.env_num, self.phone)
        header = {"Connection": "keep-alive",  # "Content-Type": "multipart/form-data",
                  "User-Agent": "BearWord/1.0.0 (iPhone; iOS 12.3.1; Scale/3.00)"}
        files = {
            'file': ("mp3.amr",open(r'./app/base/pythonProject/suite/wacc-mobile/mp3.amr', 'rb'),"multipart/form-data"),
        }
        str_params = """{'file': ("mp3.amr",open(r'mp3.amr', 'rb'),"multipart/form-data")}"""
        # logging.info(url + lianjiefu + str_params + fengefu)
        print str_params
        self.resp = requests.post(url=url,headers=header,files=files,cookies=cookies.get_dict())
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
        if result["data"]["mp3"] != "":
            return [result["data"]["mp3"]]
    @fromRedis(getKey=["bearWord_timelineId","bearWord_mp3_link","bearWord_submitUpdateDate"])
    def test_14_v1_bear_teacher_save_correction_records(self,getKey):
        """老师端：批改作业保存<br>https://mobile.yunshuxie.com/v1/bear/teacher/save_correction_records.htm<br>{"timeLineId":"","commentVoice":"","excellence":"","commentContent":""}"""
        time.sleep(10)
        bearWord_timelineId = getKey["bearWord_timelineId"]
        commentVoice = getKey["bearWord_mp3_link"]
        bearWord_submitUpdateDate = getKey["bearWord_submitUpdateDate"]
        if bearWord_timelineId and commentVoice:
            url = r"https://mobile.yunshuxie.com" + r"/v1/bear/teacher/save_correction_records.htm"
            header = {"Connection": "keep-alive", "Content-Type": "application/x-www-form-urlencoded",
                      "User-Agent": "BearWord/1.0.0 (iPhone; iOS 12.3.1; Scale/3.00)"}
            cookies = get_app_cookie("罐罐熊APP",self.env_flag, self.env_num, self.phone)
            params = {"timeLineId":bearWord_timelineId,"excellence":"0","commentVoice":commentVoice,"commentContent":"[]","submitUpdateDate":bearWord_submitUpdateDate}
            # logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
            str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
            print str_params
            self.resp = requests.post(url=url,data=params,cookies=cookies,headers=header)
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
            raise Exception, u"当前教师未存在待批改作业"
    def test_15_v1_bear_teacher_corrected_record_list(self):
        """老师端：批改记录<br>https://mobile.yunshuxie.com/v1/bear/teacher/corrected_record_list.htm<br>{"page":"1","pageSize":"10","jobType":"0"}"""
        time.sleep(2)
        url = r"https://mobile.yunshuxie.com"+r"/v1/bear/teacher/corrected_record_list.htm"
        params = {"page":"1","pageSize":"10","jobType":"0"}
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
    @fromRedis(getKey=["bearWord_timelineId"])
    def test_16_v1_bear_teacher_recommend_job(self,getKey):
        """老师端：推荐/取消推荐优秀作业-推荐<br>https://mobile.yunshuxie.com/v1/bear/teacher/recommend_job.htm.htm<br>{"timeLineId":"","excellence":"1"}"""
        bearWord_timelineId = getKey["bearWord_timelineId"]
        if bearWord_timelineId:
            url = r"https://mobile.yunshuxie.com"+r"/v1/bear/teacher/recommend_job.htm"
            params = {"timeLineId":bearWord_timelineId,"excellence":"1"}
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

    @classmethod
    def tearDownClass(self):
        pass

if __name__ == "__main__":
    unittest.main()