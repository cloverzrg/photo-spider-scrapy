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
    db='photo',
    charset='utf8'
)
cursor = connect.cursor()
mutex = threading.Lock()


class ToScrapeCSSSpider(scrapy.Spider):
    name = "photock"
    save_path = "D:\\photock\\origin\\"
    start_urls = ["https://www.photock.org/", "https://www.photock.org/category/"]

    def parse(self, response):
        urls = re.findall(r'/list/[^/]+/[^/]+/', response.body.decode())
        for url in urls:
            yield scrapy.Request(url="https://www.photock.org" + url, dont_filter=False, callback=self.list_parse)

    def list_parse(self, response):
        photo_count = response.css("#photo_count::text").extract_first()
        urls = re.findall(r'/detail/[^/]+/[0-9]+/', response.body.decode())
        page = int(int(photo_count) / 51) + 2
        for i in range(2, page):
            yield scrapy.Request(url=response.url + str(i) + "/", dont_filter=False, callback=self.list_parse)

        for url in urls:
            yield scrapy.Request(url="https://www.photock.org" + url, dont_filter=False, callback=self.photo_prase)

        urls = re.findall(r'/list/[^/]+/[^/]+/', response.body.decode())
        for url in urls:
            yield scrapy.Request(url="https://www.photock.org" + url, dont_filter=False, callback=self.list_parse)

    def photo_prase(self, response):
        url = response.css("ul[class='download_conts'] > li:last-child > dl > dd > form::attr(action)").extract_first()
        url = "https://www.photock.org" + url
        filename = response.css(
            "ul[class='download_conts'] > li:last-child > dl > dd > form > input[name='filename']::attr(value)").extract_first()
        # info = response.css("table  > tr")
        # print(info)

        # title = response.css("table  > tr:nth-child(1) > td::text").extract_first()
        # tags = response.css("table > tr:nth-child(3) > td > a")
        # tags_str = ""
        # for tag in tags:
        #     tags_str = tags_str + tag.css("::text").extract_first() + " "
        # yield {"url":response.url,"tags":tags_str,"title":title}
        if not os.path.exists(self.save_path + filename):
            yield FormRequest(url=url, dont_filter=False, formdata={'filename': filename}, callback=self.photo_save)
        else:
            print(filename + "已下载，跳过")

    def photo_save(self, response):
        disposition = response.headers.getlist('Content-Disposition')[0]
        p1 = r"([^\"]+\.[^\"]+)"
        pattern1 = re.compile(p1)
        filename = pattern1.findall(disposition.decode())
        fileHandle = open(self.save_path + filename[0], 'wb')
        fileHandle.write(response.body)
        fileHandle.close()

    def save_db(self, item):
        sql = "insert into photock (`img_id`,`width`,`height`,`tags`) values ('%s','%s','%s','%s')"
        sql = sql % (item['img_id'], item['img_width'], item['img_height'], item['tags'])
        if mutex.acquire():
            try:
                cursor.execute(sql)
                connect.commit()
            except:
                print(item['img_id'] + "：插入失败，记录可能已存在")
            mutex.release()
