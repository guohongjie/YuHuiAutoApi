#!/usr/bin/env python
#-*-coding:utf-8 -*-
import pymysql

def select_sql(sql):
	#db = pymysql.connect("192.168.12.186","test","test","qa_automation",charset='utf8')
	db = pymysql.connect("172.17.0.203", "qa_all", "stz8HxsG7weemkd", "qa_automation",port=3306, charset='utf8')
	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()
	# 使用execute方法执行SQL语句
	cursor.execute("set character_set_connection=utf8")
	cursor.execute("set character_set_client=utf8")
	cursor.execute("set character_set_connection=utf8")
	cursor.execute("set character_set_results=utf8")
	cursor.execute("set character_set_server=utf8")
	cursor.execute('SET NAMES UTF8') 
	cursor.execute(sql)
	# 使用 fetchone() 方法获取一条数据
	data = cursor.fetchall()
	# 关闭数据库连接
	db.close()
	return data
def insert_sql(sql):
	# db = pymysql.connect('192.168.12.186','test','test','ApiTestDB',charset='utf8')
	db = pymysql.connect("172.17.0.203", "qa_all", "stz8HxsG7weemkd", "qa_automation",port=3306, charset='utf8')
	cursor = db.cursor()
	cursor.execute("set character_set_connection=utf8")
	cursor.execute("set character_set_client=utf8")
	cursor.execute("set character_set_connection=utf8")
	cursor.execute("set character_set_results=utf8")
	cursor.execute("set character_set_server=utf8")
	cursor.execute('SET NAMES UTF8') 
	try:
		cursor.execute(sql)
		db.commit()
		db.close()
		return {"result":True,"reson":"Insert successful"}
	except Exception as e:
		db.rollback()
		db.close()
		return {"result":False,"reson":str(e)}
def update_sql(sql):
	# db = pymysql.connect('192.168.12.186', 'test', 'test', 'ApiTestDB', charset='utf8')
	db = pymysql.connect("172.17.0.203", "qa_all", "stz8HxsG7weemkd", "qa_automation",port=3306, charset='utf8')
	cursor = db.cursor()
	cursor.execute("set character_set_connection=utf8")
	cursor.execute("set character_set_client=utf8")
	cursor.execute("set character_set_connection=utf8")
	cursor.execute("set character_set_results=utf8")
	cursor.execute("set character_set_server=utf8")
	cursor.execute('SET NAMES UTF8')
	try:
		cursor.execute(sql)
		db.commit()
		db.close()
		return {"result":True,"reson":"Update successful"}
	except Exception as e:
		db.rollback()
		db.close()
		return {"result":False,"reson":str(e)}

class betaDB(object):
	def __init__(self):
		self.db = pymysql.connect('172.17.1.240', 'ysx_beta_writer', 'rzcXYilPKauGMCIz1dQ3AOzzO7Y-', 'ysx_order', port=3316,charset='utf8')
		self.cursor = self.db.cursor()
	def execute_sql(self,sql):
		self.cursor.execute(sql)
		self.db.commit()
	def execute_select(self,sql):
		self.cursor.execute(sql)
		data = self.cursor.fetchall()
		return data
	def execute_close(self):
		self.db.close()
class betaDB_order(object):
	def __init__(self):
		self.db = pymysql.connect('172.17.1.238', 'ysx_beta_writer', 'rzcXYilPKauGMCIz1dQ3AOzzO7Y-', 'ysx_order', port=3318,charset='utf8')
		self.cursor = self.db.cursor()
	def execute_sql(self,sql):
		self.cursor.execute(sql)
		self.db.commit()
	def execute_select(self,sql):
		self.cursor.execute(sql)
		data = self.cursor.fetchall()
		return data
	def execute_close(self):
		self.db.close()
class SelectData(object):
	def __init__(self,host,name,pwd,database,port):
		self.db = pymysql.connect(host,
								  name,
								  pwd,
								  database, port=port,charset='utf8')
		self.cursor = self.db.cursor()
	def execute_select(self,sql):
		self.cursor.execute(sql)
		data = self.cursor.fetchall()
		return data
	def execute_close(self):
		self.db.close()
if __name__ == "__main__":
# 	s = """select * from case_http_api where project='%s' and scheduling='0'"""%("云舒写首页")
# 	print s
# 	datas = select_sql(s)
	# ss= """insert into behave_config values('Given 操作页面HTML元素','输入')"""
	# tupledate = insert_sql(ss)
	# sss = """insert into behave_config values('Given 操作页面HTML元素','单击')"""
	# tupledate = insert_sql(sss)
	# ssss = """insert into behave_config values('Then 执行js代码','对弹框操作')"""
	# tupledate = insert_sql(ssss)
	# sssss = """insert into behave_config values('Given 操作页面HTML元素','添加')"""
	# tupledate = insert_sql(sssss)
	# a = """insert into behave_config values('Given 操作页面HTML元素','删除')"""
	# tupledate = insert_sql(a)
	# aa = """insert into behave_config values('Then 移动鼠标','元素区')"""
	# tupledate = insert_sql(aa)
	# aaa= """insert into behave_config values('Then 添加等待时间','秒等待')"""
	# tupledate = insert_sql(aaa)
	# print datas
	s = betaDB_order()
	sql = 'select a.ORDER_STATE,a.CALLBACK_TIME,a.* from ysx_order.ysx_order_info a where a.order_sn ="Y1100157172551292618"'
	print s.execute_sql(sql)
	print s.execute_sql("select 1 from dual")
	print s.execute_close()

