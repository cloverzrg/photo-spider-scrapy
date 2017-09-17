# -*- coding: utf-8 -*-
import scrapy, urllib
import redis
import json, re, threading

mutex = threading.Lock()
r = redis.Redis(host='127.0.0.1', port=6379, db=2)


class CanweimageSpider(scrapy.Spider):
    name = "canweimage"
    save_path = "C:\\wikimedia\\origin\\"
    start_urls = []
    url = "https://bqdw8wrg6d.execute-api.us-east-1.amazonaws.com/prod/search_images?search_term={}&offset={}"
    search_keys = r.hgetall("search")
    for item in search_keys:
        if int(search_keys[item].decode()) < 270:
            start_urls.append(url.format(urllib.parse.quote(item.decode()), search_keys[item].decode()))

    def parse(self, response):
        search = re.findall(r'search_term=([^&]+)&', response.url)[0]
        offset = re.findall(r'&offset=([\d]+)', response.url)[0]
        decode_search = urllib.parse.unquote(search)
        print("search:" + decode_search + ", offset:" + offset)
        return_json = response.body.decode().replace("\\\"", "\"").replace("\"{", "{").replace("}\"", "}").replace(
            "\\\\", "\\")
        data = json.loads(return_json)
        images = data['images']
        for item in images:
            photo_info = {
                "search": decode_search,
                "offset": offset,
                "src": images[item]['src'],
                "title": images[item]['title'],
                "detailsUrl": images[item]['detailsUrl'],
                "width": images[item]['width'],
                "height": images[item]['height'],
            }
            if mutex.acquire():
                r.hmset("wiki:" + item, photo_info)
                mutex.release()

            # if r.sismember("downloaded", item) == False:
            support_ext = ['.jpg', '.png', '.tif', '.tiff', '.gif', '.jpeg', '.bmp']
            src = images[item]['src']
            ext = src[src.rindex("."):].lower()
            width = images[item]['width']
            height = images[item]['height']
            reso = int(width) * int(height)
            if ext in support_ext and reso > 1900000 and r.sismember("downloaded", item) == False:
                yield scrapy.Request(url=images[item]['src'] + "?photo_id=" + item, callback=self.photo_save,
                                 headers={'Referer': 'https://canweimage.com/'})

        if mutex.acquire():
            r.hset("search", decode_search, int(offset) + 1)
            mutex.release()
        if data['result'] == 'images':
            yield scrapy.Request(url=self.url.format(search, int(offset) + 1), callback=self.parse,
                                 headers={'Referer': 'https://canweimage.com/'})

    def photo_save(self, response):
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
