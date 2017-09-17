# -*- coding: utf-8 -*-
import scrapy
import pymongo,time
import json, re, threading

mutex = threading.Lock()
conn = pymongo.MongoClient('localhost', 27017)
db = conn.unsplash
search_result = db.unsplash
downloaded = db.downloaded

class UnsplashSpider(scrapy.Spider):
    name = "unsplash_download"
    save_path = "C:\\unsplash\\origin\\"
    start_urls = []

    for item in search_result.find():
        break
        for item2 in item['results']:
            if downloaded.find_one({"id":item2['id']}) == None:
                start_urls.append(item2['urls']['raw'] + "?id=" + item2['id'])



    def parse(self, response):
        file_id = re.findall(r'\?id=(.*)', response.url)[0]
        file_type = response.headers.getlist('content-type')[0].decode()
        filename = 'unsplash-' + file_id + '.jpg'
        fileHandle = open(self.save_path + filename, 'wb')
        fileHandle.write(response.body)
        fileHandle.close()
        data = {}
        data['url'] = response.url
        data['id'] = file_id
        data['content-type'] = file_type
        data['time'] = time.time()
        if mutex.acquire():
            try:
                downloaded.insert(data)
            except:
                print("add downloaded logs faild")
            finally:
                mutex.release()