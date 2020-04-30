#!/usr/bin/python
#-*-coding:utf-8 -*-
import json
def assertValue(value1,value2):
    #value1   except    value2    resp
    #value1   dict   value    str  json
    #value1   str    value    str
    if type(value1).__name__ == "str":
        msg = "Except:  {Except}-*-Really:  {Really}".format(Except=value1,Really=value2)
        assert value1==value2,msg
    if type(value1).__name__ == "dict":
        json_value1 = json.dumps(value1, encoding='utf-8', ensure_ascii=False)  # 期望值转换json
        try:
            dict_resp = json.loads(value2)
            msg = "Except:  {Except}-*-Really:  {Really}".format(Except=json_value1, Really=value2)
            assert value1==dict_resp,msg  #判断期望值==返回值(转换成字典)
        except Exception as e:  #当value2 不是json类型
            print e
            msg = "Except:  {Except}-*-Really:  {Really}".format(Except=json_value1, Really=value2)
            assert json_value1 == value2,msg

if __name__ == "__main__":
    assertValue("1","2")