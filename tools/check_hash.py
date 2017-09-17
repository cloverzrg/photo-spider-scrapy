import os,glob,shutil,threadpool,re
from qiniu import Auth
from qiniu import BucketManager
from tools import qetag

def check_exist(file):
    access_key = ''
    secret_key = ''
    # 初始化Auth状态
    q = Auth(access_key, secret_key)
    # 初始化BucketManager
    bucket = BucketManager(q)
    # 你要测试的空间， 并且这个key在你空间中存在
    bucket_name = ''
    key = file
    # 获取文件的状态信息
    ret, info = bucket.stat(bucket_name, key)
    if info.status_code == 200:
        hash = re.findall(r'"hash":"([^"]+)",',info.text_body)[0]
        return hash
    else:
        return False


def check_exist2(file,i):
    key = "abay_api" + file.replace(ROOT_PATH, "").replace("\\", "/")
    status = check_exist(key)
    if status is not False:
        hash = qetag.get_qetag(file)
        if hash == status:
            print(file + ":hash正确")
        else:
            print("hash不正确")
            shutil.move(file, file.replace(ROOT_PATH, UPLOAD_SUCCESS_PATH))


ROOT_PATH = os.path.abspath(os.path.dirname("D:\\photock\\"))
UPLOAD_SUCCESS_PATH = os.path.abspath(os.path.dirname("D:\\uploaded\\"))
IMG_PATH = os.path.join(ROOT_PATH, 'origin')
BIGIMG_PATH = os.path.join(ROOT_PATH, 'thumb')
files = glob.glob(os.path.join(IMG_PATH, '*'))
files2 = glob.glob(os.path.join(BIGIMG_PATH, '*'))
files.extend(files2)

list = []
i=0
for file in files:
    i = i + 1
    item2 = []
    item2.append(file)
    item2.append(i)
    list.append((item2, None))

pool = threadpool.ThreadPool(10)

requests = threadpool.makeRequests(check_exist2, list)
for req in requests:
    pool.putRequest(req)
pool.wait()
