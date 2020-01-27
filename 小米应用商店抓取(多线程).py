import requests
from fake_useragent import UserAgent
from threading import Thread
from queue import Queue
import time
from lxml import etree
import pymysql
import random
from threading import Lock
import math


class XiaoMiSpider(object):
    def __init__(self):
        self.base_url = 'http://app.mi.com/'
        self.type_url = 'http://app.mi.com/categotyAllListApi?page={}&categoryId={}&pageSize=30'
        self.q = Queue()  # 创建队列
        self.ua = UserAgent()
        self.i = 0
        self.app_type_list_info = []
        self.conn = pymysql.connect('127.0.0.1', '用户名', '密码', 'xm_db', charset='utf8mb4')
        self.cursor = self.conn.cursor()
        self.lock = Lock()  # 创建锁

    def get_type_info(self):
        headers = {'User-Agent': self.ua.random}
        html = requests.get(self.base_url, headers=headers).text
        parse_html = etree.HTML(html)
        base_info = parse_html.xpath('//div[@class="sidebar"]/div[2]/ul/li')
        for info in base_info:
            category_id = info.xpath('./a/@href')[0].split('/')[-1]
            app_count = self.get_app_num(category_id)
            self.app_type_list_info.append((category_id, app_count))
        print('app类型列表抓取完毕!')
        self.url_in()

    def get_app_num(self, category_id):
        url = self.type_url.format(0, category_id)
        headers = {'User-Agent': self.ua.random}
        html = requests.get(url, headers=headers).json()
        app_count = html['count']
        return app_count

    # URL入队列
    def url_in(self):
        for info in self.app_type_list_info:
            for page in range(math.ceil(int(info[1]) // 30)):
                url = self.type_url.format(page, info[0])
                self.q.put(url)

    # 线程事件type_id
    def get_data(self):
        while True:
            if not self.q.empty():
                url = self.q.get()
                headers = {'User-Agent': self.ua.random}
                html = requests.get(url, headers=headers).json()
                self.parse_html(html)
            else:
                break

    def parse_html(self, html):
        app_list = []
        time.sleep(2)
        for info in html['data']:
            app_name = info['displayName']
            app_link = 'http://app.mi.com/details?id=' + info['packageName']
            app_type = info['level1CategoryName']
            app_list.append([app_type, app_name, app_link])
            self.i += 1
            print(f'{app_name}抓取完毕')
        self.save_to_file(app_list)
        time.sleep(random.randint(1, 3))

    def save_to_file(self, app_list):
        self.lock.acquire()
        ins = 'insert into app_info (app_type, app_name, app_link) values (%s,%s,%s)'
        try:
            self.cursor.executemany(ins, app_list)
        except Exception as e:
            print('error', e)
        self.lock.release()

    def main(self):
        self.get_type_info()
        t_list = []
        for i in range(3):
            t = Thread(target=self.get_data)
            t_list.append(t)
            t.start()

        for t in t_list:
            t.join()
        print(f'共{self.i}条数据')
        self.conn.commit()
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    start_time = time.time()
    spider = XiaoMiSpider()
    spider.main()
    end_time = time.time()
    print(f'执行时间{(end_time - start_time)}s')
    
