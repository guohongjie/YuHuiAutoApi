#!/usr/bin/python
#-*-coding:utf-8 -*-
from app.main import flow
from flask import render_template,request,make_response,jsonify,session
from app.config.api_models import Run_Suite,Test_Domain
from app.config.user_models import DeptName
from app import db
from sqlalchemy import func
@flow.route("/myFlowDomain",methods=["GET"])
def myFlowDomainIndex():
    """
    工作流配置主页
    :return:
    """
    # api_project = Project.query.with_entities(Project.project).distinct().all()
    #提取测试项目,传入页面中
    test_doamin = Test_Domain.query.filter(Test_Domain.statu==1).distinct().all()
    test_group = DeptName.query.filter(DeptName.status==1).all()
    return render_template("flow/flowManger.html",
                           test_groups=test_group,test_doamin=test_doamin)
@flow.route("/flowSearch",methods=["GET"])
def flowSearch():
    """
    查询工作流
    :return:
    """
    test_group = request.args.get('test_group')  # 项目组名称
    test_domain = request.args.get('test_domain')  # 项目组名称
    if test_group == 'None' and test_domain == 'None':
        # 当项目为空、接口名为空、状态为 全部
        datas = Run_Suite.query.all()
    elif test_group != 'None' and test_domain == 'None':
        datas = Run_Suite.query.filter(Run_Suite.test_group==test_group).all()
    elif test_group != 'None' and test_domain != 'None':
        datas = Run_Suite.query.filter(Run_Suite.test_group == test_group
                                       ).filter(
                            func.find_in_set(test_domain,Run_Suite.domain)).order_by(
                            Run_Suite.RunOrderId).all()
    else:
        datas = Run_Suite.query.filter(
            func.find_in_set(test_domain,Run_Suite.domain)
            ).order_by(Run_Suite.RunOrderId).all()
    suiteList = []
    for singleDatas in datas:
        suiteDatas = {"id":singleDatas.id,
                      "RunOrderId":singleDatas.RunOrderId,
                     "domain":singleDatas.domain,
                      "name":singleDatas.suiteName,
                      "desc":singleDatas.description,
                      "statu": "启用" if singleDatas.statu else "停用",
                      "test_group":singleDatas.test_group}
        suiteList.append(suiteDatas)
    resp = {"status": 200, "datas": suiteList}
    msg_resp = make_response(jsonify(resp))
    return msg_resp
@flow.route("/flowSingleDatas",methods=["GET"])
def flowSingleDatas():
    """修改查询数据"""
    flow_id = request.args.get("flow_id")
    datas = Run_Suite.query.filter(Run_Suite.id==flow_id).first()
    deptNameSession = session.get("deptName")
    isAdmin = session.get("isAdmin")
    if datas.test_group != deptNameSession and isAdmin != True:
        resp = {'datas': "当前部门与工作流所属部门不同,无权限修改!", 'code': '400'}
        return make_response(jsonify(resp))
    msg = {"id":datas.id,
        "test_group":datas.test_group,
           "name":datas.suiteName,
           "domain":datas.domain,
           "statu":datas.statu,
           "desc":datas.description,
           "user":datas.user,
           "flow_order":datas.RunOrderId}
    resp ={"status":200,"datas":msg}
    return make_response(jsonify(resp))
@flow.route("/flowSaveUpdate",methods=["GET"])
def flowSaveUpdate():
    """
    保存修改功能
    :return:
    """
    flow_id = request.args.get("flow_id")
    flow_name = request.args.get("flow_name")
    flow_domain = request.args.get("flow_domain")
    flow_statu = request.args.get("flow_statu")
    flow_desc = request.args.get("flow_desc")
    user = request.args.get("tester")
    flow_order = request.args.get("flow_order")
    if not flow_order.isdigit():
        resp = {'datas': "执行序号必须为数字", 'code': '400'}
        return make_response(jsonify(resp))
    try:
        datas = Run_Suite.query.filter_by(id=flow_id).update(dict(user=user,
                                                              suiteName=flow_name,
                                                              domain=flow_domain,
                                                              statu= 1 if flow_statu=="1" else 0,
                                                              RunOrderId=int(flow_order),
                                                              description=flow_desc))
        db.session.commit()
        resp = {'datas': '更新成功', 'code': '200'}
    except Exception as e:
        db.session.rollback()
        resp = {'datas': str(e), 'code': '400'}
    return make_response(jsonify(resp))
@flow.route("/flowDelete",methods=["GET"])
def flowDelete():
    flow_id = request.args.get("flow_id")
    datas = Run_Suite.query.filter(Run_Suite.id == flow_id).first()
    deptNameSession = session.get("deptName")
    isAdmin = session.get("isAdmin")
    if datas.test_group != deptNameSession and isAdmin != True:
        resp = {'datas': "当前部门与工作流所属部门不同,无权限修改!", 'code': '400'}
        return make_response(jsonify(resp))
    else:
        try:
            db.session.delete(datas)
            db.session.commit()
            resp = {'datas': '删除成功', 'code': '200'}
        except Exception as e:
            db.session.rollback()
            resp = {"code": 400, "datas": str(e)}
        return make_response(jsonify(resp))