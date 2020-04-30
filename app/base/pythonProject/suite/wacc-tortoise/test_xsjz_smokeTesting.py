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
class Smoke_Testing(unittest.TestCase):
    """销售简章-添加类目相关协议-添加SPU-添加SKU"""
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
    def test_00_productType_getTreeList(self):
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
    def test_01_productType_save(self):
        """添加类目接口协议<br/>http://adm.yunshuxie.com/api/productType/save.htm<br/>{"pTitle":"冒烟自动化测试-pTitle-","pId":"","childTitle":"冒烟自动化测试-childTitle-"}
        """
        url = r"http://adm.yunshuxie.com"+"/api/productType/save.htm"
        params = {"pTitle":"冒烟自动化测试-pTitle-{timestamp}".format(timestamp=self.timestamp),
                  "pId":"","childTitle":"冒烟自动化测试-childTitle-{timestamp}".format(timestamp=self.timestamp)}
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
    def test_02_productType_getList(self):
        """获取单条类目首级节点对应信息接口协议<br/>title=<br/>http://adm.yunshuxie.com/api/productType/getList.htm<br/>{"pageIndex":1,"pageSize":2,"title":}
        """
        pTitle = self.redis.str_get("pTitle")
        url = r"http://adm.yunshuxie.com"+"/api/productType/getList.htm"
        params = {"pageIndex":0,"pageSize":2,"title":pTitle}
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
        self.redis.str_set("product_id",result["data"]["list"][0]["id"])
    def test_03_productType_getRow(self):
        """获取单条类目首级节点对应信息接口协议<br/>http://adm.yunshuxie.com/api/productType/getRow.htm<br/>{"id":}
        """
        productId = self.redis.str_get("product_id")
        url = r"http://adm.yunshuxie.com"+"/api/productType/getRow.htm"
        params = {"id":productId}
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
    def test_04_productType_update(self):
        """获取单条类目首级节点对应信息接口协议<br/>http://adm.yunshuxie.com/api/productType/update.htm<br/>{"id":,"title":}
        """
        productId = self.redis.str_get("product_id")
        pTitle = self.redis.str_get("pTitle")
        url = r"http://adm.yunshuxie.com"+"/api/productType/update.htm"
        params = {"id":productId,"title":pTitle}
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
    def test_05_spu_save(self):
        """添加spu接口协议<br/>http://adm.yunshuxie.com/api/spu/save.htm<br/>{"type":,"title":"冒烟自动化测试",<br/>"imgUrls":"https://oss-ysx-pic.yunshuxie.com/agent_c/2019/03/12/19/1552388927736.jpg",<br/>"sellerPoint":"冒烟自动化测试"","shareInfo":"冒烟自动化测试","coupon":0,"introduceImgs":"冒烟自动化测试","pcImgs":"冒烟自动化测试","introduce":"冒烟自动化测试"}
        """
        productId = self.redis.str_get("product_id")
        url = r"http://adm.yunshuxie.com" + "/api/spu/save.htm"  #暂时使用Mock 数据
        #url = r"http://uwsgi.sys.bandubanxie.com/mock" + "/api/spu/save.htm"
        params = {"type": productId, "title": "冒烟自动化测试商品-title-%s" % (self.timestamp),
                  "imgUrls": "https://oss-ysx-pic.yunshuxie.com/agent_c/2019/03/12/19/1552388927736.jpg",
                  "sellerPoint": "冒烟自动化测试-sellerPoint-%s" % (self.timestamp),
                  "shareInfo": "冒烟自动化测试-shareInfo-%s" % (self.timestamp),
                  "coupon": 0, "introduceImgs": "冒烟自动化测试-introduceImgs-%s" % (self.timestamp),
                  "pcImgs": "冒烟自动化测试", "introduce": "冒烟自动化测试%s" % (self.timestamp),"auditionIds":"1234","telPhone":"60000007001"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False,encoding="utf8") + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url, data=params)
        print self.resp.text
        result = json.loads(self.resp.text, encoding="utf8")
        logging.info(url + lianjiefu + self.resp.content + fengefu)
        expect = {"code": "0"}
        if result["code"] == "0" or result["code"] == 0:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"], Really=result["code"])
        else:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],
                                                                     Really=result["code"])
        self.redis.str_set("spu_title",params["title"])
    def test_06_spu_getList(self):
        """获取spu列表信息接口协议<br/>http://adm.yunshuxie.com/api/spu/getList.htm<br/>{"pageIndex":1,"pageSize":10,"title":""}
        """
        spu_title = self.redis.str_get("spu_title")
        url = r"http://adm.yunshuxie.com"+"/api/spu/getList.htm"
        #url = r"http://uwsgi.sys.bandubanxie.com/mock"+"/api/spu/getList.htm"
        params = {"pageIndex":0,"pageSize":10,"title":spu_title}
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
        self.redis.str_set("spu_id",result["data"]["list"][0]["id"])
    def test_07_spu_getRow(self):
        """获取单条spu信息接口协议<br/>http://adm.yunshuxie.com/api/spu/getRow.htm<br/>{"id":}"""
        url = r"http://adm.yunshuxie.com"+"/api/spu/getRow.htm"
        spu_id = self.redis.str_get("spu_id")
        params = {"id":spu_id}
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
    def test_08_spu_update(self):
        """更新spu接口协议<br/>http://adm.yunshuxie.com/api/spu/update.htm<br/>{"id":}
        """
        spu_id = self.redis.str_get("spu_id")
        url = r"http://adm.yunshuxie.com"+"/api/spu/update.htm"
        params = {"id":spu_id,"title":"冒烟自动化测试-title-%s"%self.timestamp,
                  "imgUrls":"https://oss-ysx-pic.yunshuxie.com/agent_c/2019/04/24/21/1556113834007.jpg",
                  "sellerPoint":"冒烟自动化测试-sellerPoint-%s"%self.timestamp,
                  "shareInfo":"冒烟自动化测试-shareInfo-%s"%self.timestamp,"coupon":1,
                  "introduceImgs":"https://oss-ysx-pic.yunshuxie.com/agent_c/2019/04/24/21/1556113834007.jpg",
                  "pcImgs":"https://oss-ysx-pic.yunshuxie.com/agent_c/2019/04/24/21/1556113834007.jpg",
                  "introduce":"冒烟自动化测试-introduce-%s"%self.timestamp,"telPhone":"60000007001"}
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
    def test_09_spu_updateStatus(self):
        """更新spu状态接口协议<br/>"""
        spu_id = self.redis.str_get("spu_id")
        url = r"http://adm.yunshuxie.com" + "/api/spu/updateStatus.htm"
        params = {"id":spu_id,"status":"1","onlineTime":"","offlineTime":""}
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
    def test_10_product_attribute_save(self):
        """添加规格接口协议<br/>http://adm.yunshuxie.com/api/product/attribute/save.htm<br/>{"title":"自动化测试","value":"自动化测试"}"""
        url = r"http://adm.yunshuxie.com" + "/api/product/attribute/save.htm"
        params = {"title":"自动化测试-规格-%s"%(self.timestamp),"value":"自动化测试-规格值-%s"%(self.timestamp)}
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
    def test_11_product_attribute_save(self):
        """添加规格接口协议<br/>http://adm.yunshuxie.com/api/product/attribute/save.htm<br/>{"title":"冒烟自动化测试","value":"冒烟自动化测试"}"""
        url = r"http://adm.yunshuxie.com" + "/api/product/attribute/save.htm"
        params = {"title":"冒烟自动化测试2-规格-%s"%(self.timestamp),"value":"冒烟自动化测试2-规格值-%s"%(self.timestamp)}
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
    def test_12_product_attribute_getList(self):
        """规格列表接口协议<br/>http://adm.yunshuxie.com/api/product/attribute/getList.htm<br/>{"pageIndex":"1", "pageSize":"10", "productTypeName":"自动化测试"}"""
        url = r"http://adm.yunshuxie.com" + "/api/product/attribute/getList.htm"
        params =  {"pageIndex":"1", "pageSize":"10", "productTypeName":"自动化测试-规格-%s"%(self.timestamp)}
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
        attribute = result["data"]["list"][0]["id"]
        self.redis.str_set("attribute_id",attribute)
        params = {"pageIndex": "1", "pageSize": "10", "productTypeName": "冒烟自动化测试2-规格-%s" % (self.timestamp)}
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
        attribute = result["data"]["list"][0]["id"]
        self.redis.str_set("attribute_smoke_id",attribute)
    def test_13_product_attribute_getRow(self):
        """规格列表接口协议<br/>http://adm.yunshuxie.com/api/product/attribute/getRow.htm<br/>{"title":"自动化测试","value":"自动化测试"}"""
        attribute_id = self.redis.str_get("attribute_id")
        url = r"http://adm.yunshuxie.com" + "/api/product/attribute/getRow.htm"
        params =  {"id":attribute_id}
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
        attribute = result["data"]["id"]
        self.redis.str_set("attribute_id",attribute)

    def test_14_product_attribute_saveAttr(self):
        """添加子规格值接口协议<br/>http://adm.yunshuxie.com/api/product/attribute/saveAttr.htm<br/>{"title":"子规格值","pId":""}"""
        attribute_id = self.redis.str_get("attribute_smoke_id")
        url = r"http://adm.yunshuxie.com" + "/api/product/attribute/saveAttr.htm"
        params = {"title":"冒烟测试-子规格值-%s"%(self.timestamp),"pId": attribute_id}
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
    def test_15_product_attribute_update(self):
        """修改规格信息接口协议<br/>http://adm.yunshuxie.com/api/product/attribute/update.htm<br/>{"title":"规格名称","pId":""}"""
        attribute_id = self.redis.str_get("attribute_id")
        url = r"http://adm.yunshuxie.com" + "/api/product/attribute/update.htm"
        params = {"title":"规格名称-%s"%(self.timestamp),"id": attribute_id}
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
    def test_16_sku_save(self):
        """添加sku接口协议<br/>http://adm.yunshuxie.com/api/sku/save.htm<br/>{"spuId":"","attributeIds":"123","marketPrice":"999",<br/>"shopPrice":"999","courseIds":"","stocks":""}"""
        spu_id = self.redis.str_get("spu_id")
        attribute_id = self.redis.str_get("attribute_id")
        url = r"http://adm.yunshuxie.com" + "/api/sku/save.htm"
        params = {"spuId":spu_id,"attributeIds":attribute_id,"marketPrice":"1","shopPrice":"1","courseIds":"1","stocks":"1"}
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
    def test_17_sku_update(self):
        """更新sku接口协议<br/>http://adm.yunshuxie.com/api/spu/getInfo.htm<br/>{"id":,"spuId":,"marketPrice":"9999999","shopPrice":"9999999","courseIds":"9999999"}"""
        spu_id = self.redis.str_get("spu_id")
        url = r"http://adm.yunshuxie.com" + "/api/spu/getInfo.htm"
        params = {"id":spu_id}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False, encoding="utf8") + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url, data=params)
        print self.resp.text
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        result = json.loads(self.resp.text, encoding="utf8")
        sku_id = result["data"]["childList"][0]["id"]
        self.redis.str_set("sku_id", sku_id)
        url = r"http://adm.yunshuxie.com" + "/api/sku/update.htm"
        params = {"id":sku_id,"spuId":spu_id,"marketPrice":"9999999","shopPrice":"9999999","courseIds":"9999999"}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False, encoding="utf8") + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url, data=params)
        print self.resp.text
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        result = json.loads(self.resp.text, encoding="utf8")
        expect = {"code": "0"}
        if result["code"] == "0" or result["code"] == 0:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"], Really=result["code"])
        else:
            assert result["code"] == expect["code"], self.msg.format(Expect=expect["code"],
                                                                     Really=result["code"])
    def test_18_stock_update(self):
        """sku库存增减接口协议-增库存<br/>http://adm.yunshuxie.com/api/sku/save.htm<br/>{"id":, "operateType":"1", "num":"2"}"""
        sku_id = self.redis.str_get("sku_id")
        url = r"http://adm.yunshuxie.com" + "/api/stock/update.htm"
        params = {"id":sku_id, "operateType":"1", "num":"2"}
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
    def test_19_stock_update(self):
        """sku库存增减接口协议-减库存<br/>http://adm.yunshuxie.com/api/sku/save.htm<br/>{"id": "operateType":"2", "num":"1"}"""
        sku_id = self.redis.str_get("sku_id")
        url = r"http://adm.yunshuxie.com" + "/api/stock/update.htm"
        params = {"id":sku_id, "operateType":"2", "num":"1"}
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
    def test_20_sku_updateStatus(self):
        """更新sku状态接口协议-下架<br/>http://adm.yunshuxie.com/api/sku/updateStatus.htm<br/>{"id":sku_id,"status":"0",<br/>"onlineTime":"2019-01-01 00:00:01","offlineTime":"2019-01-01 00:00:01"}"""
        sku_id = self.redis.str_get("sku_id")
        url = r"http://adm.yunshuxie.com" + "/api/sku/updateStatus.htm"
        params =  {"id":sku_id,"status":"0","onlineTime":"2019-01-01 00:00:01","offlineTime":"2019-01-01 00:00:01"}
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
    def test_21_sku_updateStatus(self):
        """更新sku状态接口协议-上架<br/>http://adm.yunshuxie.com/api/sku/updateStatus.htm<br/>{"id":sku_id,"status":"1",<br/>"onlineTime":"2019-01-01 00:00:01","offlineTime":"2019-01-01 00:00:01"}"""
        sku_id = self.redis.str_get("sku_id")
        url = r"http://adm.yunshuxie.com" + "/api/sku/updateStatus.htm"
        params =  {"id":sku_id,"status":"1","onlineTime":"2019-01-01 00:00:01","offlineTime":"2019-01-01 00:00:01"}
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

    def test_22_sku_updateStatus(self):
        """更新sku状态接口协议-自动上下架<br/>http://adm.yunshuxie.com/api/sku/updateStatus.htm<br/>{"id":sku_id,"status":"2",<br/>"onlineTime":"2019-01-01 00:00:01","offlineTime":"2019-12-31 00:00:01"}"""
        sku_id = self.redis.str_get("sku_id")
        url = r"http://adm.yunshuxie.com" + "/api/sku/updateStatus.htm"
        params = {"id": sku_id, "status": "2", "onlineTime": "2019-01-01 00:00:01",
                  "offlineTime": "2019-12-31 00:00:01"}
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
    def test_23_sku_saveList(self):
        """批量添加sku接口协议<br/>http://adm.yunshuxie.com/api/sku/saveList.htm<br/>{"skuList":[{"spuId":"%s","attributeIds":"222",<br/>"marketPrice":"222","shopPrice":"222","courseIds":"222","stocks":"222"},<br/>{"spuId":"%s","attributeIds":"333","marketPrice":"333",<br/>"shopPrice":"333","courseIds":"333","stocks":"333"}]}"""
        spu_id = self.redis.str_get("spu_id")
        attribute_id = self.redis.str_get("attribute_id")
        url = r"http://adm.yunshuxie.com" + "/api/sku/saveList.htm"
        params =  {"skuList":"""[{"spuId":"%s","attributeIds":"%s","marketPrice":"222","shopPrice":"222","courseIds":"222","stocks":"222"},{"spuId":"%s","attributeIds":"%s","marketPrice":"333","shopPrice":"333","courseIds":"333","stocks":"333"}]"""%(spu_id,attribute_id,spu_id,attribute_id)}
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

    def test_24_sku_updateStatus(self):
        """新sku状态接口协议-上架<br/>http://adm.yunshuxie.com/api/sku/updateStatus.htm<br/>"""
        spu_id = self.redis.str_get("spu_id")
        url = r"http://adm.yunshuxie.com" + "/api/spu/getInfo.htm"
        params = {"id": spu_id}
        logging.info(url + lianjiefu + json.dumps(params, ensure_ascii=False, encoding="utf8") + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url, data=params)
        print self.resp.text
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        result = json.loads(self.resp.text, encoding="utf8")
        sku_id = result["data"]["childList"][1]["id"]
        url = r"http://adm.yunshuxie.com" + "/api/sku/updateStatus.htm"
        params = {"id": sku_id, "status": "1", "onlineTime": "2019-07-01 00:00:01",
                  "offlineTime": "2019-12-31 00:00:01"}
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

    def test_25_sku_delete(self):
        """删除单条sku信息接口协议<br/>http://adm.yunshuxie.com/api/sku/delete.htm<br/>{"id": sku_id}"""
        sku_id = self.redis.str_get("sku_id")
        url = r"http://adm.yunshuxie.com" + "/api/sku/delete.htm"
        params = {"id": sku_id}
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
    def test_26_course_getList(self):
        """sku选择课程列表<br/>http://adm.yunshuxie.com/api/course/getList.htm<br/>{"title": "测试"}"""
        url = r"http://adm.yunshuxie.com" + "/api/course/getList.htm"
        params = {"title": "测试"}
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
    def test_27_course_getList(self):
        """删除规格接口协议<br/>http://adm.yunshuxie.com/api/product/attribute/delete.htm<br/>{"id":""}"""
        url = r"http://adm.yunshuxie.com" + "/api/product/attribute/delete.htm"
        attribute_id = self.redis.str_get("attribute_id")
        params = {"id": attribute_id}
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

    @classmethod
    def tearDownClass(self):
        pass
if __name__ == "__main__":
    unittest.main()