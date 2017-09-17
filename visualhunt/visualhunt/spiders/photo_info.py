# -*- coding: utf-8 -*-
import scrapy
import re,redis

r = redis.Redis(host='127.0.0.1', port=6379, db=1)

class Spider(scrapy.Spider):
    name = "photo_info"
    photo_url = "https://visualhunt.com/photo/{}/"
    start_urls = []
    photos = r.keys("visualhunt:*")
    for key in photos:
        value = r.hgetall(key)
        id = re.findall(r'([\d]+)',key.decode())[0]
        try:
            temp = value['info_finished'.encode()].decode()
        except:
            start_urls.append(photo_url.format(id))

    def parse(self, response):
        download_url = re.findall(r'https://visualhunt.com/photos/[\d]/[^"]+',response.body.decode())[0]
        tags = ""
        for tag in response.css("div.tags-group > a"):
            tags = tags + tag.css("a::text").extract_first() + " "

        resolution = re.findall(r'<td>([\d]+)x([\d]+)</td>',response.body.decode())
        width = resolution[0][0]
        height = resolution[0][1]
        name = response.css("div.modal-Mainphoto > h1::text").extract_first()
        photo_id = re.findall(r'([\d]+)',response.url)[0]
        photo_info = {
            "name": name,
            "tags":tags[:-1],
            "width":width,
            "height":height,
            "download_url":download_url,
            "info_finished":1,
        }
        # print(photo_info)
        r.hmset("visualhunt:" + photo_id, photo_info)