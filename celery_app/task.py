#!/usr/bin/python
#-*-coding:utf-8 -*-
from . import celery
@celery.task()
def wctv(msg):
    with open("/app/celery_app/wctv.log","a+") as f:
        f.write(msg)
    return "wctv"
if __name__ == "__main__":
    s = wctv.delay("wctv")
