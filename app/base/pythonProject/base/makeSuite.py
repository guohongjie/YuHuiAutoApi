#!/usr/bin/python
#-*-coding:utf-8 -*-
import parseExcel
import template
import os
import sys
if sys.getdefaultencoding() != "utf-8":
    reload(sys)
    sys.setdefaultencoding("utf8")
class MakeTestSuite(object):
    def __init__(self,xls_path):
        self.xls_path = xls_path
        self.list_xlsFile = os.listdir(xls_path)
        self.listXlsFile = []
        for xlfFile in self.list_xlsFile:
            #print xls_path+"/"+xlfFile
            dict_sheet_case_params = parseExcel.test_cases_in_excel(xls_path + "/" + xlfFile)
            self.listXlsFile.append(dict_sheet_case_params)
        #print self.dict_sheet_case_params
    def make_setUp_template(self,test_params):
        getSetupText = template.getSetUpText
        postSetupText = template.postSetUpText
        num_case_params = test_params
        self.setupHtml = ""
        for num,case_params in num_case_params.items():
            if case_params["zone"] == "setup":
                if case_params["method"] == "GET":
                    self.setupText = getSetupText.replace("{{apiHost}}",
                            case_params["apiHost"]).replace("{{apiUrl}}"
                            ,case_params["apiUrl"]).replace("{{caseRequestDatas}}"
                            ,case_params["caseRequestDatas"]).replace("{{caseHeaders}}"
                            ,case_params["caseHeaders"])
                elif case_params["method"] == "POST":
                    self.setupText = postSetupText.replace("{{apiHost}}",
                            case_params["apiHost"]).replace("{{apiUrl}}"
                            ,case_params["apiUrl"]).replace("{{caseRequestDatas}}"
                            ,case_params["caseRequestDatas"]).replace("{{caseHeaders}}"
                            ,case_params["caseHeaders"])
                else:
                    pass  #其他协议暂不处理
                self.setupHtml = self.setupHtml + "\n" + self.setupText
        return self.setupHtml
    def make_test_template(self,test_params):
        getFunctionText = template.getFunctionText
        postFunctionText = template.postFunctionText
        assertAllValue = template.assertAllValue
        assertKeyValue = template.assertKeyValue
        num_case_params = test_params
        self.testHTML = ""
        for num, case_params in num_case_params.items():
               # order = "%02d"%(int(case_params["order"]))
            if case_params["zone"] == "api_test":
                if case_params["method"] == "GET":
                    exceptDatas = isStr(case_params["caseExpectDatas"])
                    if case_params["allorkeyNone"] == "ALL":
                        self.testText = getFunctionText.replace("{{apiHost}}",
                                                    case_params["apiHost"]).replace("{{apiUrl}}",
                                                    case_params["apiUrl"]).replace("{{caseRequestDatas}}",
                                                    case_params["caseRequestDatas"]).replace("{{caseHeaders}}",
                                                    case_params["caseHeaders"]).replace("{{caseDesc}}",
                                                    case_params["caseDesc"]).replace("{{caseStatusCode}}",
                                                    case_params["caseStatusCode"]).replace("{{caseExpectDatas}}",
                                                    exceptDatas).replace("{{method}}",
                                                    case_params["method"]).replace("{{apiNameEN}}",
                                                    case_params["apiNameEN"]).replace("{{assertValue}}",
                                                                                      assertAllValue).replace("{{order}}","%02d"%(int(case_params["order"])))
                    elif case_params["allorkeyNone"] == "KEY":
                        self.testText = getFunctionText.replace("{{apiHost}}",
                                                    case_params["apiHost"]).replace("{{apiUrl}}",
                                                    case_params["apiUrl"]).replace("{{caseRequestDatas}}",
                                                    case_params["caseRequestDatas"]).replace("{{caseHeaders}}",
                                                    case_params["caseHeaders"]).replace("{{caseDesc}}",
                                                    case_params["caseDesc"]).replace("{{caseStatusCode}}",
                                                    case_params["caseStatusCode"]).replace("{{caseExpectDatas}}",
                                                    exceptDatas).replace("{{method}}",
                                                    case_params["method"]).replace("{{apiNameEN}}",
                                                    case_params["apiNameEN"]).replace("{{assertValue}}",
                                                                                      assertKeyValue).replace("{{order}}","%02d"%(int(case_params["order"])))
                    else:
                        self.testText = getFunctionText.replace("{{apiHost}}",
                                                    case_params["apiHost"]).replace("{{apiUrl}}",
                                                    case_params["apiUrl"]).replace("{{caseRequestDatas}}",
                                                    case_params["caseRequestDatas"]).replace("{{caseHeaders}}",
                                                    case_params["caseHeaders"]).replace("{{caseDesc}}",
                                                    case_params["caseDesc"]).replace("{{caseStatusCode}}",
                                                    case_params["caseStatusCode"]).replace("{{caseExpectDatas}}",
                                                    exceptDatas).replace("{{method}}",
                                                    case_params["method"]).replace("{{apiNameEN}}",
                                                    case_params["apiNameEN"]).replace("{{assertValue}}",
                                                                                      u"#不用校验返回值").replace("{{order}}","%02d"%(int(case_params["order"])))
                elif case_params["method"] == "POST":
                    exceptDatas = isStr(case_params["caseExpectDatas"])
                    if case_params["allorkeyNone"] == "ALL":
                        self.testText = postFunctionText.replace("{{apiHost}}",
                                                    case_params["apiHost"]).replace("{{apiUrl}}",
                                                    case_params["apiUrl"]).replace("{{caseRequestDatas}}",
                                                    case_params["caseRequestDatas"]).replace("{{caseHeaders}}",
                                                    case_params["caseHeaders"]).replace("{{caseDesc}}",
                                                    case_params["caseDesc"]).replace("{{caseStatusCode}}",
                                                    case_params["caseStatusCode"]).replace("{{caseExpectDatas}}",
                                                    exceptDatas).replace("{{method}}",
                                                    case_params["method"]).replace("{{apiNameEN}}",
                                                    case_params["apiNameEN"]).replace("{{assertValue}}",
                                                                                      assertAllValue).replace("{{order}}","%02d"%(int(case_params["order"])))
                    elif case_params["allorkeyNone"] == "KEY":
                        self.testText = postFunctionText.replace("{{apiHost}}",
                                                    case_params["apiHost"]).replace("{{apiUrl}}",
                                                    case_params["apiUrl"]).replace("{{caseRequestDatas}}",
                                                    case_params["caseRequestDatas"]).replace("{{caseHeaders}}",
                                                    case_params["caseHeaders"]).replace("{{caseDesc}}",
                                                    case_params["caseDesc"]).replace("{{caseStatusCode}}",
                                                    case_params["caseStatusCode"]).replace("{{caseExpectDatas}}",
                                                    exceptDatas).replace("{{method}}",
                                                    case_params["method"]).replace("{{apiNameEN}}",
                                                    case_params["apiNameEN"]).replace("{{assertValue}}",
                                                                                      assertKeyValue).replace("{{order}}","%02d"%(int(case_params["order"])))
                    else:
                        self.testText = postFunctionText.replace("{{apiHost}}",
                                                    case_params["apiHost"]).replace("{{apiUrl}}",
                                                    case_params["apiUrl"]).replace("{{caseRequestDatas}}",
                                                    case_params["caseRequestDatas"]).replace("{{caseHeaders}}",
                                                    case_params["caseHeaders"]).replace("{{caseDesc}}",
                                                    case_params["caseDesc"]).replace("{{caseStatusCode}}",
                                                    case_params["caseStatusCode"]).replace("{{caseExpectDatas}}",
                                                    exceptDatas).replace("{{method}}",
                                                    case_params["method"]).replace("{{apiNameEN}}",
                                                    case_params["apiNameEN"]).replace("{{assertValue}}",
                                                                                      u"#不用校验返回值").replace("{{order}}","%02d"%(int(case_params["order"])))
                else:
                    pass  # 其他协议暂不处理
                self.testHTML = self.testHTML + "\n" + self.testText
        return self.testHTML
    def make_teardowm_template(self):
        """
        :return:  tearDown模板
        """
        self.tearDownText  = template.tearDownText
        return self.tearDownText
    def make_template(self,filepath):
        """
        传入文件路径
        :param filepath:  文件路径，测试执行时自动寻找该文件夹下的Case;
        :param env_num:   测试环境号;
        :param env_flag:   测试环境 *根据传入的测试环境/环境号，运行对应的测试环境
        :return:  File:  project  File.py:  Test_sheet_name.py
        """
        tearDownText = self.make_teardowm_template()
        for singleFile in self.listXlsFile:
            for sheet_name,test_params in singleFile.items():
                if test_params:
                    setupText = self.make_setUp_template(test_params)
                    testText = self.make_test_template(test_params)
                    classText = template.classText
                    temp_classText = classText.replace("{{sheetName}}"
                                    ,sheet_name)
                    test_classText = temp_classText.format(setUp=setupText,runCode=testText,tearDownText=tearDownText)
                    with open(filepath+"/test_%s.py"%(sheet_name),"w") as f:
                        f.write(test_classText)
def isStr(params):
    try:
        eval(params)

        return params
    except:
        new_params = "\"\"\"%s\"\"\""%(params)
        return new_params

if __name__ == "__main__":
    xls_path = "../test_setting"
    file_path = "../suite"
    MakeTestSuite(xls_path).make_template(file_path)