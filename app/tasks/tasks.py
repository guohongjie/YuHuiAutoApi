#!/usr/bin/python
#-*-coding:utf-8 -*-
from celery_app import celery,MyTask
from app.config.sql import select_sql,insert_sql
from urllib import quote
from app.config.html_template import test_case_detailed,html_all
from app.config.html_template import workflow_html,work_flow_test_detailed,html_base,workflow_api_title
from app.base.pythonProject.run import run_yunwei_case
from app.config.public_function import run_test,wechatQY_msg
import requests
import datetime
import json
import os

#持续集成调度测试

@celery.task(bind=True,base=MyTask)
def run_schedule_api(self,origin=None,originParams=None,cookies=None,developer=None):
    """
    单接口模块调度功能执行方法
    :param self:  #bind task 作为self传入
    :param origin:     #来源 根据来源判断手工调度和自动调度
    :param originParams:     #来源参数
    :param cookies:     #测试环境指向
    :param developer:     #发布人员
    :return:
    """
    if origin=="doSelfSchedule":    #手工调度发起
        keys = ["project", "case_api", "case_host", "case_url", "method", "params", "headers","description",
                "islogin", "account_project","account_username","account_passwd","isSchedule","checkAssert"]
        datas_list = []
        for key,api_datas in originParams.items():
            api_dict_datas = json.loads(api_datas)
            project,case_api,api_pid = api_dict_datas["project"],api_dict_datas["case_api"],api_dict_datas["api_pid"]
            sql = """
            select 
                project,case_api,case_host,case_url,method,params,headers,description,
                islogin,account_project,account_username,account_passwd,isSchedule,checkAssert
            from
                case_http_api 
            where
                project='%s' and case_api='%s' and id='%s'
            """%(project,case_api,api_pid)
            datas = select_sql(sql)
            for data in datas:
                key_value = dict(zip(keys, data))
                datas_list.append(key_value)
    else:    #持续集成调度发起
        project = originParams
        sql = """
        select 
            cha.project,cha.case_api,cha.case_host,cha.case_url,cha.method,
            chs.params,chs.assertValue,
            cha.headers,cha.islogin,
            cha.account_project,cha.account_username,cha.account_passwd
        from 
            case_http_api cha, case_http_schedule chs 
        where
            cha.id = chs.api_id and cha.project='%s' 
            and chs.status=1 """%(project)
        datas = select_sql(sql)
        datas_list = []
        keys = ["project", "case_api", "case_host", "case_url", "method", "params","assertValue",
                "headers","islogin", "account_project", "account_username", "account_passwd"]
        for data in datas:
            key_value = dict(zip(keys,data))
            datas_list.append(key_value)

    html_test_msg = ""
    case_total = len(datas_list)   #全部用例
    current = 0  #计数器
    case_success = 0  #成功用例数
    case_mistake = 0  #代码错误用例数
    case_failed = 0  #失败用例数
    startTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 获取开始时间
    for i in range(case_total):
        current += 1  # 计数器+1
        case_api = datas_list[i]["case_api"]  # 接口名称
        case_url = datas_list[i]["case_host"] + datas_list[i]["case_url"]
        case_params = datas_list[i]["params"]
        if origin == "doSelfSchedule":
            resp_status,resp_text = run_test(origin,datas_list[i],cookies)  # 手工调度传入 单条 接口用例数据
        else:
            resp_status, resp_text = run_test(origin,datas_list[i], cookies)  # 集成调度传入 单条 接口用例数据
        if resp_status =="Success":
            pass_status = 1
            case_success += 1
        elif resp_status == "Mistake":
            pass_status = 2
            case_mistake += 1
        else:
            pass_status = 0
            case_failed += 1
        api_name = case_api  #"接口名称"
        api_url =  case_url  #"接口链接"
        request_params = case_params  #"请求参数"
        responce_params = resp_text  #"返回参数"
        method = datas_list[i]["method"]
        project_cn = datas_list[i]["project"]
        description = datas_list[i]["description"]
        if pass_status == 1:
            status_color = "btn-success"
            case_status = u"通过"
        elif pass_status==0:
            status_color = "btn-danger"
            case_status = u"失败"
        else:
            status_color = "btn-danger"
            case_status = u"返回错误"
        new_detailed = test_case_detailed.format(api_name=api_name, method=method, api_url=api_url,description=description,
                                                 request_params=request_params,
                                                 status_color=status_color, case_status=case_status,
                                                 responce_params=responce_params,pid=str(i))
        html_test_msg += new_detailed
        # self.update_state(state='PROGRESS',
        #                   meta={'current': i, 'total': case_total,
        #                        'status': case_api,"pass_status":pass_status,"data_list":resp_text})
    endTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 获取结束时间
    start_time = startTime
    end_time = endTime
    case_total = case_total
    case_pass = str(case_success)
    env_flag = cookies["env_flag"]
    env_num = cookies["env_num"]
    case_fail = str(case_failed)
    case_mistake = case_mistake
    wc = html_all.replace("{project_cn}", project_cn)
    wc1 = wc.replace("{test_case_detailed}", html_test_msg)
    wc2 = wc1.replace("{start_time}", start_time)
    wc3 = wc2.replace("{end_time}", end_time)
    wc4 = wc3.replace("{case_total}", str(case_total), 2)
    wc5 = wc4.replace("{case_pass}", case_pass, 2)
    wc6 = wc5.replace("{env_flag}", env_flag)
    wc7 = wc6.replace("{env_num}", env_num)
    wc8 = wc7.replace("{case_fail}", case_fail)
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    project_en_sql = "select project_en from project_api where project='%s'"%(project_cn)
    project_en = select_sql(project_en_sql)[0][0]
    path = "./app/base/pythonProject/ReportHtml/integrationReport/{month}/{day}/".format(month=str(month),day=str(day))
    if not os.path.exists(path):
        os.makedirs(path)
    file_path = u"./app/base/pythonProject/ReportHtml/integrationReport/{month}/{day}/{project_cn}.html".format(month=str(month),day=str(day),project_cn=project_cn)

    with open(file_path,"w") as f:
        f.write(wc8.encode("utf8"))
###发送报告消息
    report_url = u"http://uwsgi.sys.bandubanxie.com/Report/integrationReport/{month}/{day}/{project_en}.html".format(
        month=str(month), day=str(day), project_en=project_cn)
    wechatQY_msg(developer=developer,project_cn=project_cn,report_url=report_url,
                 success_count=str(case_pass),fail_count=str(case_fail),
                 mistake_count=str(case_mistake),cookies=json.dumps(cookies,encoding="utf8",ensure_ascii=False))
    return {'current': current, 'total': case_total, 'status': u'执行成功!','result': case_success,"case_failed":case_failed,"case_mistake":case_mistake}

#持续集成业务流程调度测试
@celery.task()
def run_api_case(project_en,env_num,env_flag,description,project_cn,new_phone=None,developer=None,developer_project=None,branch=None):
    try:#project_en,env_num,env_flag,description,project_cn,new_phone=None,developer=None,developer_project=None,branch=None
        run_yunwei_case(project_en=project_en,
                        env_num=env_num,
                        env_flag=env_flag,description=description,
                        project_cn=project_cn,new_phone=new_phone,developer=developer,developer_project=developer_project,branch=branch)
        return u"执行成功!"
    except Exception as e:
        return str(e)

# @celery.task(base=MyTask)
def run_suite_api(suiteCount,suiteAll,cookies,domain,developer):
    """接口工作流功能域调度执行方法"""
    # test_suite_url = r"http://uwsgi.sys.bandubanxie.com/testSuite"
    test_suite_url = r"http://127.0.0.1:5000/testSuite"
    startTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 获取开始时间
    lengthSuite = suiteCount    #统计行数
    suiteAllCase = suiteAll
    suiteNameAndRespContent = {}
    for singleSuite in suiteAllCase:
        suiteDatas = singleSuite.suiteDatas
        suiteName = singleSuite.suiteName
        post_datas = {"datas": suiteDatas,
                      "suiteName": suiteName,
                      "cookies": cookies,
                      "isSuiteOrigin": "2"}
        resp = requests.post(url=test_suite_url, data=post_datas, timeout=600)
        if resp.status_code==200:
            suiteNameAndRespContent[singleSuite.suiteName] = [resp,singleSuite]
        else:
            suiteNameAndRespContent[singleSuite.suiteName] = [resp,singleSuite]
    temp_html,case_pass,case_fail = make_work_flow_html(suiteNameAndRespContent)    #测试完毕后传入制作测试报告
    endTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') # 获取结束时间
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    path = "./app/base/pythonProject/ReportHtml/workFlowReport/{month}/{day}/".format(month=str(month), day=str(day))
    if not os.path.exists(path):
        os.makedirs(path)
    file_path = u"./app/base/pythonProject/ReportHtml/workFlowReport/{month}/{day}/{project_cn}.html".format(
        month=str(month), day=str(day), project_cn=domain)
    with open(file_path, "w") as f:
        work_flow_report = temp_html.replace("{project_cn}", domain
                    ).replace("{start_time}",startTime
                        ).replace("{end_time}",endTime
                         ).replace("{case_total}",str(lengthSuite)
                          ).replace("{env_flag}",json.loads(cookies)["env_flag"]
                          ).replace("{env_num}",json.loads(cookies)["env_num"])
        f.write(work_flow_report)
    report_url = u"http://uwsgi.sys.bandubanxie.com/Report/workFlowReport/{month}/{day}/{project_en}.html".format(
        month=str(month), day=str(day), project_en=domain)
    new_cookies = quote(cookies)
    new_report_url = quote(report_url.encode("utf8"))
    sql ="""insert into test_report(domain,developer,report_url,success_count,fail_count,
    mistake_count,cookies,type)
    values("{domain}","{developer}","{report_url}","{success_count}",
    "{fail_count}","{mistake_count}","{cookies}","{report_type}");""".format(
        domain=domain,developer=developer,success_count=case_pass,report_type="work_flow",
        fail_count=case_fail,mistake_count=0,cookies=new_cookies,report_url=new_report_url
    )
    print sql
    msg = insert_sql(sql)
    print msg
    wechatQY_msg(developer=developer,project_cn=domain,report_url=report_url,
                 success_count=str(case_pass),fail_count=str(case_fail),mistake_count=None,cookies=cookies)

def make_work_flow_html(dictResp):
    """生成工作流測試報告"""
    #html_base    #测试报告基础模板
    #workflow_html    #工作流调度流程名称及流程描述 显示
    work_flow_html = ""    #完整工作流報告
    count = 1
    pass_count = 0
    fail_count = 0
    for key,value in dictResp.items():    #遍历工作流返回结果 type {"流程名称":"流程测试结果集"}
        count = count +1
        resp = value[0]
        apiDetail = value[1]
        api_run_statu_list = []  # 记录接口测试状态集合
        if resp.status_code==200:    #判断请求服务端测试返回结果
            list_resp_content = json.loads(resp.content,encoding="utf8")["datas"]
            api_detail_list = json.loads(resp.content,encoding="utf8")["api_detail"]
            all_work_flow_test_detail = ""    #定义测试报告基础模板总和
            for i in range(len(list_resp_content)):    #遍历工作流测试返回结果
                api_name = list_resp_content[i][0]
                req_datas = list_resp_content[i][1]
                resp_msg = list_resp_content[i][2]
                test_result = list_resp_content[i][3]
                api_run_statu_list.append(test_result)
                print api_detail_list
                new_work_flow_test_detail = work_flow_test_detailed.format(
                    api_name=api_detail_list[i]["name"],    #接口名称
                    api_url=api_name,    #接口链接
                    description=api_detail_list[i]["desc"],    #接口描述
                    method=api_detail_list[i]["method"],    #请求方式
                    pid=str(count)+str(i),    #属性索引
                    request_params=json.dumps(req_datas,encoding="utf8",ensure_ascii=False),
                    status_color="red",
                    case_status=test_result,
                    responce_params=str(resp_msg)
                )    #工作流调度测试报告基础模板

                all_work_flow_test_detail += new_work_flow_test_detail
            if api_run_statu_list.count("Mistake") and api_run_statu_list.count("Failure")==0:
                fail_count += 1
                work_flow_test_result = "测试错误,请检查错误接口及其上下文接口!"
            elif api_run_statu_list.count("Failure") and api_run_statu_list.count("Mistake")==0:
                fail_count += 1
                work_flow_test_result = "接口失败,请调试失败接口及其上下文接口!"
            elif api_run_statu_list.count("Failure") and api_run_statu_list.count("Mistake")==0:
                fail_count += 1
                work_flow_test_result = "测试失败,请检查错误接口及其上下文接口!"
            else:
                pass_count += 1
                work_flow_test_result = "测试通过"

            new_workflow_html = workflow_html.replace(
                "{work_flow_name}", key).replace(
                "{work_flow_descript}", apiDetail.description).replace("{collapse_id}", str(count)
                                                      ).replace("{work_flow_status}", work_flow_test_result)
            new_workflow_api_title = workflow_api_title.format(collapse_id=count)
            temp_html = new_workflow_html + new_workflow_api_title + all_work_flow_test_detail
        else:
            msg = "服务端接口请求异常,请调试当前工作流:%s"%(key)
            new_workflow_html = workflow_html.replace(
                "{work_flow_name}", key).replace(
                "{work_flow_descript}", apiDetail.description).replace("{collapse_id}", str(count)
                                                      ).replace("{work_flow_status}", msg)
            temp_html = new_workflow_html
            fail_count += 1
        temp_html1 = temp_html + "</tbody>"
        work_flow_html += temp_html1
    all_work_flow_html = html_base.replace("{api_title_detail}",work_flow_html
                                           ).replace("{case_pass}",str(pass_count)
                                                     ).replace("{case_fail}",str(fail_count))
    return all_work_flow_html,pass_count,fail_count
if __name__ == "__main__":
    run_schedule_api("",origin="doSelfSchedule",originParams=None,cookies=None,developer=None)