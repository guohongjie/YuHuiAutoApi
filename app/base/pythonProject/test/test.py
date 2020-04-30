#!/usr/bin/python
# -*-coding:utf-8-*-
__author__ = "guohongjie"
import requests
import base64
from PIL import Image
import json
def get_crm_cookie(env_flag,env_num):
    """登录crm,并返回cookies
    :param url 请求连接
    :param header 请求头
    :return cookies"""
    url = r"http://admin.crm.yunshuxie.com/captcha.jpg"
    captcha_header = {"Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
                      "Accept-Encoding":"gzip, deflate, br",
                      "Cache-Control": "no-cache","Pragma": "no-cache",
                      "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                      "Referer": "https://admin.crm.yunshuxie.com/login.html",
                      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",}
    cookies = requests.cookies.RequestsCookieJar()  # 生成cookies 容器
    cookies.set('env_flag', env_flag)  #设置测试环境
    cookies.set("env_num",env_num)  #设置环境号
    #cookies.set("ngxUid","8bf5aceda7a0eb92f18e6ba8a3e34613")
    params = {"t": "1557893463045"}
    resp = requests.get(url,headers=captcha_header,params=params,cookies=cookies)  # 生成验证码
    cookies.update(resp.cookies)  # 更新cookies 容器
    with open("captcha.jpg","wb") as f:  # 存储图片
        f.write(resp.content)
    img = Image.open("captcha.jpg")  # 打开图片
    img = img.crop((44,10,175,45))  # 剪裁图片，提高识别率
    img.save("captcha.jpg")  # 保存图片
    with open("captcha.jpg","rb") as f:  # 打开图片
        base64_img = base64.b64encode(f.read())  # 转换成base64格式图片
        data = {"image_base64":base64_img,
            "app_id":"491861472"}
        url = r"https://nmd-ai.juxinli.com/ocr_captcha"
        captcha_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
                              "Content-Type":"application/json"}
        captcha_resp = requests.post(url=url,headers=captcha_header,json=data)  # 获取验证码
        captcha = json.loads(captcha_resp.content,encoding="utf8")["string"].lower()  # 最小化
    url = r"http://admin.crm.yunshuxie.com/sys/login"
    params = {"username": "admin","password": "Yunshuxie916@1ppt","captcha": captcha}  # 登录接口
    header = {"Accept": "application/json, text/javascript, */*; q=0.0",
              "Cache-Control": "no-cache",
              "Connection": "keep-alive",
              "Origin": "https://admin.crm.yunshuxie.com",
              "Pragma": "no-cache",
              "Content-Type": "application/x-www-form-urlencoded",
              "Host": "admin.crm.yunshuxie.com",
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
              "X-Requested-With": "XMLHttpRequest"}
    resp = requests.post(url,headers=header,data=params,cookies=cookies)
    cookies.update(resp.cookies)
    result = json.loads(resp.content,encoding="utf8")
    if result["code"] == 0:  # 判断登录是否成功
        return cookies
    else:
        return(get_crm_cookie(env_flag,env_num))  # 递归



crm_cookie = get_crm_cookie(env_flag="stage",env_num="1")
url = r"https://admin.crm.yunshuxie.com/admin/writing_material/query/writing_material_order.json"
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
params = {
"sort": "nowDate",
"order": "asc",
"limit": "32",
"offset": "0",
"_": "1557902593873"}
resp = requests.get(url,headers=header,params=params,cookies=crm_cookie)
if __name__ == "__main__":
    print resp.content
