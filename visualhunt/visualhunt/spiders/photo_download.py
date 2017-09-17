# -*- coding: utf-8 -*-
import scrapy
import re,redis

r = redis.Redis(host='127.0.0.1', port=6379, db=1)

class Spider(scrapy.Spider):
    name = "photo_download"
    save_path = "D:\\visualhunt\\origin\\"
    start_urls = []
    photos = r.keys("visualhunt:*")
    i=0
    for key in photos:
        value = r.hgetall(key)
        id = re.findall(r'([\d]+)',key.decode())[0]
        try:
            temp = value['downloaded'.encode()].decode()
        except:
            start_urls.append(value['download_url'.encode()].decode() + "?id=" + id)
            print(value['download_url'.encode()].decode() + "?id=" + id)
            i=i+1
            if i>3:
                break



    def parse(self, response):
        file_id = re.findall(r'\?id=([\d]+)', response.url)[0]
        file_type = re.findall(r'.([^.]+)?id=', response.url)[0]
        filename = 'visualhunt-' + file_id + '.' + file_type[:-1]
        fileHandle = open(self.save_path + filename, 'wb')
        fileHandle.write(response.body)
        fileHandle.close()

        # r.hset("visualhunt:" + file_id,"downloaded",1)