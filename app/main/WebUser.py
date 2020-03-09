#!/usr/bin/python
#-*-coding:utf-8 -*-
from app.main import user
from flask import render_template,request,flash,redirect,url_for,session,g
from flask_login import login_user,logout_user,login_required
from app.config.login_form import LoginForm
from app.config.user_models import User,DeptName,Manager
from app import login_manager
import requests
import json
from app import db
@login_manager.user_loader
def load_user(userid):
    isAdmin = session.get('isAdmin')
    if isAdmin:
        return Manager.query.get(int(userid))
    else:
        return User.query.get(int(userid))
def query_user(userid):
    return True
@user.route("/",methods=["GET", 'POST'])
def webLogin():
    return redirect(url_for('views.webIndex'))
@user.route("/userLogin",methods=["GET", 'POST'])
def userLogin():
    form = LoginForm()
    if request.method == 'POST':
        url = "http://sso.sys.bandubanxie.com/api/v1/auth"
        user = form.accountNumber.data
        pwd =  form.password.data
        adminUser = Manager.query.filter(Manager.userName == user).first()  # 查询admin用户是否
        if adminUser:    #管理账号
            adminUser = Manager.query.filter(Manager.userName == user, Manager.passwd == pwd).first()    #用户&密码
            if adminUser:
                session["userName"] = adminUser.userName
                session["userId"] = "admin_%s"%(adminUser.userId)
                session["deptName"] = "管理员"
                session["isAdmin"] = True
                login_user(adminUser, remember=False)
                return redirect(url_for('views.webIndex'))
            else:
                flash(message=u'嗨~{username}!用户名或密码错误!'.format(username=form.accountNumber.data), category='error')
        else:    #普通用户账号
            params = {"Name": user, "Password": pwd, "IsLdap": "1"}
            resp = requests.post(url=url, data=params)    #SSO登录验证
            dict_resp = json.loads(resp.text, encoding="utf8")
            if resp.status_code==200 and dict_resp["code"]==0:
                user = User.query.filter(
                User.userName == dict_resp.get("data").get("UserInfo").get("Name")).first()    #查询用户是否存在
                if user:
                    dept = DeptName.query.filter(DeptName.deptId == user.deptId).first()    #查询用户部门是否存在
                    if not dept:
                        User.deptId = 1    #用户不存在部门时,部门归属为其他
                        db.session.commit()
                else:
                    insert_user = User(userId=dict_resp.get("data").get("UserInfo").get("Id"),
                                        userName=dict_resp.get("data").get("UserInfo").get("Name"),
                                       phone=dict_resp.get("data").get("UserInfo").get("Mobile"),
                                       mail=dict_resp.get("data").get("UserInfo").get("Mail"),
                                         status=1,
                                         deptId=1)
                    db.session.add(insert_user)
                    db.session.commit()
                    user = User.query.filter(
                    User.userName == dict_resp.get("data").get("UserInfo").get("Name")).first()  # 查询用户是否存在
                dept = DeptName.query.filter(DeptName.deptId == user.deptId).first()
                login_user(user, remember=False)
                session["userName"] = dict_resp.get("data").get("UserInfo").get("Name")
                session["userId"] = dict_resp.get("data").get("UserInfo").get("Id")
                session["isAdmin"] = False
                session["deptName"] = dept.deptName
                return redirect(url_for('views.webIndex'))
            else:
                flash(message=u'嗨~{username}!用户名或密码错误!'.format(username=form.accountNumber.data), category='error')
    return render_template('user/login.html',form=form)
@user.route('/logout/')
@login_required
def logout():
    logout_user()  # 登出用户
    # session.pop('userName')
    # session.pop('deptName')
    # session.pop('userId')
    # session.pop("isAdmin")
    # print dir(session)
    session.clear
    return redirect(url_for('views.webIndex'))
@user.app_errorhandler(404)
def pageNotFound(e):
    return render_template('home/404.html'),404
@user.app_errorhandler(500)
def pageNotFound(e):
    return render_template('home/500.html'),500

