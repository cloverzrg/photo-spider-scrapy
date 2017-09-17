import urllib, random
import urllib.parse, requests
import json
import hashlib

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
            self.chinese = k['trans_result']['data'][0]['dst']
            return  True
        except:
            print( "error:" + self.keyword + ":" + html)
            return  False
        return self.chinese

    def get_url(self):
        url = "http://fanyi.baidu.com/v2transapi?from=en&to=zh&query={}"
        url = url.format(urllib.parse.quote(self.keyword))
        return url
