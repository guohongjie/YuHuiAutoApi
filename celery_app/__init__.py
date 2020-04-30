#!/usr/bin/python
from celery import Celery,Task
celery = Celery('celery_app',
broker='redis://localhost:6379/1',
backend='redis://localhost:6379/2')
class MyTask(Task):
	def on_success(self, retval, task_id, args, kwargs):
		print 'task done: {0}'.format(retval)
		return super(MyTask,self).on_success(retval,task_id,args,kwargs)
	def on_failure(self, exc, task_id, args, kwargs, einfo):
		print 'task fail, reason: {0}'.format(exc)
		return super(MyTask,self).on_failure(exc,task_id,args,kwargs,einfo)
