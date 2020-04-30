#!/usr/bin/python
#-*-coding:
import os
import codecs
import configparser

configPath = os.path.join("./app/base/pythonProject/config", "config.ini")
#configPath = os.path.join("./../../config", "config.ini")
# print configPath
class ReadConfig:
    def __init__(self):
        with open(configPath) as fd:
            data = fd.read()
            if data[:3] == codecs.BOM_UTF8:
                data = data[3:]
                file = codecs.open(configPath, "w")
                file.write(data)
                file.close()

        self.cf = configparser.ConfigParser()
        self.cf.read(configPath)

    def get_env(self, name):
        value = self.cf.get("ENV", name)
        return value

    def get_params(self, name):
        value = self.cf.get("PARAMS", name)
        return value
    def get_admin(self, name):
        value = self.cf.get("ADMIN", name)
        return value

    def add_set(self,section,**kwargs):
        dictA = kwargs
        for key,value in dictA.items():
            self.cf.set(section,key,value)
        with open(configPath,"w") as f:
            self.cf.write(f)

s=ReadConfig()
env_flag = s.get_env("env_flag")
env_num = s.get_env("env_num")
phoneNum = s.get_params("phoneNum")
userName = s.get_admin("userName")
pwd = s.get_admin("pwd")

if __name__ == "__main__":
    import sys
    if sys.getdefaultencoding()!="utf8":
        reload(sys)
        sys.setdefaultencoding("utf8")
    print env_flag
    print env_num
    print phoneNum
    print pwd
    print userName