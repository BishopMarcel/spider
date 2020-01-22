import requests
from lxml import etree
import time
import random
from useragents import ua_list

class MaoyanSpider(object):
  def __init__(self):
    self.url = 'https://maoyan.com/board/4?offset={}'
    # 计数
    self.num = 0
    self.blag = 1

  def get_html(self,url):
    headers = {
      'User-Agent' : random.choice(ua_list)
    }
    if self.blag <= 3:
      try:
        res = requests.get(url=url,headers=headers,timeout=3)
        res.encoding = 'utf-8'
        html = res.text
        # 直接调用解析函数
        self.parse_html(html)
      except Exception as e:
        print('Retry')
        self.blag += 1
        self.get_html(url)


  def parse_html(self,html):
    # 此处用xpath实现 - 先基准xpath,再依次遍历
    parse_html = etree.HTML(html)
    base_xpath = '//dl[@class="board-wrapper"]/dd'
    dd_list = parse_html.xpath(base_xpath)
    item = {}
    if dd_list:
      for dd in dd_list:
        # 电影名称
        xpath_name = './/p[@class="name"]/a/@title'
        name_list = dd.xpath(xpath_name)
        item['name'] = [
          name_list[0].strip() if name_list else None
        ][0]
        # 主演
        xpath_star = './/p[@class="star"]/text()'
        star_list = dd.xpath(xpath_star)
        item['star'] = [
          star_list[0].strip() if star_list else None
        ][0]
        # 时间
        xpath_time = './/p[@class="releasetime"]/text()'
        time_list = dd.xpath(xpath_time)
        item['time'] = [
          time_list[0].strip() if time_list else None
        ][0]

        print(item)
    else:
      print('No dd_list')

  def main(self):
    for offset in range(0,31,10):
      url = self.url.format(offset)
      self.get_html(url)
      time.sleep(random.randint(1,2))
      # 重置标签
      self.blag = 1
    print('共抓取数据:',self.num)

if __name__ == '__main__':
  start = time.time()
  spider = MaoyanSpider()
  spider.main()
  end = time.time()
  print('执行时间:%.2f' % (end-start))