#!/usr/bin/python
# -*- coding:utf8 -*-

import pandas
import numpy
import datetime


def _translation(series, n):
    buf = {}
    for key in series.index:
        buf[key + n] = series[key]

    ret = pandas.Series(buf)
    ret.index.name = series.index.name
    ret.name = series.name

    return ret


if __name__ == "__main__":
    hq = pandas.read_csv(u"C://temp//行情.csv", encoding="gb2312")
    rzrq = pandas.read_csv(u"C://temp//融资融券.csv", encoding="gb2312")

    result = {}
    for i in range(-20, 6):
        if i < 0:
            data = hq.loc[:hq.shape[0] + i - 1, [u"开盘"]].join(_translation(rzrq[u"融资余额"], i))
        elif i > 0:
            data = hq.loc[i:, [u"开盘"]].join(_translation(rzrq[u"融资余额"], i))
        else:
            data = hq.loc[:, [u"开盘"]].join(_translation(rzrq[u"融资余额"], i))

        result[i] = data.corr().loc[u"开盘", u"融资余额"]

    print pandas.Series(result)

    # data = hq[u"开盘"].join(rzrq[u"融资融券余额"])



    # data.corr().to_csv(u"C://Users//xiaot//Documents//结论.csv", encoding="gb2312")
