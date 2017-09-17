# -*- coding: utf-8 -*-
import scrapy, urllib
import redis
import json, re, threading

mutex = threading.Lock()
r = redis.Redis(host='127.0.0.1', port=6379, db=2)


class CanweimageSpider(scrapy.Spider):
    name = "lost_image"
    save_path = "C:\\wikimedia\\1\\"
    start_urls = []
    photos = r.keys("wiki:*")
    for key in photos:
        value = r.hgetall(key.decode())
        key = key.decode()
        key = re.findall(r':([\d]+)', key)[0]
        if r.sismember("downloaded", key) == False:
            support_ext = ['.jpg', '.png', '.tif', '.tiff', '.gif', '.jpeg', '.bmp']
            src = value['src'.encode()].decode()
            ext = src[src.rindex("."):].lower()
            width = value['width'.encode()].decode()
            height = value['height'.encode()].decode()
            reso = int(width) * int(height)
            if ext in support_ext and reso > 1900000:
                start_urls.append(src + "?photo_id=" + str(key))



    def parse(self, response):
        file_id = re.findall(r'\?photo_id=([\d]+)', response.url)[0]
        file_type = re.findall(r'.([^.]+)?photo_id=', response.url)[0]
        filename = 'wikimedia-' + file_id + '.' + file_type[:-1]
        fileHandle = open(self.save_path + filename, 'wb')
        fileHandle.write(response.body)
        fileHandle.close()

        if mutex.acquire():
            try:
                r.sadd("downloaded", file_id)
            except:
                print("add downloaded logs faild")
            finally:
                mutex.release()
