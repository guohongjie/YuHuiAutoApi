#!/usr/bin/python
#-*-coding:utf-8 -*-
from app import db
from flask_login import UserMixin
class DeptName(db.Model):
    __bind_key__ = 'qa_user'
    __tablename__ = "Dept"  # 部门表
    deptId = db.Column(db.Integer,primary_key=True)#序号ID
    deptName = db.Column(db.String(100)) # 项目
    status = db.Column(db.Boolean,default=0)
    def __init__(self,deptId,deptName,status=0):
        self.deptId = deptId
        self.deptName = deptName
        self.status = status
    def __repr__(self):
        return '<Case %r>'%(self.deptName)
class User(db.Model,UserMixin):
    __bind_key__ = 'qa_user'
    __tablename__ = "User"  # 部门表
    userId = db.Column(db.Integer,primary_key=True)#序号ID
    userName = db.Column(db.String(100)) # 项目
    status = db.Column(db.Boolean,default=0)
    deptId = db.Column(db.Integer,db.ForeignKey('Dept.deptId'))
    phone = db.Column(db.String(11))
    mail = db.Column(db.String(100))
    imgUrl = db.Column(db.String(100))
    def __init__(self,userId,userName,deptId,phone,mail,imgUrl=None,status=0):
        self.userId = userId
        self.userName = userName
        self.status = status
        self.deptId = deptId
        self.phone = phone
        self.mail = mail
        self.imgUrl = imgUrl
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return unicode(self.userId)
    def __repr__(self):
        return '<Case %r>'%(self.userName)
class Manager(db.Model,UserMixin):
    __bind_key__ = 'qa_user'
    __tablename__ = "Manager"  # 部门表
    userId = db.Column(db.Integer,primary_key=True)#序号ID
    userName = db.Column(db.String(100)) # 项目
    deptId = db.Column(db.Integer,db.ForeignKey('Dept.deptId'))
    passwd = db.Column(db.String(100))
    def __init__(self,userId,userName,passwd,deptId):
        self.userId = userId
        self.userName = userName
        self.passwd = passwd
        self.deptId = deptId
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return unicode(self.userId)
    def __repr__(self):
        return '<Case %r>'%(self.userName)
class Message(db.Model):
    __bind_key__ = 'qa_user'
    __tablename__ = "SystemMessage"  # 部门表
    id = db.Column(db.Integer,primary_key=True)#序号ID
    fromUser = db.Column(db.String(100))    #来源用户
    toUser = db.Column(db.String(100))    #推送用户
    msg = db.Column(db.Text)    #推送消息
    params = db.Column(db.String(200))
    func = db.Column(db.String(100))
    status = db.Column(db.Integer,default=0)    #'消息状态：0 未审核 1已审核；2:已拒绝',
    createDate = db.Column(db.DateTime, nullable=False)    #来源时间
    userId = db.Column(db.String(100))
    def __init__(self,createDate,fromUser,toUser,msg,params,func,userId,status=0):
        self.createDate = createDate
        self.fromUser = fromUser
        self.toUser = toUser
        self.msg = msg
        self.params = params
        self.func = func
        self.status = status
        self.userId = userId
# class Dept(db.Model):
#     __bind_key__ = 'qa_user'
#     __tablename__ = "Dept"  # 部门表
#     deptId = db.Column(db.Integer,primary_key=True)#序号ID
#     deptName = db.Column(db.String(100)) # 项目
#     status = db.Column(db.Boolean,default=0)
#     def __init__(self,deptId,deptName,status=0):
#         self.deptId = deptId
#         self.deptName = deptName
#         self.status = status
#     def __repr__(self):
#         return '<Case %r>'%(self.deptName)
