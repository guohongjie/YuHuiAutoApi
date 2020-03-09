#!/usr/bin/python
#-*-coding:utf-8 -*-
from app.main import mock
from flask import render_template,request,make_response,jsonify
from app import db
from app.config.api_models import Case_Http_API
@mock.route("/mock/<path:url>",methods=["GET","POST"])
def mockserver(url):
    """Mcok服务"""
    new_url = r"/"+url
    if request.method=="POST":
        try:
            api_id = request.form["id"]
        except Exception as e:
            api_id = None
    elif request.method=="GET":
        api_id = request.args.get("id")
    else:
        return make_response(jsonify({"msg":"Mock Server 不支持其他协议"}))
    if api_id:
        ApiIdUrlResp = db.session.query(Case_Http_API.id,Case_Http_API.case_url,Case_Http_API.response).filter_by(case_url=new_url,id=api_id).order_by("id asc").first()
    else:
        ApiIdUrlResp = db.session.query(Case_Http_API.id,Case_Http_API.case_url,Case_Http_API.response).filter_by(case_url=new_url).order_by("id asc").first()
    #print ApiIdUrlResp[2]
    if ApiIdUrlResp:
        return ApiIdUrlResp[2] #返回期望请求
    else:
        return make_response(jsonify({"msg":"数据库未查询到对应url的返回内容，请检查url和id(如果加入请求的话)"}))