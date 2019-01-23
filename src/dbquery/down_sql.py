# coding=utf-8
import json
import time

import requests

import re

# 12个小时的查询范围
# TIME_RANGE_12 = ('2018-11-29 20:00:00', '2018-11-30 08:00:00')
TIME_RANGE_12 = ('2018-05-29 20:00:00', '2018-05-30 08:00:00')

# 24个小时的查询范围
# TIME_RANGE_24 = ('2018-11-29 20:00:00', '2018-11-30 20:00:00')
TIME_RANGE_24 = ('2018-05-29 20:00:00', '2018-05-30 20:00:00')
# 供授权使用:需要登录dbsv4.jd.com后从浏览器Dev-tools里面粘贴(比较长,大概2000个字符)
# COOKIE = ""


class DownSql:
    @staticmethod
    def down_sql(_name, _sql, cookie_str):
        time.sleep(0.5)
        print('\n%s\n%s' % (_name, _sql))
        # ok
        url = "http://dbsv4.jd.com/dbquery/queryData"
        querystring = {"domain": "ynord01s.mysql.jddb.com", "dbName": "uad_i18n", "sql": _sql}
        headers = {
            'Accept': "application/json, text/javascript, */*; q=0.01",
            'Accept-Encoding': "gzip, deflate",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
            'Cache-Control': "no-cache",
            'Cookie': cookie_str,
            'Connection': "keep-alive",
            'Host': "dbsv4.jd.com",
            'Origin': "http://dbsv4.jd.com",
            'Pragma': "no-cache",
            'Referer': "http://dbsv4.jd.com/dbquery/index?1527500905186",
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
            'X-Requested-With': "XMLHttpRequest"
        }
        # load
        response = requests.request("POST", url, headers=headers, params=querystring)
        if response.text is None:
            exit(1)
        res = json.loads(response.text)
        # format
        tb = []
        for obj in res['data'].items():
            row = []
            for data_list in obj[1].items():
                if type(data_list) != tuple or type(data_list[1]) == int or data_list[1] is None:
                    continue
                for column in data_list[1]:
                    # 去掉多余的空行
                    blank_line = re.compile('\n+')
                    s = blank_line.sub(r'', column.get('content'))
                    row.append(column.get('caseId') + '\t' + s)
                    row.append('\n')
                    print('row  = ' + s)
                tb.append(row)
                break
        # print
        f = open('down_sql.py.out', 'a+', encoding='utf-8')
        # f.write('=========================\n=== %s\n=========================' % _name)
        for row in tb:
            f.write('\n')
            f.write(''.join(row))
        f.write('\n\n')
        f.close()

    def __init__(self, cookie):
        self.down_sql('email', ("select case_id as caseId, content from biz_conversation_record where bill_type = 2	 and content is not null"), cookie)
