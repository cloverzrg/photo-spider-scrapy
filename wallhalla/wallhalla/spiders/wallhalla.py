# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
import struct
import json, re, pymysql, threading, os

connect = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='root',
    db='wallhalla',
    charset='utf8'
)
cursor = connect.cursor()
mutex = threading.Lock()


class StockvaultSpider(scrapy.Spider):
    name = "wallhalla"
    url = "https://wallpapers.wallhaven.cc/wallpapers/full/wallhaven-{}.jpg"
    start_urls = []
    for i in range(1, 543435):
        start_urls.append(url.format(i))

    def parse(self, response):
        filename = re.findall(r'/(wallhaven-[\d]+.jpg)', response.url)[0]
        fileHandle = open("D:\\wallhalla\\origin\\" + filename, 'wb')
        fileHandle.write(response.body)
        fileHandle.close()
        print("下载完成：" + filename)
