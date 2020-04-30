#!/usr/bin/python
#-*-coding:utf-8 -*-
__author__ ="guohongjie"
from flask import Blueprint
report = Blueprint("main",__name__)  #创建蓝图
test = Blueprint("api_test",__name__)
views = Blueprint("views",__name__)
mock = Blueprint("mock",__name__)
user = Blueprint("user",__name__)
flow = Blueprint("flow",__name__)
from app.main import WebHttpIndexViews,WebHttpTest,MyFlowIndex,\
    WebIndex,WebUser,MockHttpServer,ProjectIndexViews,httpSuite,apiReport,MyFlowDomain,WebTestUse

