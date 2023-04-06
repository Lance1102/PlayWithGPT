# -*- coding:utf-8 -*-
r'''
@StartTime:   2021-02-15
@Author   :   Lance Liu
@Version  :   #: 1.1 :#
@Contact  :   coder.coding.liang@gmail.com
@License  :   (C)Copyright 2020, coder.coding Lab
@AppName  :   #n ▇ CNS Scraping from AJAX Web：cnsonline.com.tw ▇▇
@Reference:   #n Python 網路爬蟲 Web Crawler 教學 - AJAX / XHR 網站技術分析實務 By 彭彭
引用練習 17_Web Crawler.py
'''

#_ import lib block

import json  # 解析 JSON
import math  # 計算百分比用
import os  # 系統目錄操作

import time
import urllib.request as req  # 連線請求

from bs4 import BeautifulSoup  # 解析 HTML


#_ function code block
def cns_request_GenerateImage(generalno='60335-1', version='zh_TW', pageNum='1', checksum='') -> str:
    url = "https://www.cnsonline.com.tw//preview/GenerateImage?" \
        + "generalno=" + generalno \
        + "&" + "version=" + version \
        + "&" + "pageNum=" + pageNum \
        + "&" + "checksum=" + checksum
    return url

def cns_request_GetData(generalno='60335-1', version='zh_TW', pageNum='1', pages='145') -> str:
    url = "https://www.cnsonline.com.tw//preview/GetData?" \
        + "generalno=" + generalno \
        + "&" + "version=" + version \
        + "&" + "pageNum=" + pageNum \
        + "&" + "pages=" + pages
    return url

def progressbar(percent=0, width=50, process_string=''):
    left = width * percent // 100
    right = width - left
    print('\r', process_string, ' [', '▇' * left, ' ' * right, ']', f' {percent:.0f}%', sep='', end='', flush=True)


#_ main code block


print('\n')
print('\x1b[5;37;40m {} \x1b[0m'.format('▄▄▄ Ｓｔａｒｔ ↓ ▄▄▄▄▄▄▄▄▄▄'))
print('\n')
#</> 程式開始 ==================================================================================


#? 輸入要抓取的資料 (初始資料) 網址：https://www.cnsonline.com.tw//?node=search&locale=zh_TW
generalno   = '15599'     # 修改標準號
# version     = 'en_US'       # 英文版(如有的話)
version     = 'zh_TW'       # 中文版
pageNum     = '1'           # 修改要開始抓的頁面
pages       = '23'         # 總頁數：要先解析第一次送出的請求才會知道


# 取得當前指令碼檔案的絕對路徑
absFilePath = os.path.abspath(__file__)
this_filepath, this_filename = os.path.split(absFilePath)

# 建立要儲存圖片的資料夾
os.makedirs(this_filepath + '/img/' + generalno + '_' + version + '/',exist_ok=True)
Path_to_store = this_filepath + '/img/' + generalno + '_' + version + '/'

pageNum_str = pageNum

# 遞迴處理
for i in range(int(pageNum), int(pages)+1):

    # Console 狀態顯示
    process_str = '下載：' + generalno + '  ' + 'Page ' + pageNum_str + '/' + pages

    # 呼叫函式 cns_request_GetData
    request_GetData_URL = cns_request_GetData(generalno, version, pageNum_str, pages)

    # 建立一個 Request 物件，附加 Request Headers 的資訊
    request_GetData_temp = req.Request(request_GetData_URL, headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.151 Safari/537.36",
    })
    
    with req.urlopen(request_GetData_temp) as response:
        GetData = response.read().decode("UTF-8") # 觀察 response 資料格式為 HTML

    # print(GetData)   # 觀察解析用 --> <Status>, <Message>
    # 
    # <Response>
    #     <Status>TRUE</Status>
    #     <Message>Successful!,90096a4831a6463c7b38931e66f3d9f0b8b94489</Message>
    # </Response>


    response_Status = BeautifulSoup(GetData, "html.parser").find('status').string  # type: ignore

    response_checksum_temp = BeautifulSoup(GetData, "html.parser").find('message').string.split(',')  # type: ignore

    request_GenerateImage_URL = cns_request_GenerateImage(generalno, version, pageNum_str, checksum=response_checksum_temp[1])

    # if response_Status == "TRUE":
    #     print('Get response Checksum: ', response_checksum_variable)
    #     print('request URL: \n', request_GenerateImage_URL)
    # else:
    #     print('<-- Error -->')

    req.urlretrieve(request_GenerateImage_URL, Path_to_store + generalno + '_Page_' + pageNum_str + '.jpg')
    # urllib.request.urlretrieve() 函式 --> 將取得的物件(本案為圖片)下載到本地

    percent_int = round(i/int(pages)*100)

    progressbar(percent=percent_int, width=40, process_string=process_str)
    time.sleep(1)

    pageNum_str = str(int(pageNum_str)+1)



print('\n\n')
print('\x1b[5;37;40m {} \x1b[0m'.format('▀▀▀　　 Ｅｎｄ ↑ ▀▀▀▀▀▀▀▀▀▀'), '\n')
#</> 程式結束 ==================================================================================


r'''
== Note ============================================================================================
@Time      :   2021-02-15 19:26:33
Descirption:   初版已完成

#*      最終組合送出請求：
"https://www.cnsonline.com.tw//preview/GenerateImage?" \
    + "generalno=" 60335-1          --> request_generalno_variable
    + "&" + "version=" + zh_TW      --> request_version_variable
    + "&" + "pageNum=" + 1          --> request_pageNum_variable
    + "&" + "checksum=" +               response_checksum_variable

#//   把程式碼用迴圈包起來即可全部下載
#>todo   前端解析：直接打入想要檢索的標準號，取得 generalno & pages --> 首頁送出標準關鍵字請求後，返回選項(標準號、年版、標準名稱、頁數) --> 使用者選擇後直接將這些參數帶入目前的code跑
#>todo   GUI化：需學習Qt
#>todo   整合為PDF、處理水印：需學習PDFLib

== Note ============================================================================================
@Time      :   2021-02-16 20:04:55
Descirption:   實作進度條 (processbar)



# 標記說明(延伸模組：Better Comments + todo-highlight)：
#*      High Priority Important Comments / 特別重要備註
#!      Normal Priority Important Comments / 重要備註
#$      High Priority Notes / 需特別注意的筆記
#n      Normal Priority Notes / 常用筆記
#&      Low Priority Notes / 一般筆記
#+>     TODO / 加強提醒待辦
#>      TODO / 待辦
#ep     Useful Examples / 非常有用的範例
#ex     Normal Examples / 一般範例
#?      Need to check / 待確認、待研究
#--     Checked / 已完成、已筆記
#_      Block Mark / 分區塊用標記
#::#    #:Word Mark / 單詞標記:#
'''
