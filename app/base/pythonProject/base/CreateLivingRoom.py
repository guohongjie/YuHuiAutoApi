# coding=utf-8/gbk
import datetime
import json
import time
import requests
from requests import session
from getCookies import get_cookies
from requests_toolbelt import MultipartEncoder
def CreateBJYRoom(env_flag,env_num, phone, isWebRtc):
    """
    :param env_flag: beta/stage/prod
    :param env_num: 1-10
    :param isWebRtc: 0/1
    :return:
    """
    if env_flag == "beta":
        cookies = get_cookies(project="云舒写ADMIN后台管理系统", env_flag=env_flag,
                              env_num=env_num,
                              account_username="panze@yunshuxie.com",
                              account_passwd="test123456")
        time_stamp = time.time()
        local_time = time.localtime(time_stamp)
        start_time = "{ymd}".format(ymd=time.strftime('%Y-%m-%d %H:%M:%S', local_time))
        end_time = "{ymd}".format(ymd=datetime.datetime.now() + datetime.timedelta(hours=1))

        header = {
            "Content-Type": "",
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://admin.yunshuxie.com",
            "Referer":
                "https://admin.yunshuxie.com/v1/admin/live_product_info/edit_live_product_course.htm?productCourseId=107564&productType=137",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        search_user_list_url = "https://admin.yunshuxie.com/v1/admin/account/query/user_list.json"
        params = {"memberId": "", "phone": phone, "order": "asc", "limit": "10", "offset": "0", "_": "1587181586134"}
        searchUserList= requests.post(search_user_list_url, headers=header, cookies=cookies["cookies"].get_dict(), params=params)
        memberId = json.loads(searchUserList.content)["rows"][0]["memberId"]
        if searchUserList.status_code == 200:
            joinMoocClass_url = "https://admin.yunshuxie.com/v1/admin/account/update/joinMoocClass.json"  # memberID用户授权
            params = {"memberId": memberId, "moocClassId": "654761", "moocClassSn": "-1", "orderId": "-1",
                      "isNeedOrder": "0", "description": ""}
            joinMoocClassResp = requests.post(joinMoocClass_url, headers=header, cookies=cookies["cookies"], params=params)
            if joinMoocClassResp.status_code != 200:
                return joinMoocClassResp
            changeWebRTC_url = "https://admin.yunshuxie.com/v1/admin/product_chapter/merge/room.json"  # 转换为webRTC
            params = {"productChapterId": "1071013", "operationType": "1", "isWebRtc": isWebRtc, "provider": "1",
                      "targetRoomId": ""}
            changeWebRTC = requests.post(changeWebRTC_url, headers=header, cookies=cookies["cookies"], params=params)
            if changeWebRTC.status_code != 200:
                return changeWebRTC
            saveOrUpdate_live_product_chapter_url = 'https://admin.yunshuxie.com/v1/admin/product_chapter/saveOrUpdate_live_product_chapter.json'
            datas = {"productChapterId": "1071013",
                     "productCourseId": "107514",
                     "jsonData": '[{"sortCode":"1","templateType":1,"templateDataContent":{"title":"学习计划","content":""}}]',
                     "btSelectItem": "1071013",
                     "productChapterTitle": "测试003__"+start_time,
                     "wordsNumber": "0",
                     "introduction": "",
                     "readAbilityType": "-1",
                     "sortCode": "3",
                     "liveTeacherId": "356",
                     "liveTeacherName": "孙伟",
                     "chapterStartTime": start_time,
                     "chapterEndTime": end_time,
                     "title": "学习计划",
                     "content": "",
                     "button": "",
                     "fileTypeArray": ""}
            data = MultipartEncoder(datas)
            header["Content-Type"] = data.content_type
            session.headers = header
            json.dumps(datas, ensure_ascii=False, encoding="utf8")
            saveOrUpdateLiveProductChapterResp = requests.post(saveOrUpdate_live_product_chapter_url, headers=header, cookies=cookies["cookies"], data=data)
            if saveOrUpdateLiveProductChapterResp.status_code != 200:
                return saveOrUpdateLiveProductChapterResp
            query_product_chapter_list_url = "https://admin.yunshuxie.com/v1/admin/product_chapter/query_product_chapter_list.json"
            params={"productCourseId":"107514","sort":"sortCode","order":"asc","limit":"10","offset":"0","_":"1588056789573"}
            searchChapterResp = requests.get(query_product_chapter_list_url, headers=header,
                                             cookies=cookies["cookies"], params=params)
            return searchChapterResp
        else:
            return searchUserList

    if env_flag == "stage" or "prod":
        cookies = get_cookies(project="云舒写ADMIN后台管理系统", env_flag=env_flag,
                              env_num=env_num,
                              account_username="panze@yunshuxie.com",
                              account_passwd="test123456")
        time_stamp = time.time()
        local_time = time.localtime(time_stamp)  #
        start_time = "{ymd}".format(ymd=time.strftime('%Y-%m-%d %H:%M:%S', local_time))
        end_time = "{ymd}".format(ymd=datetime.datetime.now() + datetime.timedelta(hours=1))

        header = {
            "Content-Type": "",
            "User-Agent":
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://admin.yunshuxie.com",
            "Referer":
                "https://admin.yunshuxie.com/v1/admin/live_product_info/edit_live_product_course.htm?productCourseId=107564&productType=137",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        search_user_list_url = "https://admin.yunshuxie.com/v1/admin/account/query/user_list.json"
        params = {"memberId": "", "phone": phone, "order": "asc", "limit": "10", "offset": "0", "_": "1587181586134"}
        searchUserList = requests.post(search_user_list_url, headers=header, cookies=cookies["cookies"], params=params)
        memberId = json.loads(searchUserList.content)["rows"][0]["memberId"]
        if searchUserList.status_code == 200:
            joinMoocClass_url = "https://admin.yunshuxie.com/v1/admin/account/update/joinMoocClass.json"  # memberID用户授权
            params = {"memberId": memberId, "moocClassId": "664837", "moocClassSn": "-1", "orderId": "-1",
                      "isNeedOrder": "0", "description": ""}
            joinMoocClassResp = requests.post(joinMoocClass_url, headers=header, cookies=cookies["cookies"],
                                              params=params)
            if joinMoocClassResp.status_code != 200:
                return joinMoocClassResp
            changeWebRTC_url = "https://admin.yunshuxie.com/v1/admin/product_chapter/merge/room.json"  # 转换为webRTC
            params = {"productChapterId": "175801", "operationType": "1", "isWebRtc": isWebRtc, "provider": "1",
                      "targetRoomId": ""}
            changeWebRTC = requests.post(changeWebRTC_url, headers=header, cookies=cookies["cookies"], params=params)
            if changeWebRTC.status_code != 200:
                return changeWebRTC
            saveOrUpdate_live_product_chapter_url = 'https://admin.yunshuxie.com/v1/admin/product_chapter/saveOrUpdate_live_product_chapter.json'
            datas = {"productChapterId": "175801",
                     "productCourseId": "107554",
                     "jsonData": '[{"sortCode":"1","templateType":1,"templateDataContent":{"title":"学习计划","content":""}}]',
                     "btSelectItem": "175801",
                     "productChapterTitle": "测试001__"+start_time,
                     "wordsNumber": "0",
                     "introduction": "",
                     "readAbilityType": "-1",
                     "sortCode": "1",
                     "liveTeacherId": "356",
                     "liveTeacherName": "孙伟",
                     "chapterStartTime": start_time,
                     "chapterEndTime": end_time,
                     "title": "学习计划",
                     "isJob": "2",
                     "content": "",
                     "button": "",
                     "fileTypeArray": ""}
            data = MultipartEncoder(datas)
            header["Content-Type"] = data.content_type
            session.headers = header
            json.dumps(datas, ensure_ascii=False, encoding="utf8")
            saveOrUpdateLiveProductChapterResp = requests.post(saveOrUpdate_live_product_chapter_url, headers=header,
                                                               cookies=cookies["cookies"], data=data)
            if saveOrUpdateLiveProductChapterResp.status_code != 200:
                return saveOrUpdateLiveProductChapterResp
            query_product_chapter_list_url = "https://admin.yunshuxie.com/v1/admin/product_chapter/query_product_chapter_list.json"
            params = {"productCourseId": "107554", "sort": "sortCode", "order": "asc", "limit": "10", "offset": "0",
                      "_": "1588056789573"}
            searchChapterResp = requests.get(query_product_chapter_list_url, headers=header,
                                             cookies=cookies["cookies"], params=params)

            return searchChapterResp
        else:
            return searchUserList


if __name__ == "__main__":
    # print CreateBJYisWebRtc("stage", "1", "1")
    print CreateBJYRoom("beta", "1", "15810346836","0")