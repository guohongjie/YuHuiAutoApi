#!/usr/bin/python
#-*-coding:utf-8
from getCookies import get_ysx_crm_cookie
import time
import requests
import json
import re
import datetime
def coupon_test(env_flag,env_num,couponPrice,phone):
    """
    :param couponPrice:   单个代金券价格
    :param phone:   领取手机号码
    :return: log
    """
    resp_log = {}
    session = requests.Session()
    resp_cookies = get_ysx_crm_cookie(env_flag,env_num)
    if resp_cookies["code"]!=200:
        raise Exception,"登录失败,请检查登录配置"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01", "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "keep-alive", "Upgrade-Insecure-Requests": "1"}
    session.headers = header
    session.cookies = resp_cookies["cookies"]
    request_retry = requests.adapters.HTTPAdapter(max_retries=3)
    session.mount("https://", request_retry)
    session.mount("http://", request_retry)
    start_date = "{ymd} 00:00:00".format(ymd=datetime.datetime.now().strftime("%Y-%m-%d"))
    end_date = "{ymd} 23:59:59".format(ymd=(datetime.datetime.now() + datetime.timedelta(days=10)).strftime("%Y-%m-%d"))
    url = r"https://admin.crm.yunshuxie.com/v1/crm/coupon_activity/edit"
    name = "测试_自动化测试_%d"%(time.time())
    params = {"couponActivityName": name,
              "couponInstructions": "测试_自动化测试创建_%s"%(name),
              "couponTotalAmount": "%.2f"%(float(couponPrice)*4),
              "couponSingleAmount": "{}".format(couponPrice),
              "couponDailyLimit": "4",
              "limitPersonReceive": "4",
              "activityStartDate": start_date,
              "activityEndDate": end_date,
              "couponType":"1","limitAmount":"","effectiveType": "2",
              "validityDays": "","validatyEndDate": end_date,
              "validatyStartDate": start_date,
              "courseApplyType": "1","courseApply": "-1",
              "sendMode": "2","activityStatus": "","couponActivityId":""}
    #print params
    resp = session.post(url=url,data=params)
    resp_log[u"创建代金券"] = resp.text
    #print "创建代金券:",resp.text
    result = json.loads(re.findall("{.*}", resp.text)[0], encoding="utf8")
    assert result["returnCode"]==0 or result["returnCode"]=="0","创建代金券:{msg}".format(msg=result["returnMsg"])
    url = r"https://admin.crm.yunshuxie.com/v1/crm/coupon_activity/test_list" # 查询代金券 couponActivityId
    params = {"couponActivityName":name,"couponActivityNumber":"","activityStatus":"1","sort":"couponActivityId","order":"DESC","limit":"10","offset":"0"}
    resp = session.get(url=url, params=params)
    resp_log[u"查询代金券"] = resp.text
    #print resp.text
    result = json.loads(re.findall("{.*}", resp.text)[0], encoding="utf8")
    couponActivityId = result["rows"][0]["couponActivityId"]
    couponActivityNumber = result["rows"][0]["couponActivityNumber"]
    url = r"https://admin.crm.yunshuxie.com/v1/crm/coupon_activity/edit"  #审核代金券
    params = {"couponActivityId": couponActivityId,"activityStatus": "3"}
    resp = session.post(url=url, data=params)
    resp_log[u"审核代金券"] = resp.text
    #print "审核代金券:",resp.text
    result = json.loads(re.findall("{.*}", resp.text)[0], encoding="utf8")
    assert result["returnCode"]==0 or result["returnCode"]=="0","审核代金券:{msg}".format(msg=result["returnMsg"])
    url = r"https://pay.yunshuxie.com/v1/coupon/post.htm"
    params = {"shareKey": "","actNum": couponActivityNumber,"phone": phone,"code": ""}
    dict_coupins = {}
    coupins = []
    header = {"Accept": "application/json, text/javascript, */*; q=0.01",
              "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
              "Origin": "http://pay.yunshuxie.com",
              "Referer": "http://pay.yunshuxie.com/coupon/coupon_test.html?shareKey=null&actNum=20190306KLHJA&clientType=1",
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
    for i in range(1,4):
        resp = requests.post(url=url,data=params,headers=header,cookies={"env_flag":env_flag,"env_num":env_num})
        resp_log[u"领取代金券-第%d次"%(i)] = resp.text
        #print "领取代金券:",resp.text
        result = json.loads(re.findall("{.*}", resp.text)[0], encoding="utf8")
        assert result["returnCode"] == 48 or result["returnCode"] == "48", "领取代金券:{msg}".format(msg=result["returnMsg"])
        coupins.append(result["data"]["couponId"])
    dict_coupins[u"代金券有效期"] = {"start":start_date,"end":end_date}
    dict_coupins[u"代金券编号"] = couponActivityNumber
    dict_coupins["couponId"] = coupins
    resp_log["coupins_desc"] = dict_coupins
    return resp_log

if __name__ == "__main__":
    print coupon_test(env_flag="beta",env_num="1",couponPrice="20",phone="18519118952")