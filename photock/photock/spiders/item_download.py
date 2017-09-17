# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
import struct
import json, re, pymysql, threading, os


class ToScrapeCSSSpider(scrapy.Spider):
    name = "photock_item"
    start_urls = ["https://www.photock.org"]
    download_url = "https://www.photock.org/download/download/{}/"
    save_path = "D:\\photock\\origin\\"


    # def parse(self, response):
    #     for i in range(1, 6000):
    #         filename = "photo0000-%04d" % i
    #         filename2 = "photo0000-%04d.jpg" % i
    #         if not os.path.exists(self.save_path + filename2):
    #             print(filename2)
    #             yield FormRequest(url=self.download_url.format(i), dont_filter=False,
    #                               formdata={'filename': filename}, callback=self.photo_save)

    def photo_save(self, response):
        # disposition = response.headers.getlist('Content-Disposition')[0]
        # p1 = r"([^\"]+\.[^\"]+)"
        # pattern1 = re.compile(p1)
        # filename = pattern1.findall(disposition.decode())
        id = re.findall(r'([\d]+)',response.url)[0]
        id = "%04d" % int(id)
        filename = "photo0000-" + id + ".jpg"
        print(filename)
        fileHandle = open(self.save_path + filename, 'wb')
        fileHandle.write(response.body)
        fileHandle.close()

    def save_db(self, item):
        sql = "insert into stocksnap (`img_id`,`width`,`height`,`tags`) values ('%s','%s','%s','%s')"
        sql = sql % (item['img_id'], item['img_width'], item['img_height'], item['tags'])
        # if mutex.acquire():
        #     try:
        #         cursor.execute(sql)
        #         connect.commit()
        #     except:
        #         print(item['img_id'] + "：插入失败，记录可能已存在")
        #     mutex.release()
