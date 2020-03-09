#!/usr/bin/env python
#-*-coding:utf-8 -*-
import pymysql
from app.config import host,user,pwd,database,port,charset
def select_sql(sql):
	db = pymysql.connect(host, user,pwd,
						 database,port=int(port), charset=charset)
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
	db = pymysql.connect(host, user,pwd,
						 database,port=int(port), charset=charset)
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
	db = pymysql.connect(host, user,pwd,
						 database,port=int(port), charset=charset)
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
if __name__ == "__main__":
	s = """select * from case_http_api where project='%s'"""%("云舒写首页")
	print s
	datas = select_sql(s)
	print datas

