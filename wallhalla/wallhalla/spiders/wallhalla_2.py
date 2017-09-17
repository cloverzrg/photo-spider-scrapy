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
    url = "https://alpha.wallhaven.cc/search?q=&search_image=&resolutions=2560x1440%2C2560x1600%2C3840x1080%2C5760x1080%2C3840x2160%2C5120x2880&sorting=date_added&order=desc&page={}"
    start_urls = []
    for i in range(1, 1169):
        start_urls.append(url.format(i))

    def parse(self, response):
        urls = re.findall(r'https://alpha.wallhaven.cc/wallpaper/[\d]+', response.body.decode())
        for url in urls:
            yield scrapy.Request(url=url, callback=self.photo_parse)

    def photo_parse(self, response):
        pass

    def save_photo(self, response):
        filename = re.findall(r'/(wallhaven-[\d]+.jpg)', response.url)[0]
        fileHandle = open("D:\\wallhalla\\origin\\" + filename, 'wb')
        fileHandle.write(response.body)
        fileHandle.close()
        print("下载完成：" + filename)
