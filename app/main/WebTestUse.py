#!/usr/bin/python
#-*-coding:utf-8 -*-
from app.main import test
from flask import request,Response,make_response,jsonify
from app.base.pythonProject.base.CreateLivingRoom import CreateBJYRoom
import json
import pickle
from app.config.config import SystemConfig
from app.config.sql import SelectData
from app.config.public_function import saveOrUpdate_live_product_chapter
import requests
from app.base.pythonProject.base.getCookies import get_ysx_crm_cookie
import time
from app import redis
from app.config.sql import betaDB,betaDB_order


@test.route("/getProductCourseHoursId",methods=["GET"])
def getProductCourseHours():
    """
    Admin创建ClassIn直播间专用
    获取ProductCourseHoursId
    :return:
    """
    productId = request.args.get("productId")
    env_flag = request.args.get("env_flag")
    selectProductCourseHoursIdSQL = """
            SELECT
            hou.PRODUCT_COURSE_HOURS_ID
        FROM
            YSX_PRODUCT_INFO AS ypi,
            ysx_product_course_hours AS hou
        WHERE
            ypi.PRODUCT_ID = {PRODUCT_ID}
        AND ypi.SOURCE_ID = hou.PRODUCT_COURSE_ID
        AND ypi.FLOW_STATUS != - 1
    """.format(PRODUCT_ID=productId)
    if env_flag == "beta":
        host = SystemConfig.beta_mysql_host
        name = SystemConfig.beta_mysql_user
        pwd = SystemConfig.beta_mysql_pwd
        port = SystemConfig.beta_mysql_port
    else:
        host = SystemConfig.stage_prod_mysql_host
        name = SystemConfig.stage_prod_mysql_user
        pwd = SystemConfig.stage_prod_mysql_pwd
        port = SystemConfig.stage_prod_mysql_port
    databaseDB = SelectData(host=host, name=name, pwd=pwd, port=port,database="ysx_mooc")
    getProductCourseHoursId = databaseDB.execute_select(selectProductCourseHoursIdSQL)
    Response.headers = {"Content-Type": "application/json; charset=UTF-8"}
    if getProductCourseHoursId:
        resp = '{"productCourseHoursId":"%s"}'%getProductCourseHoursId[0][0]
        return Response(response=resp,status=200)
    else:
        resp = '{"productCourseHoursId":"%s"}'  %'未查询数据'
        return Response(response=resp, status=400)

@test.route("/saveOrUpdate_live_product_chapter",methods=["GET"])
def saveOrUpdateLiveProductChapter():
    """
    Admin创建ClassIn直播间专用-
    :return:
    """
    env_flag =request.args.get("env_flag")
    env_num =request.args.get("env_num")
    productCourseId = request.args.get("productCourseId")    #107564
    resp = saveOrUpdate_live_product_chapter(env_flag=env_flag,env_num=env_num,productCourseId=productCourseId)
    if resp.status_code == 200:
        return resp.text
    else:
        return {"code":400,"msg":"创建失败,业务HTTP代码非200"}

@test.route("/editBJYRoom",methods=["GET"])
def editBJYRoom():
    """
    Admin创建百家云直播间专用-
    :return:
    """
    env_flag =request.args.get("env_flag")
    env_num =request.args.get("env_num")
    phone = request.args.get("phone")
    isWebRtc = request.args.get("WebRTC")
    resp = CreateBJYRoom(env_flag=env_flag, env_num=env_num, phone=phone, isWebRtc=isWebRtc)
    if resp.status_code == 200:
        return Response(response=resp, status=200)
    return Response(response=resp, status=400)

@test.route("/test_fill_order",methods=["GET"])
def test_file_order():
    """
    绩效专用
    接口生成补单
    """
    phone = request.args.get("phone")
    productId = request.args.get("pId")
    phId = request.args.get("phId")
    product_url = "https://admin.crm.yunshuxie.com/v1/admin/order/query/product_list?productId={productId}&productName=&sort=productId&order=asc&limit=100&offset=0".format(productId=productId)
    cookies = get_ysx_crm_cookie(env_flag="beta",env_num="1",
                                 account_username="guohongjie@yunshuxie.com",account_passwd="ysx2019")["cookies"]
    resp = requests.get(url=product_url,cookies=cookies)
    productSelect = json.loads(resp.text,encoding="utf-8")
    if productSelect["rows"]:
        for productDict in productSelect["rows"]:
            if int(phId)==productDict["productCourseHoursId"] and int(productId)==productDict["productId"]:
                searchProduct = productDict
                fill_order_params = {"contactPhone": phone, "orderAmount": searchProduct["productPrice"],
                        "productName": searchProduct["productName"],
                        "productId": searchProduct["productId"], "productType": searchProduct["productType"],
                        "courseHoursTitles": searchProduct["courseHoursTitle"],
                        "productCourseHoursId": searchProduct["productCourseHoursId"], "grade": searchProduct["grade"],
                        "originalAmount": searchProduct["productPrice"], "callbackTime": "2019-10-01 00:00:00",
                        "payAccount": "1", "orderSource": "微信", "shareKeyFirst": "-1",
                        "shareKeySecond": "-1","shareKey": "-1", "fromOpenId": "CCrm_653", "chargeTeacher": "赵红玲",
                        "chargeTeacher1": "CCrm_653", "outerTradeId": "osxBJ6MQ69yOMyhCejqj55SdKzyI",
                        "file": file("/home/guohj/Pictures/Operating_System_Apple_Mac_72px_1072593_easyicon.net.png","rb"),
                        "fillOrderDesc": "测试"}

                fill_order_url = "https://admin.crm.yunshuxie.com/fill/order"
                resp = requests.post(url=fill_order_url,data=fill_order_params,cookies=cookies)
                print resp.text

    return make_response(jsonify(resp.text))
@test.route("/test_protected",methods=["GET"])
def test_protected():
    """
    绩效专用
    30保护期校验
    """
    tiyan_order_sn = request.args.get("tiyan_order_sn")
    zhengshi_order_sn = request.args.get("zhengshi_order_sn")
    isProtected = request.args.get("isProjected")
    courser_day = """SELECT ymypch.COURSE_START_DATE AS courseStartDate FROM ysx_order.YSX_ORDER_INFO yoyoi INNER JOIN ysx_mooc.ysx_mooc_class_member ymymcm ON ymymcm.ORDER_ID = yoyoi.ORDER_ID 
                 INNER JOIN ysx_mooc.ysx_mooc_class ymymc ON ymymc.MOOC_CLASS_ID = ymymcm.MOOC_CLASS_ID 
                 INNER JOIN ysx_mooc.ysx_product_course_hours ymypch ON ymypch.PRODUCT_COURSE_HOURS_ID = ymymc.PRODUCT_COURSE_HOURS_ID
                 INNER JOIN ysx_order.ysx_wechat_service_teacher_class_middle yoywstcm ON yoywstcm.MOOC_CLASS_ID = ymymc.mooc_class_id 
                 INNER JOIN ysx_order.ysx_wechat_service_teacher yoywst ON yoywst.WECHATER_TEACHER_ID = yoywstcm.wechat_service_teacher_id 
                 WHERE yoyoi.order_sn = "{tiyan_order_sn}" ;""".format(
        tiyan_order_sn=tiyan_order_sn)
    select_datas = betaDB_order()
    COURSE_START_DATE = select_datas.execute_select(courser_day)[0][0]
    if isProtected =="0":    #需要保护期外数据
        sql = """select timestampdiff(day,
    (SELECT ymypch.COURSE_START_DATE AS courseStartDate FROM ysx_order.YSX_ORDER_INFO yoyoi INNER JOIN ysx_mooc.ysx_mooc_class_member ymymcm ON ymymcm.ORDER_ID = yoyoi.ORDER_ID 
     INNER JOIN ysx_mooc.ysx_mooc_class ymymc ON ymymc.MOOC_CLASS_ID = ymymcm.MOOC_CLASS_ID 
     INNER JOIN ysx_mooc.ysx_product_course_hours ymypch ON ymypch.PRODUCT_COURSE_HOURS_ID = ymymc.PRODUCT_COURSE_HOURS_ID
     INNER JOIN ysx_order.ysx_wechat_service_teacher_class_middle yoywstcm ON yoywstcm.MOOC_CLASS_ID = ymymc.mooc_class_id 
     INNER JOIN ysx_order.ysx_wechat_service_teacher yoywst ON yoywst.WECHATER_TEACHER_ID = yoywstcm.wechat_service_teacher_id 
     WHERE yoyoi.order_sn = "{tiyan_order_sn}")/*体验课程开始时间*/,
    (select a.CALLBACK_TIME from ysx_order.ysx_order_info a where a.order_sn='{zhengshi_order_sn}' and a.ORDER_STATE='2')/*正式课程下单时间*/
    )""".format(tiyan_order_sn=tiyan_order_sn,zhengshi_order_sn=zhengshi_order_sn)
        data = select_datas.execute_select(sql)[0][0]
        if data>30:
            min_data_sql = """select callback_time from ysx_order.YSX_ORDER_INFO where order_sn="{zhengshi_order_sn}" and order_state="2";""".format(zhengshi_order_sn=zhengshi_order_sn)
            min_data = select_datas.execute_select(min_data_sql)[0][0]
            datas = "%s:保护期外,不做处理"%(min_data)
        else:
            add_30_days = """
            select date_add(
    (SELECT ymypch.COURSE_START_DATE AS courseStartDate FROM ysx_order.YSX_ORDER_INFO yoyoi INNER JOIN ysx_mooc.ysx_mooc_class_member ymymcm ON ymymcm.ORDER_ID = yoyoi.ORDER_ID 
     INNER JOIN ysx_mooc.ysx_mooc_class ymymc ON ymymc.MOOC_CLASS_ID = ymymcm.MOOC_CLASS_ID 
     INNER JOIN ysx_mooc.ysx_product_course_hours ymypch ON ymypch.PRODUCT_COURSE_HOURS_ID = ymymc.PRODUCT_COURSE_HOURS_ID
     INNER JOIN ysx_order.ysx_wechat_service_teacher_class_middle yoywstcm ON yoywstcm.MOOC_CLASS_ID = ymymc.mooc_class_id 
     INNER JOIN ysx_order.ysx_wechat_service_teacher yoywst ON yoywst.WECHATER_TEACHER_ID = yoywstcm.wechat_service_teacher_id 
     WHERE yoyoi.order_sn = "{tiyan_order_sn}" ),interval 31 day) from dual;""".format(tiyan_order_sn=tiyan_order_sn)
            data = select_datas.execute_select(add_30_days)[0][0]
            update_sql = """update ysx_order.ysx_order_info a set a.callback_time='{tdate}' where
      a.order_sn='{zhengshi_order_sn}' and a.ORDER_STATE='2';""".format(tdate=data,zhengshi_order_sn=zhengshi_order_sn)
            update_data = betaDB()
            update_data.execute_sql(update_sql)
            update_data.execute_close()
            datas="%s:保护期外+30天完成增加"%(data)
    else:    #需要保护期内数据
        sql = """select timestampdiff(day,
            (SELECT ymypch.COURSE_START_DATE AS courseStartDate FROM ysx_order.YSX_ORDER_INFO yoyoi INNER JOIN ysx_mooc.ysx_mooc_class_member ymymcm ON ymymcm.ORDER_ID = yoyoi.ORDER_ID 
             INNER JOIN ysx_mooc.ysx_mooc_class ymymc ON ymymc.MOOC_CLASS_ID = ymymcm.MOOC_CLASS_ID 
             INNER JOIN ysx_mooc.ysx_product_course_hours ymypch ON ymypch.PRODUCT_COURSE_HOURS_ID = ymymc.PRODUCT_COURSE_HOURS_ID
             INNER JOIN ysx_order.ysx_wechat_service_teacher_class_middle yoywstcm ON yoywstcm.MOOC_CLASS_ID = ymymc.mooc_class_id 
             INNER JOIN ysx_order.ysx_wechat_service_teacher yoywst ON yoywst.WECHATER_TEACHER_ID = yoywstcm.wechat_service_teacher_id 
             WHERE yoyoi.order_sn = "{tiyan_order_sn}")/*体验课程开始时间*/,
            (select a.CALLBACK_TIME from ysx_order.ysx_order_info a where a.order_sn='{zhengshi_order_sn}' and a.ORDER_STATE='2')/*正式课程下单时间*/
            )""".format(tiyan_order_sn=tiyan_order_sn, zhengshi_order_sn=zhengshi_order_sn)
        data = select_datas.execute_select(sql)
        if data < 30:
            min_data_sql = """select callback_time from ysx_order.YSX_ORDER_INFO where order_sn="{zhengshi_order_sn}" and order_state="2";""".format(
                zhengshi_order_sn=zhengshi_order_sn)
            min_data = select_datas.execute_select(min_data_sql)[0][0]
            datas = "%s:保护期内,不做处理" % (min_data)
        else:
            add_29_days = """
                    select date_add(
            (SELECT ymypch.COURSE_START_DATE AS courseStartDate FROM ysx_order.YSX_ORDER_INFO yoyoi INNER JOIN ysx_mooc.ysx_mooc_class_member ymymcm ON ymymcm.ORDER_ID = yoyoi.ORDER_ID 
             INNER JOIN ysx_mooc.ysx_mooc_class ymymc ON ymymc.MOOC_CLASS_ID = ymymcm.MOOC_CLASS_ID 
             INNER JOIN ysx_mooc.ysx_product_course_hours ymypch ON ymypch.PRODUCT_COURSE_HOURS_ID = ymymc.PRODUCT_COURSE_HOURS_ID
             INNER JOIN ysx_order.ysx_wechat_service_teacher_class_middle yoywstcm ON yoywstcm.MOOC_CLASS_ID = ymymc.mooc_class_id 
             INNER JOIN ysx_order.ysx_wechat_service_teacher yoywst ON yoywst.WECHATER_TEACHER_ID = yoywstcm.wechat_service_teacher_id 
             WHERE yoyoi.order_sn = "{tiyan_order_sn}" ),interval 29 day) from dual;""".format(
                tiyan_order_sn=tiyan_order_sn)
            COURSE_START_DATE =select_datas.execute_select(courser_day)[0][0]
            data = select_datas.execute_select(add_29_days)[0][0]
            update_sql = """update ysx_order.ysx_order_info a set a.callback_time='{tdate}' where
              a.order_sn='{zhengshi_order_sn}' and a.ORDER_STATE='2';""".format(tdate=data,
                                                                                zhengshi_order_sn=zhengshi_order_sn)
            update_data = betaDB()
            update_data.execute_sql(update_sql)
            update_data.execute_close()
            datas = "%s:保护期内+课程开课事件增加29天完成"%(data)
    select_datas.execute_close()
    response = make_response(jsonify({"code": 200,"COURSE_START_DATE":str(COURSE_START_DATE) ,"CALLBACK_TIME": datas}))  # 返回response
    return response

@test.route("/getMemberIdJson",methods=["POST"])
def getMemberIdJson():
    startPhone = request.form['startPhone'].strip()
    endPhone = request.form['endPhone'].strip()
    # respMsg = adminAuthorizeCourse("beta","10",int(startPhone),int(endPhone))
    msg = {"code": 0,
           "data": {},
           "msg": "返回成功",
           "ts": "%d=" % time.time()
           }
    userJsonList = []
    with open("./app/config/memberIdUsers.pickle",'r') as f:
        datas = pickle.load(f)
        for phone in range(int(startPhone),int(endPhone)):
            memberId = datas[phone]
            userJson = makeJson(phone,memberId)
            userJsonList.append(userJson)
    total = len(userJsonList)
    msg['data']['total'] = total
    msg['data']['room_user_info'] = userJsonList
    return make_response(jsonify(msg))
def adminAuthorizeCourse(env_flag,env_num,startUser,endUser):
    cookies = requests.cookies.RequestsCookieJar()  # 生成cookies 容器
    cookies.set('env_flag', env_flag)  # 设置测试环境
    cookies.set("env_num", env_num)  # 设置环境号
    adminLoginUrl = r"https://admin.yunshuxie.com/common_index/loginIn.json"    #admin登录接口
    adminSearchUserInfoUrl = r"https://admin.yunshuxie.com/v1/admin/account/query/user_list.json"    #查询用户信息接口
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}
    loginParams = {"userName": "automation@yunshuxie.com", "pwd": "ysx2019",
                   "emailVerifyCode": "ysx2019"}    #登录接口固定参数
    adminUserInfoParams = {"memberId":"","sort":"memberId","order":"asc","limit":"20","offset":"0",
                           "phone":""}    #用户查询接口 phone 可变参数
    adminLoginResp = requests.post(url=adminLoginUrl, headers=headers,
                                   data=loginParams, cookies=cookies)  # admin登录获取cookies
    msg = {"code": 0,
           "data": {},
           "msg": "返回成功",
           "ts": "%d" % time.time()
           }
    if json.loads(adminLoginResp.content)["returnCode"] == "0":
        loginMsg = "登录成功"
        cookies.update(adminLoginResp.cookies)    #更新cookies
        room_user_info = []
        for phone in range(startUser, endUser):
            adminUserInfoParams["phone"]=str(phone)
            userInfoResp = requests.get(url=adminSearchUserInfoUrl, headers=headers,
                                              params=adminUserInfoParams, cookies=cookies)
            memberId = json.loads(userInfoResp.content)["rows"][0]["memberId"]
            user_json = makeJson(phone,memberId)
            room_user_info.append(user_json)
        total = len(room_user_info)
        msg["data"]["total"] = total
        msg["data"]["room_user_info"] = room_user_info
        return msg
    else:
        return msg
def makeJson(phone,memberId):
    userJson = {
        "date": time.strftime("%Y-%m-%d", time.localtime()),
        "user_number": memberId,
        "user_name": "测试_"+str(phone),
        "user_role": "0",
        "first_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "last_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "first_heartbeat_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "last_heartbeat_time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "actual_listen_time": "0",
        "user_ip": "172.0.0.1",
        "network_operator": "联通",
        "client_type": "1",
        "area": "北京",
        "city": "北京",
        "group": "2"
    }
    return userJson
@test.route("/ClassInCreate",methods=["GET"])
def ClassInCreate():
    env_flag = request.args.get("env_flag")
    env_num = request.args.get("env_num")
    phone = request.args.get("phone")
    developer =request.args.get("developer")
    redis.set("ClassInCreate", "{'phone':'%s'}"%phone, 600)
    redis.set("ClassInCreateFlag", "{'env_flag':'%s'}"%env_flag, 600)
    redis.set("ClassInCreateNum", "{'env_num':'%s'}"%env_num, 600)
    url = "http://uwsgi.sys.bandubanxie.com/scheduleSuite?domain=ClassIn&env_flag=%s&env_num=%s&developer=%s"%(env_flag,env_num,developer)
    wctv = {}
    resp = requests.get(url=url)
    time.sleep(10)
    value = redis.get("v1/admin/product_chapter/create_live_room.json")
    wctv["schedule"] = resp.text
    wctv["RoomMsg"] = value
    return make_response(jsonify(wctv))
@test.route("/BJYCreate",methods=["GET"])
def BJYCreate():
    env_flag = request.args.get("env_flag")
    env_num = request.args.get("env_num")
    phone = request.args.get("phone")
    developer =request.args.get("developer")
    WebRTC = request.args.get("WebRTC")
    redis.set("editBJYRoom", "{'phone':'%s'}"%phone, 600)
    redis.set("editBJYRoomFlag", "{'env_flag':'%s'}"%env_flag, 600)
    redis.set("editBJYRoomNum", "{'env_num':'%s'}"%env_num, 600)
    # url = "http://127.0.0.1:5000/scheduleSuite?domain=ClassIn&env_flag=%s&env_num=%s&developer=%s&WebRTC=%s"%(env_flag,env_num,developer,WebRTC)
    url = "http://uwsgi.sys.bandubanxie.com/scheduleSuite?domain=BJY&env_flag=%s&env_num=%s&developer=%s&WebRTC=%s"%(env_flag,env_num,developer,WebRTC)
    wctv = {}
    resp = requests.get(url=url)
    time.sleep(10)
    wctv["schedule"] = resp.text
    return make_response(jsonify(wctv))