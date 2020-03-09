#!/usr/bin/python
#-*-coding:utf-8 -*-
import unittest
from base import HTMLTestRunnerCN
import datetime
import os
import requests
# 测试用例存放路径
# 获取所有测试用例
TEST_FOLDER = "./app/base/pythonProject"
def get_allcase(project):
    """
    :param project:  传入{project},获得suite路径下{project}文件夹内test开头的py文件
    :return: suite:  测试集合
    """
   # print TEST_FOLDER +"/suite/{project}".format(project=project)
    case_path = os.path.join(TEST_FOLDER +"/suite/",project)
    dis = unittest.TestLoader()
    discover = dis.discover(case_path, pattern="api_test*.py")
    suite = unittest.TestSuite()
    suite.addTest(discover)
    return suite
def run_test_case(project_en,env_num,env_flag,description,project_cn):
    """
    :param project:  传入{project},创建 suite路径/test_setting路径下{project}文件夹
    :param env_num:  测试环境号
    :param env_flag:  测试环境
    :return:  测试报告
    """
    # 运行测试用例
    xls_path = TEST_FOLDER + "/test_setting/{project}".format(project=project_en)
    filepath = TEST_FOLDER + "/suite/{project}".format(project=project_en)
    MakeTestSuite(xls_path).make_template(filepath)
    #year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    filePath = TEST_FOLDER + "/ReportHtml/scheduleReport/{month}/{day}".format(month=month,day=day)
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    fileName = "{project}_{env_flag}.html".format(project=project_cn,env_flag=env_flag)
    fp = filePath+"/"+fileName
    fp = file(fp,"wb")
    runner = HTMLTestRunnerCN.HTMLTestRunner(stream=fp, title="《"+project_cn+"》--接口测试报告", description=description,env_num=env_num,env_flag=env_flag)
    runner.run(get_allcase(project_en))


def run_yunwei_case(project_en,env_num,env_flag,description,project_cn,new_phone=None,developer=None,developer_project=None,branch=None):
    """
    :param project:  传入{project},创建 suite路径/test_setting路径下{project}文件夹
    :param env_num:  测试环境号
    :param env_flag:  测试环境
    :return:  测试报告
    """
    # 运行测试用例
    filepath = TEST_FOLDER + "/suite/{project}".format(project=project_en)
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    filePath = TEST_FOLDER + "/ReportHtml/scheduleReport/{month}/{day}".format(month=month,day=day)
    fileName = "{project}_{env_flag}_{env_num}.html".format(project=project_cn, env_flag=env_flag,env_num=env_num)
    # if env_num:
    #     fileName = "{project}_{env_flag}_{env_num}.html".format(project=project_cn,env_flag=env_flag,env_num=env_num)
    # else:
    #     fileName = "{project}_{env_flag}.html".format(project=project_cn, env_flag=env_flag)
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    fp = filePath+"/"+fileName
    fp = file(fp,"wb")
    new_phone = new_phone
    runner = HTMLTestRunnerCN.HTMLTestRunner(stream=fp, title="《"+project_cn+"》--接口测试报告", description=description,env_num=env_num,env_flag=env_flag,new_phone=new_phone)
    test_result = runner.run(get_allcase(project_en))
    error_count,failure_count,success_count =test_result.error_count,test_result.failure_count,test_result.success_count
    qiye_wechat_url = r"http://msg.inf.bandubanxie.com/api/v0.2/msg/qiye_weixin"
    report_url = r"http://uwsgi.sys.bandubanxie.com/Report/{month}/{day}/{project_cn}_{env_flag}_{env_num}.html".format(month=month,day=day,project_cn=project_cn,
                                                                                                                        env_flag=env_flag,env_num=env_num)
    if developer != None and  branch != None and developer_project != None:
        content = """后端发布自动化测试结果:
发布人: {developer}
发布项目: {developer_project}
发布环境: {env_flag}-{env_num}
发布分支: {branch}
测试项目: {project_cn}
通过接口数: {success_count}
未通过接口数: {error_count}
失败接口数: {failure_count}
结果查看地址: {report_url}""".format(project_cn=project_cn,env_flag=env_flag,env_num=env_num,success_count=success_count,
                                            error_count=error_count,failure_count=failure_count,developer=developer,
                                            developer_project=developer_project,branch=branch,report_url=report_url)
    else:
        content = """账号自动化创建:
创建号码: {new_phone}
发布环境: {env_flag}-{env_num}
通过接口数: {success_count}
未通过接口数: {error_count}
失败接口数: {failure_count}
结果查看地址: {report_url}""".format(env_flag=env_flag, env_num=env_num,
                                       success_count=success_count, error_count=error_count,
                                       failure_count=failure_count, new_phone=new_phone,report_url=report_url)
    params = {"tos":"guohongjie,renhuihui,zhaohongling,pengjunxia,wangmengxiao,hongchen,tianningxue,liushuang,xuhongying,panze,jiayujiao,huyanfeng,liangguoqing,{developer}".format(developer=developer),
              "content":content,"app":"qa","sed":"guohongjie"}
    requests.post(url=qiye_wechat_url,data=params)
    return {"Error":error_count,"Failure":failure_count,"Success":success_count,"report_url":report_url}