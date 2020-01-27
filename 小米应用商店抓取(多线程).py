import requests
from threading import Thread
from queue import Queue
import time
from useragents import ua_list
from lxml import etree
import csv
from threading import Lock
import random

class XiaomiSpider(object):
  def __init__(self):
    self.url = 'http://app.mi.com/categotyAllListApi?page={}&categoryId={}&pageSize=30'
    # 存放所有URL地址的队列
    self.q = Queue()
    self.i = 0
    # 存放所有类型id的空列表
    self.id_list = []
    # 打开文件
    self.f = open('xiaomi.csv','a')
    self.writer = csv.writer(self.f)
    # 创建锁
    self.lock = Lock()


  def get_cateid(self):
    # 请求
    url = 'http://app.mi.com/'
    headers = { 'User-Agent': random.choice(ua_list)}
    print(headers)
    html = requests.get(url=url,headers=headers).text
    # 解析
    parse_html = etree.HTML(html)
    xpath_bds = '//ul[@class="category-list"]/li'
    li_list = parse_html.xpath(xpath_bds)
    for li in li_list:
      typ_name = li.xpath('./a/text()')[0]
      typ_id = li.xpath('./a/@href')[0].split('/')[-1]
      # 计算每个类型的页数
      pages = self.get_pages(typ_id)
      self.id_list.append( (typ_id,pages) )

    # 入队列
    self.url_in()

  # 获取counts的值并计算页数
  def get_pages(self,typ_id):
    # 每页返回的json数据中,都有count这个key
    url = self.url.format(0,typ_id)
    html = requests.get(
      url=url,
      headers={'User-Agent':random.choice(ua_list)}
    ).json()
    count = html['count']
    pages = int(count) // 30 + 1

    return pages

  # url入队列
  def url_in(self):
    for id in self.id_list:
      # id为元组,('2',pages)
      for page in range(2):
        url = self.url.format(page,id[0])
        # 把URL地址入队列
        self.q.put(url)

  # 线程事件函数: get() - 请求 - 解析 - 处理数据
  def get_data(self):
    while True:
      if not self.q.empty():
        url = self.q.get()
        headers = {'User-Agent':random.choice(ua_list)}
        html = requests.get(url=url,headers=headers).json()
        self.parse_html(html)
      else:
        break

  # 解析函数
  def parse_html(self,html):
    # 存放1页的数据 - 写入到csv文件
    app_list = []

    for app in html['data']:
      # 应用名称 + 链接 + 分类
      name = app['displayName']
      link = 'http://app.mi.com/details?id=' + \
             app['packageName']
      typ_name = app['level1CategoryName']
      # 把每一条数据放到app_list中,目的为了 writerows()
      app_list.append([name,typ_name,link])

      print(name,typ_name)
      self.i += 1

    # 开始写入1页数据 - app_list
    self.lock.acquire()
    self.writer.writerows(app_list)
    self.lock.release()

  # 主函数
  def main(self):
    # URL入队列
    self.get_cateid()
    t_list = []
    # 创建多个线程
    for i in range(1):
      t = Thread(target=self.get_data)
      t_list.append(t)
      t.start()

    # 回收线程
    for t in t_list:
      t.join()

    # 关闭文件
    self.f.close()
    print('数量:',self.i)

if __name__ == '__main__':
  start = time.time()
  spider = XiaomiSpider()
  spider.main()
  end = time.time()
  print('执行时间:%.2f' % (end-start))