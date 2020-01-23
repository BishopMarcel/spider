import requests
from lxml import etree
import re
import pymysql

class GovementSpider(object):
  def __init__(self):
    self.url = 'http://www.mca.gov.cn/article/sj/xzqh/2019/'
    self.headers = {'User-Agent':'Mozilla/5.0'}
    # 创建2个对象
    self.db = pymysql.connect(
      '127.0.0.1','root','123456','govdb',charset='utf8'
    )
    self.cursor = self.db.cursor()

  # 获取假链接
  def get_false_link(self):
    html = requests.get(
      url = self.url,
      headers = self.headers
    ).text
    # 解析
    parse_html = etree.HTML(html)
    # a_list: [<element a at xx>,<element a at xxx>]
    a_list = parse_html.xpath('//a[@class="artitlelist"]')
    for a in a_list:
      # get()方法:获取某个属性的值
      title = a.get('title')
      if title.endswith('代码'):
        false_link = 'http://www.mca.gov.cn' + a.get('href')
        break

    self.incr_spider(false_link)

  # 增量爬取函数
  def incr_spider(self,false_link):
    sel = 'select url from version where url=%s'
    self.cursor.execute(sel,[false_link])
    # fetchall: (('http://xxxx.html',),)
    result = self.cursor.fetchall()
    # not result:代表数据库version表中无数据
    if not result:
      self.get_true_link(false_link)
      # 可选操作: 数据库version表中只保留最新1条数据
      dele = 'delete from version'
      self.cursor.execute(dele)
      # 把爬取后的url插入到version表中
      ins = 'insert into version values(%s)'
      self.cursor.execute(ins,[false_link])
      self.db.commit()
    else:
      print('数据已是最新,无须爬取')

  # 获取真链接
  def get_true_link(self,false_link):
    # 先获取假链接的响应,然后根据响应获取真链接
    html = requests.get(
      url = false_link,
      headers = self.headers
    ).text
    # 利用正则提取真实链接
    re_bds = r'window.location.href="(.*?)"'
    pattern = re.compile(re_bds,re.S)
    true_link = pattern.findall(html)[0]

    self.save_data(true_link)

  # 数据提取
  def save_data(self,true_link):
    html = requests.get(
      url = true_link,
      headers = self.headers
    ).text

    # xpath提取数据
    parse_html = etree.HTML(html)
    tr_list = parse_html.xpath('//tr[@height="19"]')
    for tr in tr_list:
      code = tr.xpath('./td[2]/text()')[0].strip()
      name = tr.xpath('./td[3]/text()')[0].strip()

      print(name,code)


  # 主函数
  def main(self):
    self.get_false_link()

if __name__ == '__main__':
  spider = GovementSpider()
  spider.main()