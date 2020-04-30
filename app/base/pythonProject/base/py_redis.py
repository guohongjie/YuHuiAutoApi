#!/usr/bin/python
#-*-coding:utf-8 -*-
import redis
class MyRedis(object):
    def __init__(self):
        try:
            self.r = redis.Redis(host="localhost", port=6379)
        except Exception as e:
            print "redis 连接失败，错误信息%s"%(str(e))
    def str_get(self,key):
        res = self.r.get(key)
        return res
    def str_set(self,key,value,ex=60):
        res = self.r.set(key,value,ex=ex)
        return res
    def del_key(self,key):
        res = self.r.delete(key)
        return res


def fromRedis(setKey=None,getKey=None):
    def outer(func):
        def inner(self):
            rs = MyRedis()
            if getKey != None and setKey != None:
                get_datas = dict(zip(getKey,map(lambda x: rs.str_get(x),getKey)))
                set_datas = func(self,get_datas)
                if set_datas:
                    if len(setKey) == len(set_datas) :
                        for i in range(len(setKey)):
                            rs.str_set(setKey[i],set_datas[i])
                    else:
                        raise Exception,u"fromRedis Error:setKey length and set_Key's length not equal "
            elif getKey != None and setKey == None:
                get_datas = dict(zip(getKey,map(lambda x: rs.str_get(x),getKey)))
                func(self, get_datas)
            elif getKey == None and setKey != None:
                set_datas = func(self)
                if set_datas:
                    if len(setKey) == len(set_datas):
                        for i in range(len(setKey)):
                            rs.str_set(setKey[i], set_datas[i])
                    else:
                        raise Exception,u"fromRedis Error:setKey length and set_Key's length not equal "
        return inner
    return outer
if __name__ == "__main__":
    s = MyRedis()
    s.str_set("wc","1234")