# -*- coding: utf-8 -*-
import scrapy
import pymongo
import json,pymysql

conn = pymongo.MongoClient('localhost', 27017)
db = conn.unsplash
search_result = db.unsplash
info_db = db.info

connect = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='root',
    db='photo',
    charset='utf8'
)
cursor = connect.cursor()

class UnsplashSpider(scrapy.Spider):
    name = "unsplash_info2"
    info_url = "https://unsplash.com/napi/photos/{}/info"
    start_urls = []
    k = set()
    for item in info_db.find():
        k.add(item['id'])
    print(len(k))
    i = 0

    sql = "select photo_id from unsplash"
    cursor.execute(sql)
    photos = cursor.fetchall()
    for item in photos:
        if item[0] not in k:
            start_urls.append(info_url.format(item[0]))
            i= i+1
            print(i)
            print(item[0])



    def parse(self, response):
        data = json.loads(response.body)
        # info_db.insert(data)