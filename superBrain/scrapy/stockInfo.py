#!/usr/bin/python
# -*- coding:utf8 -*-

from bs4 import BeautifulSoup
import urllib
import urllib2
import xlrd


class StockInfo:
    def __init__(self):
        pass

    @staticmethod
    def collection():
        # cookie = cookielib.CookieJar()
        # handler = urllib2.HTTPCookieProcessor(cookie)
        # opener = urllib2.build_opener(handler)

        # response = opener.open("http://www.sse.com.cn/assortment/stock/list/share/")
        # #获取cookie值
        # soup = BeautifulSoup(response.read().decode("utf-8"), "html.parser")
        # tags = soup.select(".mysse_feedbackdiv #form_sample_1 #lastUpdateUser")
        # if len(tags) == 0:
        #     print '".mysse_feedbackdiv #form_sample_1 #lastUpdateUser" tag is not exist'
        #     return
        # else:
        #     tag = tags[0]
        #     print tag.attrs["value"]

        # #抓取股票列表
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, sdch",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Connection": "keep-alive",
            "Host": "query.sse.com.cn",
            "Referer": "http://www.sse.com.cn/market/othersdata/margin/sum/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        }
        #
        # datas = {
        #     "jsonCallBack": "jsonpCallback29041",
        #     "isPagination": True,
        #     "stockCode": "",
        #     "csrcCode": "",
        #     "areaName": "",
        #     "stockType": 1,
        #     "pageHelp.cacheSize": 1,
        #     "pageHelp.beginPage": 1,
        #     "pageHelp.pageSize": 25,
        #     "pageHelp.pageNo": 1,
        # }
        #
        # url = "http://query.sse.com.cn/security/stock/getStockListData2.do?" + urllib.urlencode(datas)
        #
        # request = urllib2.Request(url, None, headers)
        # response = opener.open(request)
        # str = response.read().decode('utf-8')

        datas = {
            "csrcCode": "",
            "stockCode": "",
            "areaName": "",
            "stockType": 1
        }
        url = "http://query.sse.com.cn/security/stock/downloadStockListFile.do"
        full_url = url + "?" + urllib.urlencode(datas)

        request = urllib2.Request(full_url, headers = headers)
        response = urllib2.urlopen(request)

        file_path = u"C://Users//xiaot//Documents//A股.xls"
        f = open(file_path, 'wb')
        block_size = 8192
        while True:
            fbuffer = response.read(block_size)
            if not fbuffer:
                break

            f.write(fbuffer)

        f.close()

        xls = xlrd.open_workbook(file_path)
        table = xls.sheet_by_index(0)
        row = table.row(0)
        for cell in row:
            print cell.value


if __name__ == '__main__':
    StockInfo.collection()
