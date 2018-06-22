# -*- coding:utf-8 -*-
"""
@author:Zzb.
@file:newsreport.py
@time:2018/6/2011:06
"""

import requests
from bs4 import BeautifulSoup
import chardet
import json
from MEmail import send_ms
import datetime


# 爬取页面
def get_page(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
    }
    html = requests.get(url, headers=headers)
    # 编码检测并将检测结果设置为html的编码设置
    Encoding = chardet.detect(html.content)['encoding']
    html.encoding = Encoding
    data = html.text
    return data


# 获取更新的番数据
def get_data(data):
    news = {}
    bangumi = json.loads(data)
    for i in bangumi.get('result'):
        if i.get('new') == True:
            news[i.get('title')] = i.get('lastupdate_at')
            # news.append(i.get('title'))
            # date.append(i.get('lastupdate_at'))
    return news


# 查看喜欢的番有没更新
def list_same(dict1, list2):
    for j in list(dict1.keys()):
        if j not in list2:
            del dict1[j]


# 通过邮件发送通知
def send_report(result):
    if len(result) != 0:
        s = ''
        for m in result.keys():
            s = s + m + '已更新！\n'
        send_ms(s)

#查看更新时间与运行时间的间隔
def mytime(str1):
    startime = datetime.datetime.strptime(str1, "%Y-%m-%d %H:%M:%S")
    nowtime = datetime.datetime.now()
    endtime = nowtime - startime
    # print(startime)
    return endtime.total_seconds()



if __name__ == '__main__':
    url = 'https://bangumi.bilibili.com/jsonp/timeline_v2_global'
    like = ['超能力女儿', '多田君不恋爱', '我的英雄学院 第三季', '戒律的复活', '棒球大联盟 2']
    data = get_page(url)
    new_data = get_data(data)
    list_same(new_data, like)

    for key,value in new_data.items():
        endtime = mytime(value)
        if endtime < 3601:
            send_ms(key + '已更新！\n')

