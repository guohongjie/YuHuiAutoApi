#!/usr/bin/python
#-*-coding:utf-8 -*-
"""
@author: guohongjie
"""
import os
max_connec_redis=10
test_fail_try_num=3
PageShow=25#这里配置的就是每个页显示多少条数据
OneAdminCount=10 #设置项目管理员的数量
Config_daoru_xianzhi=50#配置可以导入限制
TEST_FOLDER = './app/base/pythonProject'


class TestingConfig(object):#研发环境配置
	SECRET_KEY = 'guohongjie'
	basedir=os.path.abspath(os.path.dirname(__file__))
	SQLALCHEMY_DATABASE_URI = "qa_automation?charset=utf8"
	SQLALCHEMY_BINDS = {
		"qa_user": "mysql+mysqlconnector://qa_user?charset=utf8"
	}
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	CSRF_ENABLED = True
	DEBUG = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	JSON_AS_ASCII = False
	REDIS_HOST = "localhost"
	REDIS_PORT = 6379
	REDIS_DB = 0
	CELERY_BROKER_URL = 'redis://localhost:6379/1'
	CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'
	@staticmethod
	def init_app(app):
		pass
class Project(object):
	#线上环境的配置
	SECRET_KEY = 'guohongjie'
	basedir = os.path.abspath(os.path.dirname(__file__))
	SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector:///qa_automation?charset=utf8"
	SQLALCHEMY_BINDS = {
		"qa_user": "mysql+mysqlconnector:///qa_user?charset=utf8"
	}
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	CSRF_ENABLED = True
	UPLOAD_FOLDER = '/upload'
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	JSON_AS_ASCII = False
	REDIS_HOST = "localhost"
	REDIS_PORT = 6379
	@staticmethod
	def init_app(app):
		pass
def lod():
	return TestingConfig
class Config(object):
	JOBS = [ ]
	SCHEDULER_API_ENABLED = True
class SystemConfig(object):
	pass
config = {
    'testing': TestingConfig,
    'production': Project,
    'default': TestingConfig
}