#!/usr/bin/python
#-*-coding:utf-8 -*-
from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(Form):
    accountNumber = StringField('accountNumber',
                                validators=[DataRequired(u"用户名不能为空")],
                                render_kw={'rows': 20,"autocomplete":"off","required":"required","class":"from-control",
                                           'placeholder': u'用户名'})
    password = PasswordField('password', validators=[DataRequired(u"密码不能为空")],
                             render_kw={'rows': 20, "autocomplete": "off","required":"required","class":"from-control",
                                        'placeholder': u'密码'})