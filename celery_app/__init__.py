#!/usr/bin/python
from celery import Celery,Task
from app.config import redis_db,redis_port,redis_hosts
celery = Celery('celery_app',
broker='redis://{redis_host}:{redis_port}/{redis_db}'.format(
	redis_port=redis_port,redis_db=redis_db,redis_host=redis_hosts
),
backend='redis://{redis_host}:{redis_port}/{redis_db}'.format(
	redis_port=redis_port,redis_db=redis_db,redis_host=redis_hosts
))
class MyTask(Task):
	def on_success(self, retval, task_id, args, kwargs):
		print 'task done: {0}'.format(retval)
		return super(MyTask,self).on_success(retval,task_id,args,kwargs)
	def on_failure(self, exc, task_id, args, kwargs, einfo):
		print 'task fail, reason: {0}'.format(exc)
		return super(MyTask,self).on_failure(exc,task_id,args,kwargs,einfo)
