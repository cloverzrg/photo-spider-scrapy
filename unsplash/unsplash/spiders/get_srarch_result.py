# -*- coding: utf-8 -*-
import scrapy
import redis,pymongo
import json, re

r = redis.Redis(host='127.0.0.1', port=6379, db=3)

conn = pymongo.MongoClient('localhost', 27017)
db = conn.unsplash
search_result = db.unsplash

class UnsplashSpider(scrapy.Spider):
    name = "unsplash"
    save_path = "C:\\unsplash\\origin\\"
    search_keys = ["business","coffee","nature","love","team","health","space","social","computer","girl","food","people","work","office","music","landscape","family","couple","pug","canada","wedding","bike","laptop","rain","fitness","new","autumn","desk","flowers","woman","clothing","happy","clock","iphone","road","yoga","man","home","tree","mountains","city","summer","nasa","feet","friends","shopping","japan","typewriter","house","restaurant","sky","watch"]
    search_url = "https://unsplash.com/napi/search/photos?query={}&xp=&per_page=20&page={}"
    start_urls = []
    for item in search_keys:
        start_urls.append(search_url.format(item,1))

    def parse(self, response):
        data = json.loads(response.body)
        search_key = re.findall(r'query=([^&]+)&', response.url)[0];
        cur_page = re.findall(r'&page=([\d]+)', response.url)[0];
        data['search_key'] = search_key
        data['cur_page'] = cur_page
        search_result.insert(data)
        total_pages = data['total_pages']
        for i in range(2,total_pages + 1):
            yield scrapy.Request(url=self.search_url.format(search_key,i),callback=self.search_page_parse)

    def search_page_parse(self,response):
        data = json.loads(response.body)
        search_key = re.findall(r'query=([^&]+)&', response.url)[0];
        cur_page = re.findall(r'&page=([\d]+)', response.url)[0];
        data['search_key'] = search_key
        data['cur_page'] = cur_page
        search_result.insert(data)