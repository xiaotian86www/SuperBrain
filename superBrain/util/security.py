#!/usr/bin/python
# -*- coding:utf8 -*-

import re
import bs4
import pandas
import datetime
import urllib
import urllib2

url = "http://data.10jqka.com.cn/market/rzrqgg/code/$(code)/order/desc/page/$(page)/ajax/2/"


def get(report_code, start=datetime.datetime(1800, 1, 1), end=datetime.datetime.now()):
    if start > end or not report_code:
        return None

    titles = [
        u"序号",
        u"日期",
        u"融资余额",
        u"融资买入额",
        u"融资偿还额",
        u"融资净买入额",
        u"融券余量",
        u"融券卖出量",
        u"融券偿还量",
        u"融券净卖出",
        u"融资融券余额",
    ]

    page = 0
    df = pandas.DataFrame(columns=titles)
    while True:
        page += 1
        full_url = re.sub(r"\$\(code\)", report_code, url)
        full_url = re.sub(r"\$\(page\)", str(page), full_url)


        print u"获取第" + unicode(page) + u"页开始"
        request = urllib2.Request(full_url)
        response = urllib2.urlopen(request)
        response_data = response.read().decode("gb2312")
        bs = bs4.BeautifulSoup(response_data, "html.parser")
        print u"获取第" + unicode(page) + u"页结束"

        print u"获取第" + unicode(page) + u"页数据开始"
        rows = []
        for row in bs.select("tbody tr"):
            row_list = [tag.string.strip() for tag in row.find_all("td")]
            #遍历完所有记录
            if not row_list[1]:
                break

            row_list[0] = int(row_list[0])
            row_list[1] = datetime.datetime.strptime(row_list[1], "%Y-%m-%d")
            row_list[2] = _trans_balance(row_list[2])
            row_list[3] = _trans_balance(row_list[3])
            row_list[4] = _trans_balance(row_list[4])
            row_list[5] = _trans_balance(row_list[5])
            row_list[6] = _trans_balance(row_list[6])
            row_list[7] = _trans_balance(row_list[7])
            row_list[8] = _trans_balance(row_list[8])
            row_list[9] = _trans_balance(row_list[9])
            row_list[10] = _trans_balance(row_list[10])

            rows.append(row_list)

        if not rows:
            print u"这已经是最后一页"
            break
        else:
            print u"获取第" + unicode(page) + u"页数据结束"

        tdf = pandas.DataFrame(rows, columns=titles)
        if tdf[u"日期"].max() < start:
            print u"已超过日期范围"
            break
        elif tdf[u"日期"].max() > end:
            print u"还未进入日期范围"
            continue
        else:
            print u"插入数据"
            df = df.append(tdf[(tdf[u"日期"] >= start) & (tdf[u"日期"] <= end)])

    del df[u"序号"]

    return df.set_index(u"日期")


def _trans_balance(balance_str):
    cp = re.compile(ur"([-\d.]+)([亿万]?)")
    match = cp.match(balance_str)
    if match:
        balance = float(match.group(1))
        unit = {
            u"亿": 100000000,
            u"万": 10000,
            "": 1
        }

        balance *= unit[match.group(2)]

        return balance


if __name__ == "__main__":
    data = get("600570")
    file_path = u"C://Users//xiaot//Documents//融资融券.csv"

    data.to_csv(file_path, encoding="gb2312")
