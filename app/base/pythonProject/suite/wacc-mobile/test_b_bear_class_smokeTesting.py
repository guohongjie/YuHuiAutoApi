#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import unittest
import json
from app.base.pythonProject.base.log import TestLog,fengefu,lianjiefu
from app.base.pythonProject.base.py_redis import fromRedis
from app.base.pythonProject.base.getCookies import get_app_cookie
import time
#logging = TestLog().getlog()
class BearWord_Class_Test(unittest.TestCase):
    """<br>学生端-上课<br>1.未登录，上课页显示登录按钮<br>2.已登录-微信-查看课程列表<br>3.已登录-APP-存在课程<br>4.已登录-APP-进入所选课程,查看章节列表<br>5.已登录-视频播放到70%即为已学习状态，解锁上传作品按钮<br>6.已登录-APP-上传作业，成功上传<br>7.已登录-APP-打卡接口<br>8.已登录-APP-作业被点评前，重新上传作业成功"""
    @classmethod
    @fromRedis(getKey=["wacc_mobile_env_flag","wacc_mobile_env_num","make_user_phones"])
    def setUpClass(self,getKey):
        self.env_flag = "beta"#getKey["wacc_mobile_env_flag"]
        self.env_num = "1"#getKey["wacc_mobile_env_num"]
        self.phone_Exist_Course = getKey["make_user_phones"]#"60000009092"  #存在课程
        self.timestamp = "%d"%(time.time())
        self.session = requests.Session()
        self.header = {"Connection": "keep-alive", "Content-Type": "application/x-www-form-urlencoded","User-Agent": "BearWord/1.0.0 (iPhone; iOS 12.3.1; Scale/3.00)"}
        self.msg = """\n        Expect:  {Expect}-*-\n        Really:  {Really}"""  # 校验HTTP返回代码
        self.session.headers = self.header
        cookies = get_app_cookie("罐罐熊APP",self.env_flag,self.env_num,self.phone_Exist_Course) #进行登录展示接口_新用户
        self.session.cookies = cookies
    def test_01_bear_student_courseList(self):
        """课程列表接口-未登录<br>https://mobile.yunshuxie.com/v1/bear/student/courseList.htm<br/>{"page":"1","isApp":"2"}
        """
        url = r"https://mobile.yunshuxie.com"+"/v1/bear/student/courseList.htm"
        params = {"page":"1","isApp":"2"}
        #logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        cookies = {"env_flag":self.env_flag,"env_num":self.env_num}
        print str_params
        self.resp = requests.post(url=url, data=params, headers=self.header, cookies=cookies,)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        #logging.info(url + lianjiefu + self.resp.content + fengefu)
        expect = {"returnCode": "4"}
        if result["returnCode"] == "4" or result["returnCode"] == 4:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
        else:
            assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                 Really=result["returnCode"])
    def test_02_bear_student_courseList(self):
        """课程列表接口-已登录<br>https://mobile.yunshuxie.com/v1/bear/student/courseList.htm<br/>{"page":"1","isApp":"1"}
        """
        url = r"https://mobile.yunshuxie.com"+"/v1/bear/student/courseList.htm"
        params = {"page":"1","isApp":"2"}
        #logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
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
    @fromRedis(setKey=["bearWord_productCourseId"])
    def test_03_bear_student_courseList(self):
        """课程列表接口-已登录(存在课程)<br>https://mobile.yunshuxie.com/v1/bear/student/courseList.htm<br/>{"page":"1","isApp":"1"}"""
        cookies = get_app_cookie("罐罐熊APP",self.env_flag,self.env_num,user=self.phone_Exist_Course) #进行登录展示接口_新用户
        self.session.cookies = cookies
        url = r"https://mobile.yunshuxie.com" + "/v1/bear/student/courseList.htm"
        params = {"page": "1", "isApp": "2"}
        #logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
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
        if result["data"]["list"]:
            return [result["data"]["list"][0]["productCourseId"]]
    @fromRedis(setKey=["bearWord_productChapterId"],getKey=["bearWord_productCourseId"])
    def test_04_bear_student_chapterList(self,getKey):
        """ 章节列表接口<br>https://mobile.yunshuxie.com/v1/bear/student/chapterList.htm<br/>{"productCourseId":"","isApp":"2"}"""
        productCourseId = getKey["bearWord_productCourseId"]
        if productCourseId:
            url = r"http://mobile.yunshuxie.com" + "/v1/bear/student/chapterList.htm"
            params = {"productCourseId":productCourseId,"isApp":"2"}
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
            if result["data"]["list"]:
                return [result["data"]["list"][2]["productChapterId"]]
        else:
            print u"当前页面不存在章节数据"
            raise Exception,u"当前页面不存在章节数据"
    @fromRedis(getKey=["bearWord_productChapterId"])
    def test_05_bear_student_chapterFinish(self,getKey):
        """ 视频播放完毕后更新学习完成状态<br>https://mobile.yunshuxie.com/v1/bear/student/chapterFinish.htm<br/>{"productChapterId":"","isApp":"2"}"""
        productChapterId = getKey["bearWord_productChapterId"]
        if productChapterId:
            url = r"http://mobile.yunshuxie.com" + "/v1/bear/student/chapterFinish.htm"
            params = {"productChapterId":productChapterId,"isApp":"2"}
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
            raise Exception,u"当前页面不存在章节数据"
    @fromRedis(setKey=["bearWord_workId"],getKey=["bearWord_productChapterId"])
    def test_06_bear_student_uploadWork(self,getKey):
        """ 上传作品<br>https://mobile.yunshuxie.com/v1/bear/student/uploadWork.htm<br/>{img,content,productChapterId,isApp}"""
        productChapterId = getKey["bearWord_productChapterId"]
        if productChapterId:
            url = r"http://mobile.yunshuxie.com" + "/v1/bear/student/uploadWork.htm"
            params = {"img":"https://ysx-sts-upload.oss-cn-beijing.aliyuncs.com/pic/ios/avatar/2019/07/26/14/44/15/f0611a93e0034d5ab5ebc0c86dc4046c/D373EF8C-8F81-47F2-83FC-8B072F536EEB.png",
                      "content":"测试,权限归测试组所有",
                      "productChapterId":productChapterId,"isApp":"2"}
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
            if result["data"]["workId"]:
                return [result["data"]["workId"]]
        else:
            print u"当前页面不存在章节数据"
            raise Exception, u"当前页面不存在章节数据"
    @fromRedis(getKey=["bearWord_productCourseId","bearWord_productChapterId"])
    def test_07_bear_student_clock(self,getKey):
        """ 打卡接口<br>https://mobile.yunshuxie.com/v1/bear/student/clock.htm<br/>{img,content,productChapterId,isApp}"""

        productCourseId = getKey["bearWord_productCourseId"]
        productChapterId = getKey["bearWord_productChapterId"]
        if productCourseId and productChapterId:
            url = r"http://mobile.yunshuxie.com" + "/v1/bear/student/clock.htm"
            params = {"productCourseId":productCourseId,"productChapterId":productChapterId,"isApp":"2"}
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
    @fromRedis(setKey=["bearWord_workId"],getKey=["bearWord_productChapterId"])
    def test_08_bear_student_uploadWork(self,getKey):
        """重新上传作品<br>https://mobile.yunshuxie.com/v1/bear/student/uploadWork.htm<br/>{img,content,productChapterId,isApp}"""
        time.sleep(5)
        productChapterId = getKey["bearWord_productChapterId"]
        if productChapterId:
            url = r"http://mobile.yunshuxie.com" + "/v1/bear/student/uploadWork.htm"
            params = {
                    "img": "https://ysx-sts-upload.oss-cn-beijing.aliyuncs.com/pic/ios/avatar/2019/07/26/14/44/15/f0611a93e0034d5ab5ebc0c86dc4046c/D373EF8C-8F81-47F2-83FC-8B072F536EEB.png",
                    "content": "测试,权限归测试组所有",
                    "productChapterId": productChapterId, "isApp": "2"}
            #logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
            str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
            print str_params
            self.resp = self.session.post(url=url, data=params)
            print self.resp.text
            result = json.loads(self.resp.text, encoding="utf8")
            #logging.info(url + lianjiefu + self.resp.text + fengefu)
            expect = {"returnCode": "13008"}
            if result["returnCode"] == "13008" or result["returnCode"] == 13008:
                assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                         Really=result["returnCode"])
            else:
                assert result["returnCode"] == expect["returnCode"], self.msg.format(Expect=expect["returnCode"],
                                                                                         Really=result["returnCode"])
            if result["data"]["workId"]:
                return [result["data"]["workId"]]
        else:
            print u"当前页面不存在章节数据"
            raise Exception, u"当前页面不存在章节数据"
    @classmethod
    def tearDownClass(self):
        pass

if __name__ == "__main__":
    unittest.main()