#!/usr/bin/python
# -*- coding:utf8 -*-

import os
import re
import pandas


def read(file_path, encoding="utf-8", pattern=r"\s"):
    if os.path.exists(file_path):
        f = open(file_path, 'r')
        try:
            title_str = f.readline().decode(encoding)
            if not title_str:
                return

            titles = [title for title in re.split(pattern, title_str) if title]
            datas = {}
            for title in titles:
                datas[title] = []

            while True:
                line_str = f.readline().decode(encoding)
                if not line_str:
                    break

                values = [value for value in re.split(pattern, line_str) if value]
                for i in range(len(values)):
                    value = values[i]
                    datas[titles[i]].append(value)

            # for values in datas.values():
            #     print len(values)

            return pandas.DataFrame(datas)
        finally:
            f.close()


if __name__ == "__main__":
    print read(u"C://Users//xiaot//Documents//A股.xls", "gb2312")
    # print pandas.read_csv(u"C://Users//xiaot//Documents//A股.xls", encoding="gb2312", delimiter="\t")
