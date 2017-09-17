# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest
import struct
import json, re,redis, threading, os
import glob

r = redis.Redis(host='127.0.0.1', port=6379, db=4)

class ToScrapeCSSSpider(scrapy.Spider):
    name = "photock_info"
    start_urls = ["https://www.photock.org"]
    info_url = "https://www.photock.org/detail/photo/{}/"

    ROOT_PATH = os.path.abspath(os.path.dirname("D:\\photock\\"))
    IMG_PATH = os.path.join(ROOT_PATH, 'origin')

    files = glob.glob(os.path.join(IMG_PATH, '*.*'))
    i = 0
    for file in files:
        file_name = os.path.basename(file)
        base, ext = os.path.splitext(file_name)
        id = re.findall(r'^photock-photo0000-([\d]+)$', base)[0]
        start_urls.append(info_url.format(int(id)))
        i=i+1
        # if i>2:
        #     break
    print(i)

    def parse(self, response):
        id = re.findall(r'/photo/([\d]+)/',response.url)[0]
        title = response.css("table  > tr:nth-child(1) > td::text").extract_first()
        tags = response.css("table > tr:nth-child(3) > td > a")
        tags_str = ""
        for tag in tags:
            tags_str = tags_str + tag.css("::text").extract_first() + " "

        tags_str = tags_str.strip()

        photo_info = {
            "id": id,
            "title": title,
            "tags_str": tags_str,
        }
        r.hmset("photock:" + str(id), photo_info)