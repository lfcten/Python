#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time     : 2017/7/27 10:24
@Author   : Danxiyang
@File     : example1.py
@Software : PyCharm
"""
# 可以尝试理解下(\w)((?=\1\1\1)(\1))+ 的匹配过程
import re
import time

# Apache日志文件分割

data = '127.0.0.1 - frank [10/Oct/2000:13:55:36 +0800] "GET /apache_pd.gif HTTP/1.0" 200 2326 "http://www.example.com/start.html" "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0"'

pattern = re.compile(r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)(?![^\[]*\])')
result = re.split(pattern, data)


def parseTime(t):
    t = re.sub(r'\[|\]', '', t)
    t = time.strptime(t, '%d/%b/%Y:%H:%M:%S +0800')
    return time.strftime("%Y-%m-%d %a %H:%M:%S", t)


def parseRequest(r):
    r = re.sub(r'"', '', r)
    return r

print(f'ip:       {result[0]}')
print(f'time:     {parseTime(result[3])}')
print(f'request:  {parseRequest(result[4])}')
print(f'status:   {result[5]}')
print(f'size:     {result[6]}')
print(f'refer:    {parseRequest(result[7])}')
print(f'header:   {parseRequest(result[8])}')
