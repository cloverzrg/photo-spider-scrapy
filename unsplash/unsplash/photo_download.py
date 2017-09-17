import redis,re,threadpool,requests


myproxy = dict(http='socks5://127.0.0.1:1080',https='socks5://127.0.0.1:1080')
save_path = "D:\\visualhunt\\origin\\"


r = redis.Redis(host='127.0.0.1', port=6379, db=1)

def photo_download(url,id,ext = "jpg"):
    response = requests.get(url=url,proxies=myproxy,timeout=180)
    fileHandle = open(save_path + "visualhunt-" + id + "." + ext, 'wb')
    fileHandle.write(response.content)
    fileHandle.close()
    r.hset("visualhunt:" + id, "downloaded", 1)

photos = r.keys("visualhunt:*")
download_list = []
i=0
for key in photos:
    value = r.hgetall(key)
    id = re.findall(r'([\d]+)', key.decode())[0]
    try:
        temp = value['downloaded'.encode()].decode()
        #已下载
    except:
        #未下载
        url = value['download_url'.encode()].decode()
        ext = re.findall(r'\.([^.]+)$', url)[0]
        item = []
        item.append(url)
        item.append(id)
        item.append(ext)
        i=i+1
        if i>20:
            break
        download_list.append((item, None))

pool = threadpool.ThreadPool(4)

work_list = threadpool.makeRequests(photo_download, download_list)
for req in work_list:
    pool.putRequest(req)
pool.wait()