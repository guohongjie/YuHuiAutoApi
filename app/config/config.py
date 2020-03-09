#!/usr/bin/python
#-*-coding:utf-8 -*-
"""
@author: guohongjie
"""
import os
from app.config.getDataFromXml import get_from_xml
TEST_FOLDER = './app/base/pythonProject'
def get_datas():
	host = get_from_xml(gen="service")["host"]
	port = int(get_from_xml(gen="service")["port"])
	user = get_from_xml(gen="service")["user"]
	pwd = get_from_xml(gen="service")["pwd"]
	database = get_from_xml(gen="service")["database"]
	database2 = get_from_xml(gen="service")["database2"]
	charset = get_from_xml(gen="service")["charset"]
	redis_host = get_from_xml(gen="redis")["host"]
	redis_port = int(get_from_xml(gen="redis")["port"])
	redis_db = int(get_from_xml(gen="redis")["db"])
	return {"host":host,"port":port,
			"user":user,"pwd":pwd,"database":database,
			"database2":database2,"charset":charset,
			"redis_host":redis_host,"redis_port":redis_port,
			"redis_db":redis_db}
class TestingConfig(object):#研发环境配置
	datas = get_datas()
	SECRET_KEY = 'guohongjie'
	basedir=os.path.abspath(os.path.dirname(__file__))
	SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{user}:{pwd}@{host}:{port}/{database}?charset={charset}".format(user=datas["user"],pwd=datas["pwd"],
																													  host=datas["host"],port=datas["port"],
																													  database=datas["database"],charset=datas["charset"])
	SQLALCHEMY_BINDS = {
		"{database}".format(database=datas["database2"]): "mysql+mysqlconnector://{user}:{pwd}@{host}:{port}/{database}?charset={charset}".format(user=datas["user"],pwd=datas["pwd"],
																													  host=datas["host"],port=datas["port"],
																													  database=datas["database2"],charset=datas["charset"])
	}
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	CSRF_ENABLED = True
	DEBUG = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	JSON_AS_ASCII = False
	REDIS_HOST = datas["redis_host"]
	REDIS_PORT = datas["redis_port"]
	REDIS_DB = datas["redis_db"]
	CELERY_BROKER_URL = 'redis://{redis_host}:{redis_port}/1'.format(redis_host=datas["redis_host"],
																	 redis_port=datas["redis_port"])
	CELERY_RESULT_BACKEND = 'redis://{redis_host}:{redis_port}/2'.format(redis_host=datas["redis_host"],
																		 redis_port=datas["redis_port"])
	@staticmethod
	def init_app(app):
		pass
class Project(object):
	#线上环境的配置
	datas = get_datas()
	SECRET_KEY = 'guohongjie'
	basedir = os.path.abspath(os.path.dirname(__file__))
	SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{user}:{pwd}@{host}:{port}/{database}?charset={charset}".format(user=datas["user"],
																													  pwd=datas["pwd"],
																													  host=datas["host"],
																													  port=datas["port"],
																													  database=datas["database"],
																													  charset=datas["charset"])
	SQLALCHEMY_BINDS = {
		"{database}".format(database=datas["database2"]): "mysql+mysqlconnector://{user}:{pwd}@{host}:{port}/{database}?charset={charset}".format(user=datas["user"],
																													  pwd=datas["pwd"],
																													  host=datas["host"],
																													  port=datas["port"],
																													  database=datas["database2"],
																													  charset=datas["charset"])
	}
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	CSRF_ENABLED = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	JSON_AS_ASCII = False
	REDIS_HOST = datas["redis_host"]
	REDIS_PORT = datas["redis_port"]
	@staticmethod
	def init_app(app):
		pass
def lod():
	return TestingConfig
class Config(object):
	JOBS = [ ]
	SCHEDULER_API_ENABLED = True
config = {
    'testing': TestingConfig,
    'production': Project,
    'default': TestingConfig
}

if __name__ == "__main__":
	print get_datas()