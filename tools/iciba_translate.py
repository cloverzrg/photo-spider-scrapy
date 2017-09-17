import urllib, re
import urllib.parse, requests
import json


class IcibaTranslate():
    keyword = ""
    chinese = ""

    def __init__(self, keyword):
        self.keyword = keyword
        self.__translate()

    def __get_html(self, url):
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

    def __translate(self):
        url = self.__get_url()
        html = self.__get_html(url)
        if html.find("未找到结果") != -1:
            return  False
        p=html.find("<br><br>")
        html = html[p:]
        html = html.replace("返回查词首页","")
        try:
            print(re.findall(r'[\u4e00-\u9fa5]+',html))
            self.chinese = re.findall(r'[\u4e00-\u9fa5]+',html)[0]
            return True
        except:
            print("error:" + self.keyword + ":" + html)
            return False

    def __get_url(self):
        url = "http://dict-co.iciba.com/search.php?word={}"
        url = url.format(urllib.parse.quote(self.keyword))
        return url

if __name__ == "__main__":
    k=IcibaTranslate("A  pleasant surprise is in store for you")
    print(k.chinese)