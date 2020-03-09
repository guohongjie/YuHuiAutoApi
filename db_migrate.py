#!/usr/bin/python
#-*-coding:utf-8 -*-
"""
@author: guohongjie
"""
'''数据库同步使用'''
from flask_migrate import Migrate,MigrateCommand
from flask_script import  Manager
from app import db,create_app
app = create_app("default")
manage=Manager(app)
migrate=Migrate(app,db)
manage.add_command('db',MigrateCommand)
if __name__=='__main__':
    manage.run()