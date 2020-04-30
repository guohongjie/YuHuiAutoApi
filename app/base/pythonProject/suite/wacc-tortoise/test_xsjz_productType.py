#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import unittest
import json
from app.base.pythonProject.base.log import TestLog,fengefu,lianjiefu
from app.base.pythonProject.base.py_redis import MyRedis
from app.base.pythonProject.base.getCookies import get_wacc_tortoise_cookie
import time
logging = TestLog().getlog()
class ProductType_Test(unittest.TestCase):
    """销售简章-类目相关协议"""
    @classmethod
    def setUpClass(self):
        self.redis = MyRedis()
        env_flag = self.redis.str_get("wacc_tortoise_env_flag")
        env_num = self.redis.str_get("wacc_tortoise_env_num")
        self.timestamp = "%d" % (time.time())
        self.session = requests.Session()
        cookies = get_wacc_tortoise_cookie(env_flag,env_num)
        header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","Content-Type":"application/x-www-form-urlencoded","Accept":"application/json, text/plain, */*","Connection":"keep-alive"}
        self.msg = """\n        Expect:  {Expect}-*-\n        Really:  {Really}"""  # 校验HTTP返回代码
        self.session.headers = header
        self.session.cookies = cookies
    def test_01_productType_save(self):
        """添加类目类目协议-父级节点新增<br/>http://adm.yunshuxie.com/api/productType/save.htm<br/>{"pTitle":"类目测试-pTitle-{timestamp}","pId":"","childTitle":"类目测试-childTitle-{timestamp}"}
        """
        url = r"http://adm.yunshuxie.com"+"/api/productType/save.htm"
        params = {"pTitle":"类目测试-pTitle-{timestamp}".format(timestamp=self.timestamp),"pId":"",
                  "childTitle":"类目测试-childTitle-{timestamp}".format(timestamp=self.timestamp)}
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
        self.redis.str_set("pTitle",params["pTitle"])
    def test_02_productType_save(self):
        """添加类目类目协议-父级节点新增-下级类目未空<br/>http://adm.yunshuxie.com/api/productType/save.htm<br/>{"pTitle":"类目测试-pTitle-{timestamp}","pId":"","childTitle":""}
        """
        url = r"http://adm.yunshuxie.com"+"/api/productType/save.htm"
        params = {"pTitle":"类目测试-pTitle-{timestamp}".format(timestamp=self.timestamp),"pId":"","childTitle":""}
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
        """添加类目类目协议-父级节点非新增-存在下级类目<br/>http://adm.yunshuxie.com/api/productType/save.htm<br/>{"pTitle":"类目测试-pTitle-{timestamp}","pId":"","childTitle":""}
        """
        url = r"http://adm.yunshuxie.com"+"/api/productType/save.htm"
        params = {"pTitle":"类目测试-pTitle-{timestamp}".format(timestamp=self.timestamp),"pId":"1",
                  "childTitle":"类目测试-childTitle-{timestamp}".format(timestamp=self.timestamp)}
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
        """添加类目类目协议-pTitle为空<br/>http://adm.yunshuxie.com/api/productType/save.htm<br/>{"pTitle":"","pId":"","childTitle":""}
        """
        url = r"http://adm.yunshuxie.com"+"/api/productType/save.htm"
        params = {"pTitle":"","pId":"1","childTitle":"类目测试-childTitle-{timestamp}".format(timestamp=self.timestamp)}
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
    def test_05_productType_getList(self):
        """获取单条类目首级节点对应信息类目协议"title":"类目测试"<br/>http://adm.yunshuxie.com/api/productType/getList.htm<br/>{"pageIndex":0,"pageSize":1,"title":"类目测试"}
        """
        pTitle = self.redis.str_get("pTitle")
        url = r"http://adm.yunshuxie.com"+"/api/productType/getList.htm"
        params = {"pageIndex":0,"pageSize":10,"title":pTitle}
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
        self.redis.str_set("productId",result["data"]["list"][0]["id"])
        self.redis.str_set("delete_productId", result["data"]["list"][1]["id"])
    def test_06_productType_getList(self):
        """获取单条类目首级节点对应信息类目协议"title":""<br/>http://adm.yunshuxie.com/api/productType/getList.htm<br/>{"pageIndex":1,"pageSize":2,"title":""}
         """
        url = r"http://adm.yunshuxie.com" + "/api/productType/getList.htm"
        params = {"pageIndex": 1, "pageSize": 2, "title": ""}
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
    def test_07_productType_getRow(self):
        """获取单条类目首级节点对应信息类目协议<br/>http://adm.yunshuxie.com/api/productType/getRow.htm<br/>{"id":}
        """
        productId = self.redis.str_get("productId")
        url = r"http://adm.yunshuxie.com"+"/api/productType/getRow.htm"
        params = {"id":productId}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False,encoding="utf8") + fengefu)
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
        """商品类型树形结构类目协议<br/>http://adm.yunshuxie.com/api/productType/getTreeList.htm
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
        """获取单条类目首级节点对应信息类目协议"title":""<br/>http://adm.yunshuxie.com/api/productType/update.htm<br/>{"id":112,"title":""}
        """
        productId = self.redis.str_get("productId")
        url = r"http://adm.yunshuxie.com"+"/api/productType/update.htm"
        params = {"id":productId,"title":""}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False,encoding="utf8") + fengefu)
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
        """获取单条类目首级节点对应信息类目协议"title":"类目测试-修改"<br/>http://adm.yunshuxie.com/api/productType/update.htm<br/>{"id": , "title": "类目测试-修改"}
        """
        productId = self.redis.str_get("productId")
        url = r"http://adm.yunshuxie.com" + "/api/productType/update.htm"
        params = {"id": productId, "title": "类目测试-修改"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False,encoding="utf8") + fengefu)
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
    def test_11_productType_delete(self):
        """删除类目类目协议<br/>http://adm.yunshuxie.com/api/productType/delete.htm<br/>{"id": }
        """
        productId = self.redis.str_get("productId")
        url = r"http://adm.yunshuxie.com" + "/api/productType/delete.htm"
        params = {"id": productId}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False,encoding="utf8") + fengefu)
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
        productId = self.redis.str_get("delete_productId")
        params = {"id": productId}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False, encoding="utf8") + fengefu)
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
    def test_12_productType_update(self):
        """获取单条类目首级节点对应信息类目协议-与商品产生关联<br/>http://adm.yunshuxie.com/api/productType/update.htm<br/>{"id":, "title": "类目测试"}
        """
        productId = self.redis.str_get("productId")
        def add_spu_save():
            """添加spu类目协议<br/>http://adm.yunshuxie.com/api/spu/save.htm<br/>{"type":112,"title":"类目测试商品",<br/>"imgUrls":"https://oss-ysx-pic.yunshuxie.com/agent_c/2019/03/12/19/1552388927736.jpg",<br/>"sellerPoint":"类目测试"","shareInfo":"类目测试","coupon":0,"introduceImgs":"类目测试使用","pcImgs":"类目测试","introduce":"类目测试"}
                """
            url = r"http://adm.yunshuxie.com" + "/api/spu/save.htm"
            params = {"type": productId, "title": "类目测试商品-title-%s" % (self.timestamp),
                          "imgUrls": "https://oss-ysx-pic.yunshuxie.com/agent_c/2019/03/12/19/1552388927736.jpg",
                          "sellerPoint": "类目测试-sellerPoint-%s" % (self.timestamp),
                          "shareInfo": "类目测试-shareInfo-%s" % (self.timestamp), "coupon": 0,
                          "introduceImgs": "类目测试使用-introduceImgs-%s" % (self.timestamp),
                          "pcImgs": "类目测试", "introduce": "类目测试%s" % (self.timestamp),"telPhone":"60000007001"}
            logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False,encoding="utf8") + fengefu)
            str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
            print str_params
            self.resp = self.session.post(url=url, data=params)
            print self.resp.text
            result = json.loads(self.resp.text, encoding="utf8")
            logging.info(url + lianjiefu + self.resp.content + fengefu)
            expect = {"code": "0"}
            if result["code"] == "0" or result["code"] == 0:
                assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],
                                                                             Really=result["code"])
            else:
                assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],
                                                                             Really=result["code"])

        add_spu_save() #创建spu
        url = r"http://adm.yunshuxie.com" + "/api/productType/update.htm"
        params = {"id": productId, "title": "类目测试"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False,encoding="utf8") + fengefu)
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
        """删除类目类目协议-商品已关联<br/>http://adm.yunshuxie.com/api/productType/delete.htm<br/>{"id": }
        """
        productId = self.redis.str_get("productId")
        url = r"http://adm.yunshuxie.com" + "/api/productType/delete.htm"
        params = {"id": productId}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False,encoding="utf8") + fengefu)
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