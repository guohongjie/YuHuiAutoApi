#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import unittest
import json
from app.base.pythonProject.base.log import TestLog,fengefu,lianjiefu
from app.base.pythonProject.base.py_redis import MyRedis
from app.base.pythonProject.base.getCookies import get_xsjz_cookie
import time
logging = TestLog().getlog()
class ProductType_Test(unittest.TestCase):
    """销售简章-SKU相关操作协议"""
    @classmethod
    def setUpClass(self):
        redis = MyRedis()
        env_flag = redis.str_get("wacc_tortoise_env_flag")
        env_num = redis.str_get("wacc_tortoise_env_num")
        self.session = requests.Session()
        cookies = get_xsjz_cookie(env_flag,env_num)
        header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","Content-Type":"application/x-www-form-urlencoded","Accept":"application/json, text/plain, */*","Connection":"keep-alive"}
        self.msg = """\n        Expect:  {Expect}-*-\n        Really:  {Really}"""  # 校验HTTP返回代码
        self.session.headers = header
        self.session.cookies = cookies
    def test_01_sku_save(self):
        """添加sku接口协议<br/>http://adm.yunshuxie.com/api/sku/save.htm<br/>{"pTitle":"测试-pTitle-{timestamp}","pId":"","childTitle":"测试-childTitle-{timestamp}"}
        """
        url = r"http://adm.yunshuxie.com"+"/api/sku/save.htm"
        timestamp = "%d"%(time.time())
        params = {"pTitle":"测试-pTitle-{timestamp}".format(timestamp=timestamp),"pId":"","childTitle":"测试-childTitle-{timestamp}".format(timestamp=timestamp)}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url,data=params)
        print self.resp.text
        result = json.loads(self.resp.text,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.content + fengefu)
        expect = {"code":"0"}
        if result ["code"] == "0" or result["code"] == 0:
            assert result["code"]==expect["code"],self.msg.format(Expect=expect["code"],Really=result["code"])
        else:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],
                                                                     Really=result["code"])
    def test_02_productType_save(self):
        """添加类目接口协议-父级节点新增-下级类目未空<br/>http://adm.yunshuxie.com/api/productType/save.htm<br/>{"pTitle":"测试-pTitle-{timestamp}","pId":"","childTitle":""}
        """
        url = r"http://adm.yunshuxie.com"+"/api/productType/save.htm"
        timestamp = "%d"%(time.time())
        params = {"pTitle":"测试-pTitle-{timestamp}".format(timestamp=timestamp),"pId":"","childTitle":""}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url,data=params)
        print self.resp.text
        result = json.loads(self.resp.text,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"code":"0"}
        if result ["code"] == "0" or result["code"] == 0:
            assert result["code"]==expect["code"],self.msg.format(Expect=expect["code"],Really=result["code"])
        else:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],
                                                                     Really=result["code"])
    def test_03_productType_save(self):
        """添加类目接口协议-父级节点非新增-存在下级类目<br/>http://adm.yunshuxie.com/api/productType/save.htm<br/>{"pTitle":"测试-pTitle-{timestamp}","pId":"","childTitle":""}
        """
        url = r"http://adm.yunshuxie.com"+"/api/productType/save.htm"
        timestamp = "%d"%(time.time())
        params = {"pTitle":"测试-pTitle-{timestamp}".format(timestamp=timestamp),"pId":"1","childTitle":"测试-childTitle-{timestamp}".format(timestamp=timestamp)}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url,data=params)
        print self.resp.text
        result = json.loads(self.resp.text,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"code":"0"}
        if result ["code"] == "0" or result["code"] == 0:
            assert result["code"]==expect["code"],self.msg.format(Expect=expect["code"],Really=result["code"])
        else:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],
                                                                     Really=result["code"])
    def test_04_productType_save(self):
        """添加类目接口协议-pTitle为空<br/>http://adm.yunshuxie.com/api/productType/save.htm<br/>{"pTitle":"","pId":"","childTitle":""}
        """
        url = r"http://adm.yunshuxie.com"+"/api/productType/save.htm"
        timestamp = "%d"%(time.time())
        params = {"pTitle":"","pId":"1","childTitle":"测试-childTitle-{timestamp}".format(timestamp=timestamp)}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url,data=params)
        print self.resp.text
        result = json.loads(self.resp.text,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"code":"1"}
        if result ["code"] == "1" or result["code"] == 1:
            assert result["code"]==expect["code"],self.msg.format(Expect=expect["code"],Really=result["code"])
        else:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],
                                                                     Really=result["code"])
    def test_05_productType_getRow(self):
        """获取单条类目首级节点对应信息接口协议<br/>http://adm.yunshuxie.com/api/productType/getRow.htm<br/>{"id":112}
        """
        url = r"http://adm.yunshuxie.com"+"/api/productType/getRow.htm"
        params = {"id":112}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url,data=params)
        print self.resp.text
        result = json.loads(self.resp.text,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"code":"0"}
        if result ["code"] == "0" or result["code"] == 0:
            assert result["code"]==expect["code"],self.msg.format(Expect=expect["code"],Really=result["code"])
        else:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],
                                                                     Really=result["code"])
    def test_06_productType_getList(self):
        """获取单条类目首级节点对应信息接口协议"title":"测试"<br/>http://adm.yunshuxie.com/api/productType/getList.htm<br/>{"pageIndex":1,"pageSize":2,"title":"测试"}
        """
        url = r"http://adm.yunshuxie.com"+"/api/productType/getList.htm"
        params = {"pageIndex":1,"pageSize":2,"title":"测试"}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url,data=params)
        print self.resp.text
        result = json.loads(self.resp.text,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"code":"0"}
        if result ["code"] == "0" or result["code"] == 0:
            assert result["code"]==expect["code"],self.msg.format(Expect=expect["code"],Really=result["code"])
        else:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],
                                                                     Really=result["code"])
    def test_07_productType_getList(self):
        """获取单条类目首级节点对应信息接口协议"title":""<br/>http://adm.yunshuxie.com/api/productType/getList.htm<br/>{"pageIndex":1,"pageSize":2,"title":""}
        """
        url = r"http://adm.yunshuxie.com"+"/api/productType/getList.htm"
        params = {"pageIndex":1,"pageSize":2,"title":""}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url,data=params)
        print self.resp.text
        result = json.loads(self.resp.text,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"code":"0"}
        if result ["code"] == "0" or result["code"] == 0:
            assert result["code"]==expect["code"],self.msg.format(Expect=expect["code"],Really=result["code"])
        else:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],
                                                                     Really=result["code"])
    def test_08_productType_getTreeList(self):
        """商品类型树形结构接口协议<br/>http://adm.yunshuxie.com/api/productType/getTreeList.htm
        """
        url = r"http://adm.yunshuxie.com"+"/api/productType/getTreeList.htm"
        self.resp = self.session.post(url=url)
        print self.resp.text
        result = json.loads(self.resp.text,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"code":"0"}
        if result ["code"] == "0" or result["code"] == 0:
            assert result["code"]==expect["code"],self.msg.format(Expect=expect["code"],Really=result["code"])
        else:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],
                                                                     Really=result["code"])
    def test_09_productType_update(self):
        """获取单条类目首级节点对应信息接口协议"title":""<br/>http://adm.yunshuxie.com/api/productType/update.htm<br/>{"id":112,"title":""}
        """
        url = r"http://adm.yunshuxie.com"+"/api/productType/update.htm"
        params = {"id":112,"title":""}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url,data=params)
        print self.resp.text
        result = json.loads(self.resp.text,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"code":"1"}
        if result ["code"] == "1" or result["code"] == 1:
            assert result["code"]==expect["code"],self.msg.format(Expect=expect["code"],Really=result["code"])
        else:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],
                                                                     Really=result["code"])
    def test_10_productType_update(self):
        """获取单条类目首级节点对应信息接口协议"title":"自动化测试"<br/>http://adm.yunshuxie.com/api/productType/update.htm<br/>{"id": 112, "title": "自动化测试"}
        """
        url = r"http://adm.yunshuxie.com" + "/api/productType/update.htm"
        params = {"id": 112, "title": "自动化测试"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url, data=params)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"code": "10001"}
        if result["code"] == "10001" or result["code"] == 10001:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"], Really=result["code"])
        else:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],
                                                                     Really=result["code"])
    def test_11_productType_update(self):
        """获取单条类目首级节点对应信息接口协议-与商品产生关联<br/>http://adm.yunshuxie.com/api/productType/update.htm<br/>{"id": 112, "title": "自动化测试"}
        """
        url = r"http://adm.yunshuxie.com" + "/api/productType/update.htm"
        params = {"id": 112, "title": "自动化测试"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url, data=params)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"code": "10001"}
        if result["code"] == "10001" or result["code"] == 10001:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"], Really=result["code"])
        else:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],
                                                                     Really=result["code"])
    def test_12_productType_delete(self):
        """删除类目接口协议<br/>http://adm.yunshuxie.com/api/productType/delete.htm<br/>{"id": 112}
        """
        url = r"http://adm.yunshuxie.com" + "/api/productType/delete.htm"
        params = {"id": 2}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url, data=params)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"code": "0"}
        if result["code"] == "0" or result["code"] == 0:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"], Really=result["code"])
        else:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],
                                                                     Really=result["code"])
    def test_13_productType_delete(self):
        """删除类目接口协议-商品已关联<br/>http://adm.yunshuxie.com/api/productType/delete.htm<br/>{"id": 112}
        """
        url = r"http://adm.yunshuxie.com" + "/api/productType/delete.htm"
        params = {"id": 112}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url, data=params)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"code": "10001"}
        if result["code"] == "10001" or result["code"] == 10001:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"], Really=result["code"])
        else:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],
                                                                     Really=result["code"])
    @classmethod
    def tearDownClass(self):
        pass

if __name__ == "__main__":
    unittest.main()