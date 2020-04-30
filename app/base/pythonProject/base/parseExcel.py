#!/usr/bin/python
#-*-coding:utf-8
import xlrd
import sys
import os
def test_cases_in_excel(test_case_file):
    # 获取测试用例全路径
    test_case = xlrd.open_workbook(test_case_file)
    #print test_case._all_sheets_count  #获取SHEET COUNT
    countIndex = 0  # 获取第一个sheet，下标从0开始
    #print test_case.sheet_names()
    dict_sheet_case = {}
    for sheet in test_case.sheet_names():
        dict_case_sheet_params = {}
        table = test_case.sheet_by_index(countIndex)
        countIndex += 1
        for i in range(1,test_case.sheet_by_name(sheet).nrows):
            dict_case_params = {}  # table.cell(0, 0).value
            dict_case_params["order"] = table.cell(i, 0).value.replace("\n", "").replace("\r", "")
            dict_case_params["zone"] = table.cell(i, 1).value.replace("\n", "").replace("\r", "")
            dict_case_params["apiName"] = table.cell(i, 2).value.replace("\n", "").replace("\r", "")
            dict_case_params["apiNameEN"] = table.cell(i,3).value.replace("\n", "").replace("\r", "")
            dict_case_params["apiHost"] = table.cell(i, 4).value.replace("\n", "").replace("\r", "")
            dict_case_params["apiUrl"] = table.cell(i, 5).value.replace("\n", "").replace("\r", "")
            dict_case_params["method"] = table.cell(i, 6).value.replace("\n", "").replace("\r", "")
            dict_case_params["caseDesc"] = table.cell(i, 7).value.replace("\n", "").replace("\r", "")
            dict_case_params["caseHeaders"] = table.cell(i, 8).value.replace("\n", "").replace("\r", "")
            dict_case_params["caseRequestDatas"] = table.cell(i, 9).value.replace("\n", "").replace("\r", "")
            dict_case_params["caseStatusCode"] = table.cell(i, 10).value.replace("\n", "").replace("\r", "")
            dict_case_params["allorkeyNone"] = table.cell(i, 11).value.replace("\n", "").replace("\r", "")
            dict_case_params["caseExpectDatas"] = table.cell(i, 12).value.replace("\n", "").replace("\r", "")
            dict_case_sheet_params[i] = dict_case_params
        dict_sheet_case[sheet]=dict_case_sheet_params
    return dict_sheet_case
if __name__ == "__main__":
    filepath = "../api_test/data.xls"
    wc =  "%02d"%(int(test_cases_in_excel(filepath)["indexTest"][1]["order"]))
    s = "{{sss}}".replace("{{sss}}",wc)
    print s