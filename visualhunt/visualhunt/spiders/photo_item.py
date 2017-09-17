# -*- coding: utf-8 -*-
import scrapy
import re,redis

r = redis.Redis(host='127.0.0.1', port=6379, db=1)

class Spider(scrapy.Spider):
    name = "photo_item"
    search_url = "https://visualhunt.com/popular/{}/"
    start_urls = []
    for i in range(1,5651):
        if r.sismember("parsed_page", str(i)) == False:
            start_urls.append(search_url.format(i))

    def parse(self, response):
        photos = re.findall(r'href=\"/photo/([\d]+)/',response.body.decode())
        photo_info = {
            "z":0,
        }
        for photo in photos:
            r.hmset("visualhunt:" + photo, photo_info)
        page = re.findall(r'([\d]+)',response.url)[0]
        r.sadd("parsed_page", page)