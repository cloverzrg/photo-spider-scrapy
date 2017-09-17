# -*- coding: utf-8 -*-
import scrapy
import pymongo,time
import json, re, threading

mutex = threading.Lock()
conn = pymongo.MongoClient('localhost', 27017)
db = conn.unsplash
search_result = db.unsplash
info_db = db.info

class UnsplashSpider(scrapy.Spider):
    name = "unsplash_info"
    info_url = "https://unsplash.com/napi/photos/{}/info"
    start_urls = []

    for item in search_result.find():
        break
        for item2 in item['results']:
            if info_db.find_one({"id":item2['id']}) == None:
                start_urls.append(info_url.format(item2['id']))


    def parse(self, response):
        data = json.loads(response.body)
        info_db.insert(data)