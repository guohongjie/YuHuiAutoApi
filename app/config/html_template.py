#!/usr/bin/python
#-*-coding:utf-8
#测试报告基础模板
html_base = u"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<!-- saved from url=(0104)http://uwsgi.sys.bandubanxie.com/Report/8/9/%E4%BA%91%E8%88%92%E5%86%99CRM%E7%B3%BB%E7%BB%9F_beta_7.html -->
<html xmlns="http://www.w3.org/1999/xhtml"><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>《{project_cn}》--接口测试报告</title>
    <meta name="generator" content="HTMLTestRunner 0.8.2.1">
        <link href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
    <script src="http://libs.baidu.com/jquery/2.0.0/jquery.min.js"></script>
    <script src="http://libs.baidu.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>
    
<style type="text/css" media="screen">
body        { font-family: Microsoft YaHei,Tahoma,arial,helvetica,sans-serif;padding: 20px; font-size: 80%; }
table       { font-size: 100%; }
/* -- heading ---------------------------------------------------------------------- */
.heading {
    margin-top: 0ex;
    margin-bottom: 1ex;
}
.heading .description {
    margin-top: 4ex;
    margin-bottom: 6ex;
}
/* -- report ------------------------------------------------------------------------ */
#total_row  { font-weight: bold; }
.passCase   { color: #5cb85c; }
.failCase   { color: #d9534f; font-weight: bold; }
.errorCase  { color: #f0ad4e; font-weight: bold; }
.hiddenRow  { display: none; }
.testcase   { margin-left: 2em; }
</style>

</head>
<body>
<div class="heading">
<h1 style="font-family: Microsoft YaHei">《{project_cn}》--接口测试报告</h1>
<p class="attribute"><strong>测试人员 : </strong> 最棒QA</p>
<p class="attribute"><strong>开始时间 : </strong> {start_time}</p>
<p class="attribute"><strong>结束时间 : </strong> {end_time}</p>
<p class="attribute"><strong>测试结果 : </strong> 共 {case_total}，通过 {case_pass}</p>
<p class="attribute"><strong>测试环境 : </strong> {env_flag}</p>
<p class="attribute"><strong>环境编号 : </strong> {env_num}</p>
</div>
<p id="show_detail_line">
<a class="btn btn-primary" href="javascript:showCase(0)">概要{ 100.00% }</a>
<a class="btn btn-danger" href="javascript:showCase(1)">失败{ {case_fail} }</a>
<a class="btn btn-success" href="javascript:showCase(2)">通过{ {case_pass} }</a>
<a class="btn btn-info" href="javascript:showCase(3)">所有{ {case_total} }</a>
</p>
<table id="result_table" class="table table-condensed table-bordered">
<colgroup>
<col align="left">
<col align="right">
<col align="right">
<col align="right">
<col align="right">
<col align="right">
</colgroup>
<tbody>
{api_title_detail}
</tbody></table>
</body></html>"""

#接口模块手工调度展示
schedule_html = u"""<tr id="header_row" class="text-center success" style="font-weight: bold;font-size: 14px;">
    <th style="width:10%">接口名称</td>
    <th style="width:25%">URL</td>
    <th style="width:20%">接口描述</td-->
    <th style="width:5%">请求方式</td>
    <th style="width:20%">请求参数</td>
    <th style="width:20%">详细</td>
</tr>
<tr class="passClass warning">
        {test_case_detailed}
    </tr>"""
#接口模块手工调度测试报告基础模板
html_all = html_base.replace("{api_title_detail}",schedule_html)
#接口测试模块调度功能报告明细
test_case_detailed = u"""
<tr class="passClass warning">
        <td>{api_name}</td>
        <td class="text-center text-justify pre-scrollable">{api_url}</td>
        <td class="text-center text-justify pre-scrollable">{description}</td>
        <td class="text-center text-justify pre-scrollable">{method}</td>
        <td class="text-center text-justify pre-scrollable"><button id="btn_req_params" type="button" class="btn btn-danger btn-xs collapsed" data-toggle="collapse" data-target="#btn_req_params_{pid}">详细</button>
            <div id="btn_req_params_{pid}" class="collapse" style="height: 0px;"> 
            <pre>    
        {request_params}
            </pre>
        </div></td>
        <td class="text-center text-justify pre-scrollable"><button type="button" class="btn {status_color} btn-xs collapsed" data-toggle="collapse" data-target="#btn_resp_json_{pid}">{case_status}</button>
        <div id="btn_resp_json_{pid}" class="collapse" style="height: 0px;"> 
        <pre>    
        {responce_params}
        </pre>
        </div></td>
</tr>
"""

#--------------------------------------------------华丽的分割线---------------------------------------#
#工作流调度流程名称及流程描述 显示  workflow_html
workflow_html = u"""
<tbody class="collapsed" data-toggle="collapse" data-target="#wctv_{collapse_id}">
<tr style="font-weight: bold;font-size: 18px;background-color:#506271">
    <th class="text-center" style="color:whitesmoke" colspan="2">工作流名称</th>
    <th class="text-center" style="color:whitesmoke" colspan="2">描述</th>
    <th class="text-center" style="color:whitesmoke" colspan="2">状态</th>
    
</tr>
<tr class="passClass warning">
    <td class="text-center text-primary text-justify pre-scrollable" colspan="2">{work_flow_name}</td>
    <td class="text-center text-primary text-justify pre-scrollable" colspan="2">{work_flow_descript}</td>
    <td class="text-center text-primary text-justify pre-scrollable" colspan="2">{work_flow_status}</td>
</tr>
</tbody>
"""
#工作流程内接口title
workflow_api_title = u"""
<tbody class="collapse" id="wctv_{collapse_id}">
<tr id="header_row_{collapse_id}" class="success" style="font-weight: bold;font-size: 14px;">
    <th class="text-center" style="width:10%">接口名称</th>
    <th class="text-center" style="width:25%">URL</th>
    <th class="text-center"  style="width:15%">接口描述</th>
    <th class="text-center"  style="width:10%">请求方式</th>
    <th class="text-center"  style="width:20%">请求参数</th>
    <th class="text-center"  style="width:20%">详细</th>
</tr>
"""
#工作流调度测试报告基础模板
work_flow_test_detailed = u"""
<tr class="passClass warning">
        <td>{api_name}</td>
        <td class="text-center text-justify pre-scrollable">{api_url}</td>
        <td class="text-center text-justify pre-scrollable">{description}</td>
        <td class="text-center text-justify pre-scrollable">{method}</td>
        <td class="text-center text-justify pre-scrollable">
        <button type="button" class="btn btn-danger btn-xs collapsed" data-toggle="collapse" data-target="#btn_req_params_{pid}">详细
        </button>
            <div id="btn_req_params_{pid}" class="collapse" style="height: 0px;"> 
            <pre>    
        {request_params}
            </pre>
        </div></td>
        <td class="text-center text-justify pre-scrollable">
        <button type="button" class="btn {status_color} btn-xs collapsed" data-toggle="collapse" data-target="#btn_resp_json_{pid}">{case_status}</button>
        <div id="btn_resp_json_{pid}" class="collapse" style="height: 0px;"> 
        <pre>    
        {responce_params}
        </pre>
        </div></td>
</tr>
"""


if __name__ == "__main__":
    api_name = "接口名称"
    api_url = "接口链接"
    request_params = "请求参数"
    assertValue = "校验参数"
    status_color = "btn-success" # or "btn-danger"
    case_status = "通过"
    responce_params = "返回参数"
    method = "GET"
    new_detailed = test_case_detailed.format(api_name=api_name,method=method,api_url=api_url,request_params=request_params,assertValue=assertValue,
                              status_color=status_color,case_status=case_status,responce_params=responce_params)

    project_cn = "测试项目"
    start_time = "20190816"
    end_time = "20190819"
    case_total = "100"
    case_pass = "20"
    env_flag = "beta"
    env_num = "8"
    case_fail = "10"
    wc = html_all.replace("{project_cn}",project_cn)
    wc1 = wc.replace("{test_case_detailed}",new_detailed)
    wc2 = wc1.replace("{start_time}",start_time)
    wc3 = wc2.replace("{end_time}",end_time)
    wc4 = wc3.replace("{case_total}",case_total,2)
    wc5 = wc4.replace("{case_pass}",case_pass,2)
    wc6 = wc5.replace("{env_flag}",env_flag)
    wc7 = wc6.replace("{env_num}",env_num)
    wc8 = wc7.replace("{case_fail}",case_fail)
    with open("C:\Users\Administrator\Desktop\wc.html","w") as f:
        f.write(wc8)