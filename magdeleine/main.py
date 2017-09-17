import magdeleine
import baidufanyi
import threadpool
import pymysql

connect = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='',
    db='magdeleine',
    charset='utf8'
)
cursor = connect.cursor()


class MagdeleineController:
    # def __init__(self):
    #     print("start")

    def create_table(self):
        sql = "CREATE TABLE `photos` ( `id` int(11) NOT NULL AUTO_INCREMENT,  `page_url` varchar(255) NOT NULL,`photo_url` varchar(255) NOT NULL, `resolution` char(20) DEFAULT NULL, `category` varchar(255) DEFAULT NULL,`tags` varchar(255) DEFAULT NULL,`chinese_category` varchar(255) DEFAULT NULL,`chinese_tags` varchar(255) DEFAULT NULL,`created_at` datetime NOT NULL,PRIMARY KEY (`id`) ) ENGINE=InnoDB AUTO_INCREMENT=1225 DEFAULT CHARSET=utf8;"
        cursor.execute(sql)
        connect.commit()
        print("done")

    def translate_category(self):
        spider = Magdeleine.Magdeleine(1, 10)
        spider.translate_category()

    def translate_tags(self):
        spider = Magdeleine.Magdeleine(1, 10)
        spider.translate_tags()

    def get_resolution(self, folder):
        spider = Magdeleine.Magdeleine(1, 10)
        spider.get_resolution(folder)

    def export_photo_address_list(self):
        spider = Magdeleine.Magdeleine(1, 10)
        spider.export_photo_address_list()

    def test(self, page):
        spider = Magdeleine.Magdeleine(page, page)
        spider.run()

    def start(self, start_page=1, end_page=50, thread_count=30):
        pool = threadpool.ThreadPool(thread_count)
        requests = threadpool.makeRequests(self.test, range(start_page, end_page))
        for req in requests:
            pool.putRequest(req)
        pool.wait()


controller = MagdeleineController()
# 在数据库中生成表格
# controller.create_table()
# 抓取图片信息，包括下载地址、类别、标签，三个参数，分别为开始page，结束page，抓取线程数
controller.start(1, 116, 25)
# 导出下载地址列表，用于在迅雷中下载
# controller.export_photo_address_list()
# 获取分辨率，传入一个参数，为下载的图片的目录
# controller.get_resolution("D:\迅雷下载\photo")
# 把类别翻译成中文
# controller.translate_category()
# 把标签翻译成中文
# controller.translate_tags()
