from PIL import Image,ImageFile
import os
import glob, threadpool, threading

Image.MAX_IMAGE_PIXELS = None
ImageFile.LOAD_TRUNCATED_IMAGES = True

mutex = threading.Lock()


def make_thumb(path, thumb_path, i):
    try:
        img = Image.open(path)
    except:
        print(path + ":打开失败")
        return
    ori_width, ori_height = img.size
    bili = ori_width / ori_height
    merge_width = 0
    merge_height = 0
    if bili >= 1.54:
        width = ori_height * 1.53
        height = ori_height
        merge_width = (ori_width - width) / 2
    elif bili < 1.54:
        width = ori_width
        height = ori_width / 1.53
        merge_height = (ori_height - height) / 2

    box = (int(merge_width), int(merge_height), int(merge_width + width), int(merge_height + height))

    region = img.crop(box)
    # 裁剪
    thumb = region.resize((800, 520), Image.ANTIALIAS)
    # 缩小
    base, ext = os.path.splitext(os.path.basename(path))

    filename = base + '-thumb.jpg'
    filepath = os.path.join(thumb_path, filename)

    thumb = thumb.convert('RGB')
    thumb.save(filepath, quality=96)
    print(str(i) + ': ' + filename + '   done!')


ROOT_PATH = os.path.abspath(os.path.dirname("D:\\test\\"))
IMG_PATH = os.path.join(ROOT_PATH, 'origin')
THUMB_PATH = os.path.join(ROOT_PATH, 'thumb')

if not os.path.exists(THUMB_PATH):
    os.makedirs(THUMB_PATH)

files = glob.glob(os.path.join(IMG_PATH, '*.*'))
i = 0
list = []
for file in files:
    base_name = os.path.basename(file)
    base, ext = os.path.splitext(base_name)
    filename = base + '-thumb.jpg'
    filepath = os.path.join(THUMB_PATH, filename)
    if os.path.exists(filepath) == True:
        # 已存在缩略图的话就不用重新生成了
        continue

    i = i + 1
    item2 = []
    item2.append(file)
    item2.append(THUMB_PATH)
    item2.append(i)
    list.append((item2, None))

pool = threadpool.ThreadPool(4)

requests = threadpool.makeRequests(make_thumb, list)
for req in requests:
    pool.putRequest(req)
pool.wait()
