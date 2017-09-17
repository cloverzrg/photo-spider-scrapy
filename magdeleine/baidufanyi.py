import urllib, re, random, time
import urllib.parse, requests
from bs4 import BeautifulSoup
import pandas as pd
import json, pymysql, sys, os
import socks, socket
import threading
import hashlib, threadpool

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
mutex2 = threading.Lock()
chinese = {}


class BaiduFanyi():
    keyword = ""
    chinese = ""
    def __init__(self, keyword):
        self.keyword = keyword

    def get_html(self, url):
        headers = {
            'User-Agent': str(
                "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"),
        }
        req = urllib.request.Request("%s" % (url))
        for i in headers:
            req.add_header(i, headers[i])
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
        exit(1)

    def translate(self):
        url = self.get_url()
        html = self.get_html(url)
        k = json.loads(html)
        try:
            self.chinese = k['trans_result'][0]['dst']
        except:
            print( "error:" + self.keyword + ":" + html)
        return self.chinese

    def get_url(self):
        appid = ""
        secretKey = ''
        url = "http://api.fanyi.baidu.com/api/trans/vip/translate?q={}&from=en&to=zh&appid={}&salt={}&sign={}"
        salt = random.randint(32768, 65536)
        sign = appid + self.keyword + str(salt) + secretKey
        m1 = hashlib.md5()
        m1.update(sign.encode("utf-8"))
        sign = m1.hexdigest()
        url = url.format(urllib.parse.quote(self.keyword), appid, salt, sign)
        return url


def translate(keyword):
    global chinese
    baidu_translater = BaiduFanyi(keyword)
    baidu_translater.translate()
    if mutex.acquire():
        chinese[keyword] = baidu_translater.chinese
        mutex.release()
    return

    sql = "insert into translate (english,chinese) VALUES ('%s','%s')"
    sql = sql % (connect.escape_string(keyword), connect.escape_string(chinese_word))
    if mutex.acquire():
        cursor.execute(sql)
        connect.commit()
        mutex.release()


def addlist():
    sql = "select * from photos"
    cursor.execute(sql)
    photos = cursor.fetchall()
    translate_list = set()
    for item in photos:
        tags = json.loads(item[5])
        for item2 in tags:
            translate_list.add(item2)
    pool = threadpool.ThreadPool(50)
    requests = threadpool.makeRequests(translate, translate_list)
    for req in requests:
        pool.putRequest(req)
    pool.wait()


def save_db():
    global chinese
    sql = "select * from photos"
    cursor.execute(sql)
    photos = cursor.fetchall()
    for item in photos:
        tags = json.loads(item[5])
        tags_string = ""
        for item2 in tags:
            try:
                tags_string = tags_string + chinese[item2] + " "
            except:
                print("error:" + item2)
        sql = "update photos set `chinese_tags` = '%s' where `id` = %s"
        sql = sql % (tags_string, item[0])
        print(sql)
        cursor.execute(sql)
        connect.commit()

if __name__ == "__main__":
    addlist()
    save_db()