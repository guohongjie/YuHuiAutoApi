#!/usr/bin/python
#-*-coding:utf-8 -*-
__author__ = "guohongjie"
from flask import render_template,request,flash
from app.main import report
from app.base import report_html
from app.config.config import TEST_FOLDER
@report.route('/Report')
def search_year():
	"""
	测试报告链接
	:return: report.html  测试报告
	"""
	integrationReportPath = TEST_FOLDER+"/ReportHtml/integrationReport"    #手工集成测试报告
	integrationFile = report_html(integrationReportPath)
	scheduleReportPath = TEST_FOLDER+"/ReportHtml/scheduleReport"    #手工集成测试报告
	scheduleFile = report_html(scheduleReportPath)
	workFlowReportPath = TEST_FOLDER +"/ReportHtml/workFlowReport"    #工作流测试报告
	workFlowFile = report_html(workFlowReportPath)
	return render_template('home/report.html',
						   integrationFile=integrationFile,
						   scheduleFile=scheduleFile,workFlowFile=workFlowFile)
@report.route('/Report/<reportType>/<month>/<data>/<html>')
def search_inner(reportType,month, data, html):
	"""
	测试完毕后,生成 {date}/{day}/{project}.html,该接口读取Html,并返回至页面
	:param month:  月
	:param data:   日
	:param html:   测试报告
	:return: 测试报告
	"""
	print html
	report_path = TEST_FOLDER + "/ReportHtml" + "/"+reportType+"/" + month + "/" + data + "/" + html
	html_inner = open(report_path.encode("utf8")).read()
	return html_inner