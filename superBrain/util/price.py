#!/usr/bin/python
# -*- coding:utf8 -*-

import re
import json
import copy
import pandas
import urllib
import urllib2
import datetime


url = "http://q.stock.sohu.com/hisHq"
request_data = {
    "code": None,
    "start": None,
    "end": None,
    "stat": 1,
    "order": "D",
    "period": "d",
    "rt": "jsonp",
}

titles = [
    u"日期",
    u"开盘",
    u"收盘",
    u"涨跌额",
    u"涨跌幅",
    u"最低",
    u"最高",
    u"成交量(手)",
    u"成交金额(万)",
    u"换手率",
]


def get(report_code, start, end):
    full_request_data = copy.deepcopy(request_data)
    full_request_data["code"] = "cn_" + report_code
    full_request_data["start"] = start
    full_request_data["end"] = end

    full_url = url + "?" + urllib.urlencode(full_request_data)

    request = urllib2.Request(full_url)
    response = urllib2.urlopen(request)

    jsonp = response.read().decode("gb2312")
    match = re.match(r"^callback\((.*)\)$", jsonp)
    if match:
        response_data_str = match.group(1)
        response_data = json.loads(response_data_str)

        tables = response_data[0]["hq"]
        for row in tables:
            row[0] = datetime.datetime.strptime(row[0], "%Y-%m-%d")

        return pandas.DataFrame(tables, columns=titles).set_index(u"日期")


if __name__ == "__main__":
    data = get("600570", "20130916", "20170909")
    file_path = u"C://Users//xiaot//Documents//行情.csv"

    data.to_csv(file_path, encoding="gb2312")
