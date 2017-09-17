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
    db='pexels',
    charset='utf8'
)
cursor = connect.cursor()
mutex = threading.Lock()


class ToScrapeCSSSpider(scrapy.Spider):
    name = "pexels"
    save_path = "D:\\pexels\\origin\\"
    start_urls = []
    url = "https://www.pexels.com/?page={}&format=js&seed=2017-07-19%2002:36:18%20+0000"
    # 3204
    for i in range(1, 3204):
        start_urls.append(url.format(i))

    def parse(self, response):
        urls = re.findall(r'<a href=\\"(/photo/[^/]+/)', response.body.decode())
        for url in urls:
            yield scrapy.Request(url="https://www.pexels.com" + url, callback=self.photo_parse)

    def photo_parse(self, response):
        url = response.css(".js-download::attr(href)").extract_first()
        # filename = os.path.basename()
        filename = re.findall(r'[^/]+\.[^/]+', url)[1]
        tags_str = ""
        for tags in response.css("li > a[data-track-label='tag']"):
            tags_str = tags_str + tags.css("::text").extract_first() + " "
        size = re.findall(r'<span>([\d]+\.[\d]+ MB)</span>', response.body.decode())[0]
        resolution = re.findall(r'[\d]+ x [\d]+ pixels', response.body.decode())[0].replace(" pixels", "")

        self.save_db(url, size, tags_str, resolution)
        if not os.path.exists(self.save_path + filename):
            yield scrapy.Request(url=url, callback=self.photo_save)
        else:
            print(filename + "已下载，跳过")

    def photo_save(self, response):
        url = response.url
        filename = re.findall(r'[^/]+\.[^/]+', url)[1]
        fileHandle = open(self.save_path + filename, 'wb')
        fileHandle.write(response.body)
        fileHandle.close()

    def save_db(self, url, size, tags_str, resolution):
        sql = "insert into pexels (`url`,`size`,`resolution`,`tags`) values ('%s','%s','%s','%s')"
        sql = sql % (url, size, resolution, tags_str)
        if mutex.acquire():
            try:
                cursor.execute(sql)
                connect.commit()
            except:
                print(url + "：插入失败，记录可能已存在")
            mutex.release()
