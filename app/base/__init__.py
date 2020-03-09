#!/usr/bin/python
#-*-coding:utf-8 -*-
import os
from collections import OrderedDict
from copy import deepcopy
def report_html(report_path):
	month = OrderedDict()
	report_list = os.listdir(report_path)
	report_list.sort()
	report_list.reverse()
	for monthFile in report_list:
		day = OrderedDict()
		month_list = os.listdir(report_path+"/"+monthFile)
		month_list.sort()
		month_list.reverse()
		for dayFile in month_list:
			fileList = os.listdir(report_path+"/"+"/"+monthFile+"/"+dayFile)
			day[dayFile] = fileList
		month[monthFile] = day
	return month  #{"month":{"day":[fileList]}}
