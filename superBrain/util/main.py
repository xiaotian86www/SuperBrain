#!/usr/bin/python
# -*- coding:utf8 -*-

import pandas


if __name__ == "__main__":
    hq = pandas.read_csv(u"C://Users//xiaot//Documents//行情.csv", index_col=u"日期", encoding="gb2312")
    rzrq = pandas.read_csv(u"C://Users//xiaot//Documents//融资融券.csv", index_col=u"日期", encoding="gb2312")

    data = hq.loc[:, [u"开盘"]].join(rzrq.loc[:, [u"融资融券余额"]])
    # data = hq[u"开盘"].join(rzrq[u"融资融券余额"])

    for kvp in data:
        print kvp

    print data.corr()

    # data.corr().to_csv(u"C://Users//xiaot//Documents//结论.csv", encoding="gb2312")
