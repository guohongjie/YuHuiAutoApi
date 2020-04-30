#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import unittest
import json
# import sys
# sys.path.append("../../base")
from app.base.pythonProject.base.log import TestLog,fengefu,lianjiefu
from app.base.pythonProject.base.py_redis import MyRedis
from app.base.pythonProject.base.getCookies import get_ysx_crm_cookie
logging = TestLog().getlog()
class Ysx_Crm_CXSHDD(unittest.TestCase):
    """CRM 查询商户订单"""
    @classmethod
    def setUpClass(self):
        redis = MyRedis()
        env_flag = redis.str_get("ysx_crm_env_flag")
        env_num = redis.str_get("ysx_crm_env_num")
        self.session = requests.Session()
        cookies = get_ysx_crm_cookie(env_flag,env_num)
        header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36","Accept": "application/json, text/javascript, */*; q=0.01","Accept-Encoding": "gzip, deflate, br","Accept-Language": "zh-CN,zh;q=0.9","Connection": "keep-alive","Upgrade-Insecure-Requests": "1"}
        self.msg = """\n        Expect:  {Expect}-*-\n        Really:  {Really}"""  # 校验HTTP返回代码
        self.session.headers = header
        self.session.cookies = cookies
    def test_01_merchants_order(self):
        """查询商户订单<br/>http://admin.crm.yunshuxie.com/v1/admin/order/query/merchants/order<br/>{"orderSn": "Y1760155867978891781"}
        """
        url = r"http://admin.crm.yunshuxie.com/v1/admin/order/query/merchants/order"
        params = {"orderSn": "Y1760155867978891781"}
        logging.info(url + lianjiefu + json.dumps(params,ensure_ascii=False) + fengefu)
        str_params = json.dumps(params, ensure_ascii=False, encoding="utf8")
        print str_params
        self.resp = self.session.post(url=url,data=params)
        print self.resp.content
        result = json.loads(self.resp.content,encoding="utf8")
        logging.info(url + lianjiefu + self.resp.text + fengefu)
        expect = {"tradeStatus":"SUCCESS"}
        assert result["tradeStatus"]==expect["tradeStatus"],self.msg.format(Expect=expect["tradeStatus"],Really=result["tradeStatus"])
    @classmethod
    def tearDownClass(self):
        pass

if __name__ == "__main__":
    unittest.main()