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
    db='stockvault',
    charset='utf8'
)
cursor = connect.cursor()
mutex = threading.Lock()


class StockvaultSpider(scrapy.Spider):
    name = "stockvault"
    save_path = "D:\\stockvault\\origin\\"
    start_urls = ["http://www.stockvault.net/"]
    allowed_domains = ["www.stockvault.net", "stockvault.net"]

    def parse(self, response):
        urls = re.findall(r'href="//www.stockvault.net(/c/[^"]+)"', response.body.decode())
        for url in urls:
            yield scrapy.Request(url="http://www.stockvault.net" + url, callback=self.categories_parse)

    def categories_parse(self, response):
        photos = re.findall(r'/photo/[\d]+/[^\']+', response.body.decode())
        for photo in photos:
            yield scrapy.Request(url="http://www.stockvault.net" + photo, callback=self.photo_parse)

        urls = re.findall(r'/c/[^/]+/\?.{0,4}p=[\d]+', response.body.decode())
        for url in urls:
            yield scrapy.Request(url="http://www.stockvault.net" + url, callback=self.categories_parse)

    def photo_parse(self, response):
        url = re.findall(r'onclick="window.location.href=\'(/photo/download/[\d]+)\'"', response.body.decode())[0]
        id = re.findall(r'([\d]+)', url)[0]
        title = response.xpath("/html/head/title/text()").extract_first().replace(" Free Stock Photo - Free Images", '')

        tags_str = ""
        for tags in response.css("div.tagcloud.cut.nobottommargin > a"):
            if tags.css("::text").extract_first():
                tags_str = tags_str + tags.css("::text").extract_first() + " "
        file_size = re.findall(r'[\d]{1,3}\.[\d]{1,3} MB|[\d]{1,3}\.[\d]{1,3} KB', response.body.decode())[0]
        resolution = re.findall(r'[\d]{1,5} x [\d]{1,5} px', response.body.decode())[0].replace(" px", "")

        self.save_db(id, title, tags_str, file_size, resolution)

        if not os.path.exists(self.save_path + id + '.jpg'):
            yield scrapy.Request(url="http://www.stockvault.net" + url, callback=self.photo_save)
        else:
            print(title + "已下载，跳过")

    def photo_save(self, response):
        id = re.findall(r'([\d]+)', response.url)[0]
        fileHandle = open(self.save_path + id + '.jpg', 'wb')
        fileHandle.write(response.body)
        fileHandle.close()
        print("下载完成：" + id)

    def save_db(self, id, title, tags_str, size, resolution):
        sql = "insert into stockvault (`id`,`title`,`tags`,`file_size`,`resolution`) values ('%s','%s','%s','%s','%s')"
        sql = sql % (id, title.replace('\'', ''), tags_str.replace('\'', ''), size, resolution)
        if mutex.acquire():
            try:
                # print(sql)
                cursor.execute(sql)
                connect.commit()
            except:
                print(id + "：插入失败，记录可能已存在")
            mutex.release()
