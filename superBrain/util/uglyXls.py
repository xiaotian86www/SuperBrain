#!/usr/bin/python
# -*- coding:utf8 -*-

import os
import re
import pandas


def read(file_path):
    if os.path.exists(file_path):
        f = open(file_path, 'r')
        try:
            title_str = f.readline().decode("gb2312")
            if not title_str:
                return

            titles = [title for title in re.split(r"\s", title_str) if title]
            datas = {}
            for title in titles:
                datas[title] = []

            while True:
                line_str = f.readline().decode("gb2312")
                if not line_str:
                    break

                values = [value for value in re.split(r"\s", line_str) if value]
                for i in range(len(values)):
                    value = values[i]
                    datas[titles[i]].append(value)

            # for values in datas.values():
            #     print len(values)

            return pandas.DataFrame(datas)
        finally:
            f.close()


if __name__ == "__main__":
    print read(u"D://A股.xls")


