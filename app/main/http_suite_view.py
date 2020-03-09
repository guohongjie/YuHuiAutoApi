#!/usr/bin/python
#-*-coding:utf-8 -*-
__author__ = "guohongjie"
from flask import render_template,request,flash,make_response,jsonify,send_from_directory,send_file
from app.main import views
from app import db
from app.config.api_models import Project
import os
from app.config.config import TEST_FOLDER

@views.route("/httpSuite",methods=["GET"])
def http_suite():
    """测试集首页，下拉项内显示项目"""
    projects = db.session.query(Project.project).all()
    return render_template("home/http_suite.html",projects=projects)

@views.route("/UploadAction",methods=["POST"])
def api_upload():
    """上传测试用例接口
    :param project:  项目名称
    :param fileList:  测试用例文件
    :return: msg
    """
    project = request.form["project"]
    xls_file = request.files['fileList']
    project_en = db.session.query(Project.project_en).filter_by(project=project).first()
    try:
        dirPath = TEST_FOLDER + "/test_setting/{project_en}".format(project_en=project_en[0])
        dirPathSuite = TEST_FOLDER + "/suite/{project_en}".format(project_en=project_en[0])
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
        if not os.path.exists(dirPathSuite):
            os.makedirs(dirPathSuite)
            f = file(TEST_FOLDER + "/suite/{project_en}/__init__.py".format(project_en=project_en[0]),
                     "w")
            del f
        xls_file.save(TEST_FOLDER + "/test_setting/{project_en}/{project_en}.xls".format(project_en=project_en[0]))
        msg = {"code":200,"Msg":"执行成功"}
    except Exception as e:
        msg = {"code": 400, "Msg": "执行失败", "ErrorMsg": str(e)}
    return make_response(jsonify(msg))

@views.route("/DownFileXls",methods=["GET"])
def download_file():
    """
    :return:  接口测试用例模板文件
    """
    directory = os.getcwd()
    return send_from_directory(directory,"jiekou.xls",as_attachment=True)
@views.route("/DownPojectXls",methods=["GET"])
def download_project_file():
    """
    :param project:  项目名称
    :param project_en:  项目名称(英文)
    :return:  接口测试用例文件
    """
    directory = os.getcwd()
    project = request.args.get("project")
    project_en = db.session.query(Project.project_en).filter_by(project=project).first()
    if project_en:
        projectPath = TEST_FOLDER + "/test_setting/{project_en}".format(project_en=project_en[0])
        directory = directory+"/"+projectPath+"/"+"{project_en}.xls".format(project_en=project_en[0])
        if os.path.exists(projectPath):
            msg = {"code":200,"Msg":"执行成功","project":project_en[0]}
    else:
        msg = {"code":400,"Msg":"下载失败","ErrorMsg":"文件路径不存在"}
    return make_response(jsonify(msg))
@views.route("/Download/<project>")
def download_xls_file(project):
    """
    下载已存在的项目用例文件
    :param project:  项目英文名称
    :return:  接口测试用例文件
    """
    projectPath = TEST_FOLDER + "/test_setting/{project_en}".format(project_en=project)
    directory = os.getcwd()+"/"+projectPath
    #print directory
    return send_from_directory(directory,"{project}.xls".format(project=project),as_attachment=True)

