import urllib, re, random, time
import urllib.parse, requests
from bs4 import BeautifulSoup
import pandas as pd
import json, pymysql, sys, os
import socks, socket
import threading
from PIL import Image
import baidufanyi

connect = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='',
    db='magdeleine',
    charset='utf8'
)
cursor = connect.cursor()
mutex = threading.Lock()


class Magdeleine(threading.Thread):
    start_page = 1
    end_page = 50
    cursor = None

    def __init__(self, start_page=1, end_page=50):
        threading.Thread.__init__(self)
        self.start_page = start_page
        self.end_page = end_page + 1
        self.cursor = connect.cursor()

    def run(self):
        self.get_page()

    def get_html(self, url):
        headers = {
            'User-Agent': str(
                "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"),
        }
        req = urllib.request.Request("%s" % (url))
        for i in headers:
            req.add_header(i, headers[i])
        proxy_support = urllib.request.ProxyHandler({'sock5': 'localhost:1080'})
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
        attempts = 0
        success = False
        while attempts < 10 and not success:
            try:
                ws1 = urllib.request.urlopen(req, data=None, timeout=5).read()
                success = True
                return ws1.decode()
            except:
                print("超时重试：" + url)
                attempts += 1
        print("html获取失败：" + url)
        exit(1)

    def get_page(self):
        for i in range(self.start_page, self.end_page):
            if i == 1:
                html = self.get_html("https://magdeleine.co/browse/")
            else:
                page_url = "https://magdeleine.co/browse/page/{}/"
                page_url = page_url.format(i)
                html = self.get_html(page_url)
            self.get_item(html)

    def get_item(self, html):
        soup = BeautifulSoup(html, 'lxml')
        ss = soup.select('a.photo-link')

        for item in ss:
            page_url = item.get("href")
            if mutex.acquire():
                self.cursor.execute("select * from photos where `page_url`='%s'" % page_url)
                mutex.release()
            running_status = self.cursor.fetchone()
            if (running_status == None):
                # print("fetching " + page_url)
                self.get_photo(page_url)
                # else:
                #     print(page_url + "已抓取，跳过")

    def get_photo(self, url):
        html = self.get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        ss = soup.select('a.button.download')
        photo_url = ss[0].get("href")
        sss = soup.select("div.category-links a")
        category_arr = []
        for item in sss:
            if item.get("title").find("View all photos in") != -1:
                category_arr.append(item.text)
        ssss = soup.select("ul.category-links.tags > li")
        tags_arr = []
        for item in ssss:
            tags_arr.append(item.a.text)
        category_json = json.dumps(category_arr)
        tags_json = json.dumps(tags_arr)
        sql = "insert into photos (`page_url`,`photo_url`,`category`,`tags`,`created_at`) values ('%s','%s','%s','%s','%s')"
        category_json = connect.escape_string(category_json)
        tags_json = connect.escape_string(tags_json)
        sql = sql % (url, photo_url, category_json, tags_json, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        if mutex.acquire():
            self.cursor.execute(sql)
            connect.commit()
            mutex.release()

    def get_resolution(self, folder):
        self.cursor.execute("select * from photos")
        photos = self.cursor.fetchall()
        for item in photos:
            photo_url = item[2]
            pos = photo_url.rfind("/")
            file_name = photo_url[pos + 1:]
            img = Image.open(folder + "\\" + file_name)
            size = img.size
            sql = "update photos set `resolution` = '%s' where `id` = %s"

            sql = sql % (size, item[0])
            print(sql)
            self.cursor.execute(sql)
            connect.commit()

    def translate_category(self):
        self.cursor.execute("select * from photos")
        photos = self.cursor.fetchall()
        dict = {'People': '人物', 'Abstract': '抽象', 'Animals': '动物', 'Nature': '自然', 'Technology': '科学/技术', 'Food': '食物',
                'City & Architecture': '建筑', 'Objects': '物体', 'Sports': '运动', 'Macro': '宏伟的'}
        a = set()

        for item in photos:
            category_english = json.loads(item[4])
            # category_chinese = []
            category_chinese = ""
            for item2 in category_english:
                # category_chinese.append(dict[item2])
                category_chinese = dict[item2]
                a.add(item2)
            sql = "update photos set `chinese_category` = '%s' where `id` = %s"
            sql = sql % (category_chinese, item[0])
            print(sql)
            self.cursor.execute(sql)
            connect.commit()
        print(a)

    def translate_tags(self):
        baidufanyi.addlist()
        baidufanyi.save_db()

    def export_photo_address_list(self):
        sql = "select * from photos"
        cursor.execute(sql)
        photos = cursor.fetchall()
        for item in photos:
            print(item[2])


if __name__ == "__main__":
    print(1)
