#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
import hashlib
import urllib
def sendMsg(msg,phones):
    url = r"https://api.yunshuxie.com/yunshuxie-message-service/sms/send_batch_message"
    params = {"contentType": "1", "content": msg,
              "phones": "{phone1}".format(phone1=",".join(phones)), "platform": "0",
              "idiograph ": "云舒写"}  # "云舒写"}#,"msgTemplate":"","msgVars":""}
    print params
    string = urllib.urlencode(params)
    salt = "mengmengda"
    s = string + salt
    md = hashlib.md5()
    md.update(s)
    md5 = md.hexdigest()
    data = string + "&sign=" + md5
    header = {"Connection": "keep-alive", "Content-Type": "application/x-www-form-urlencoded",
              "Cache-Control": "no-cache",
              "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 Safari/601.1 wechatdevtools/1.02.1904090 MicroMessenger/6.7.3 Language/zh_CN webview/15578306374265793 webdebugger port/22562"}
    resp = requests.post(url, headers=header, data=data)
    print resp.content
if __name__ == "__main__":
    sendMsg("wctv",phones=["18519118952"])