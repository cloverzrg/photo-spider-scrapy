# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest, Request
import json, re, os, redis

r = redis.Redis(host='127.0.0.1', port=6379, db=5)


class Spider(scrapy.Spider):
    name = "absfreepic"
    save_path = "D:\\absfreepic\\origin\\"
    start_urls = ["http://absfreepic.com/"]

    def parse(self, response):
        photos = re.findall(r'http://absfreepic\.com/free-photos/download/[^./]+.html', response.body.decode())
        for photo in photos:
            yield Request(url=photo, callback=self.photo_parse)

        tags = re.findall(r'http://absfreepic\.com/free-photos/[^./]+.html', response.body.decode())
        for tag in tags:
            if tag.find("_sort_") == -1:
                yield Request(url=tag, callback=self.tag_page_parse)

    def tag_page_parse(self, response):
        photos = re.findall(r'http://absfreepic\.com/free-photos/download/[^./]+.html', response.body.decode())
        for photo in photos:
            yield Request(url=photo, callback=self.photo_parse)

        tags = re.findall(r'http://absfreepic\.com/free-photos/[^./]+.html', response.body.decode())
        for tag in tags:
            if tag.find("_sort_") == -1:
                yield Request(url=tag, callback=self.tag_page_parse)

    def photo_parse(self, response):
        tags = re.findall(r'http://absfreepic\.com/free-photos/[^./]+.html', response.body.decode())
        for tag in tags:
            if tag.find("_sort_") == -1:
                yield Request(url=tag, callback=self.tag_page_parse)

        photos = re.findall(r'http://absfreepic\.com/free-photos/download/[^./]+.html', response.body.decode())
        for photo in photos:
            yield Request(url=photo, callback=self.photo_parse)

        origin_photo = \
        re.findall(r'href="(http://absfreepic\.com/absolutely_free_photos/original_photos/[^./]+.[^"]+)"',
                   response.body.decode())[0]
        title = re.findall(r'<h1 class="media-heading" >([^<]+)</h1>', response.body.decode())[0]
        head_title = response.xpath('//title/text()').extract_first()
        resolotion = re.findall(r'[\d]+x[\d]+', head_title)[0]
        file_size = re.findall(r' ([^ ]+)$', head_title)[0]
        tags = ""
        for tag in re.findall(r'<a class=\'tag\' href=/free-photos/([^./]+).html >', response.body.decode()):
            tags = tags + tag + " "

        filename = \
        re.findall(r'http://absfreepic\.com/absolutely_free_photos/original_photos/([^./]+.[^"]+)$', origin_photo)[0]
        filename = "absfreepic-" + filename
        if not r.sismember("downloaded", filename):
            yield Request(url=origin_photo, callback=lambda
                response,
                origin_photo=origin_photo,
                title=title,
                resolotion=resolotion,
                file_size=file_size,
                tags=tags: self.photo_save(response, origin_photo, title, resolotion, file_size, tags))

    def photo_save(self, response, origin_photo, title, resolotion, file_size, tags):
        filename = \
        re.findall(r'http://absfreepic\.com/absolutely_free_photos/original_photos/([^./]+.[^"]+)$', response.url)[0]
        filename = "absfreepic-" + filename
        fileHandle = open(self.save_path + filename, 'wb')
        fileHandle.write(response.body)
        fileHandle.close()

        r.sadd("downloaded", filename)

        photo_info = {
            "origin_photo": origin_photo,
            "filename": filename,
            "title": title,
            "resolotion": resolotion,
            "file_size": file_size,
            "tags": tags,
        }

        r.hmset("absfreepic:" + filename, photo_info)
