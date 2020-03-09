#!/usr/bin/python
#-*-coding:utf-8-*-
import requests
import unittest
classText="""#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import unittest
import re
import json
from requests import Session,Request
from log import TestLog,fengefu,lianjiefu
from getConfig import ReadConfig
logging = TestLog().getlog()
class {{sheetName}}Test(unittest.TestCase):
    #"{{sheetName}}"
    @classmethod
    def setUpClass(self):
        \"\"\"起始方法
        #:return:  cookies \"\"\"
        s = ReadConfig()
        env_flag = s.get_env("env_flag")
        env_num = s.get_env("env_num")
        phoneNum = s.get_params("phoneNum")
        userName = s.get_admin("userName")
        pwd = s.get_admin("pwd")
        self.cookies = requests.cookies.RequestsCookieJar()
        self.cookies.set('env_flag', env_flag)  #设置测试环境
        self.cookies.set("env_num",env_num)  #设置环境号
        {setUp}
    {runCode}
    @classmethod
    def tearDownClass(self):
        \"\"\"测试结束后执行,断言Req==Resp
        :return:  True OR False\"\"\"
        {tearDownText}
if __name__ == "__main__":
    unittest.main()"""
getSetUpText = """        params = {{caseRequestDatas}}
        self.url = "{{apiHost}}"+"{{apiUrl}}"
        caseHeaders = {{caseHeaders}}
        self.resp = requests.get(self.url, params=params, headers=caseHeaders ,cookies=self.cookies)
        logging.info(self.url + lianjiefu + self.resp.text +fengefu )
        self.cookies.update(self.resp.cookies)"""
postSetUpText = """        data = {{caseRequestDatas}}
        self.url = "{{apiHost}}"+"{{apiUrl}}"
        caseHeaders = {{caseHeaders}}
        self.resp = requests.post(self.url, data=data, headers=caseHeaders ,cookies=self.cookies)
        logging.info(self.url + lianjiefu + self.resp.text +fengefu )
        self.cookies.update(self.resp.cookies)"""
postFunctionText="""    def test_{{apiNameEN}}(self):
        \"\"\"{{caseDesc}}<br/>{{apiHost}}{{apiUrl}}<br/>\"\"\"
        self.caseStatusCode = {{caseStatusCode}}
        self.caseExpectDatas ={{caseExpectDatas}}
        data = {{caseRequestDatas}}
        self.url = "{{apiHost}}"+"{{apiUrl}}"
        method = "{{method}}"
        caseHeaders = {{caseHeaders}}
        str_params = json.dumps(data, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = requests.post(self.url, data=data, headers=caseHeaders,cookies=self.cookies)
        print self.resp.text
        logging.info(self.url + lianjiefu + self.resp.text +fengefu )
        msg = \"\"\"\n        Except:  {Except}-*-\n        Really:  {Really}\"\"\"  #校验HTTP返回代码
        assert self.caseStatusCode==self.resp.status_code,msg.format(Except=self.caseStatusCode,Really=self.resp.status_code)
        {{assertValue}}"""
getFunctionText="""    def test_{{order}}_{{apiNameEN}}(self):
        \"\"\"{{caseDesc}}<br/>{{apiHost}}{{apiUrl}}<br/>\"\"\"
        self.caseStatusCode = {{caseStatusCode}}
        self.caseExpectDatas ={{caseExpectDatas}}
        params = {{caseRequestDatas}}
        self.url = "{{apiHost}}"+"{{apiUrl}}"
        method = "{{method}}"
        caseHeaders = {{caseHeaders}}
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = requests.get(self.url, params=params, headers=caseHeaders,cookies=self.cookies)
        print self.resp.text
        logging.info(self.url + lianjiefu + self.resp.text +fengefu )
        msg = \"\"\"\n        Except:  {Except}-*-\n        Really:  {Really}\"\"\"  #校验HTTP返回代码
        assert self.caseStatusCode==self.resp.status_code,msg.format(Except=self.caseStatusCode,Really=self.resp.status_code)
        {{assertValue}}"""


assertAllValue="""respMsg = self.resp.content  #返回值
        caseExpectDatas = self.caseExpectDatas  #xls 校验值
        if caseExpectDatas:
            if type(caseExpectDatas).__name__ == "str":
                assert caseExpectDatas==respMsg,msg.format(Except=caseExpectDatas,Really=respMsg)
            elif type(caseExpectDatas).__name__ == "dict":
                json_caseExpectDatas = json.dumps(caseExpectDatas, encoding='utf-8', ensure_ascii=False)  # 期望值转换json
                try:
                    dict_resp = json.loads(re.match(".*?({.*}).*", respMsg, re.S).group(1))
                    assert caseExpectDatas==dict_resp,msg.format(Except=json_caseExpectDatas, Really=respMsg)  #判断期望值==返回值(转换成字典)
                except Exception as e:  #当value2 不是json类型
                    print e
                    respMsg = re.match(".*?({.*}).*", respMsg, re.S).group(1)
                    assert json_caseExpectDatas == respMsg,msg.format(Except=json_caseExpectDatas, Really=respMsg)
"""
assertKeyValue="""def assertKey(value1,value2):
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
                        msg = \"\"\"\n        Except:  {Except}-*-\n        Really:  {Really}\"\"\"
                        return key
            elif type(dictvalue2).__name__ == "list":
                for list_index in range(len(dictvalue2)):
                    assertKey(dictvalue1[list_index],dictvalue2[list_index])
        value1 = self.caseExpectDatas
        value2 = json.loads(re.match(".*?({.*}).*", self.resp.content, re.S).group(1))
        keyValue = assertKey(value1,value2)
        if keyValue:
            assert keyValue=="Error",msg.format(Except=keyValue,Really="Error")"""
tearDownText="""
        pass"""
