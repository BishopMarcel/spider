import requests
from lxml import etree
import time
import random
from useragents import ua_list

class LianjiaSpider(object):
  def __init__(self):
    self.url='https://bj.lianjia.com/ershoufang/pg{}/'
    self.blog = 1

  def get_html(self,url):
    headers = {'User-Agent':random.choice(ua_list)}
    # 尝试3次,否则换下一页地址
    if self.blog <= 3:
      try:
        res = requests.get(url=url,headers=headers,timeout=5)
        res.encoding = 'utf-8'
        html = res.text
        # 直接调用解析函数
        self.parse_page(html)
      except Exception as e:
        print('Retry')
        self.blog += 1
        self.get_html(url)


  def parse_page(self,html):
    parse_html = etree.HTML(html)
    # li_list: [<element li at xxx>,<element li at xxx>]
    li_list = parse_html.xpath('//ul[@class="sellListContent"]/li[@class="clear LOGVIEWDATA LOGCLICKDATA"]')
    item = {}
    for li in li_list:
      # 名称
      xpath_name = './/a[@data-el="region"]/text()'
      name_list = li.xpath(xpath_name)
      item['name'] = [
        name_list[0].strip() if name_list else None
      ][0]
      # 户型+面积+方位+是否精装
      info_xpath = './/div[@class="houseInfo"]/text()'
      info_list = li.xpath(info_xpath)
      if info_list:
        info_list = info_list[0].strip().split('|')
        if len(info_list) == 5:
          item['model'] = info_list[1].strip()
          item['area'] = info_list[2].strip()
          item['direction'] = info_list[3].strip()
          item['perfect'] = info_list[4].strip()
        else:
          item['model']=item['area']=item['direction']=item['perfect']=None
      else:
        item['model'] = item['area'] = item['direction'] = item['perfect'] = None

      # 楼层
      xpath_floor = './/div[@class="positionInfo"]/text()'
      floor_list = li.xpath(xpath_floor)
      item['floor'] = [
        floor_list[0].strip().split()[0] if floor_list else None
      ][0]

      # 地区
      xpath_address = './/div[@class="positionInfo"]/a/text()'
      address_list = li.xpath(xpath_address)
      item['address'] = [
        address_list[0].strip() if address_list else None
      ][0]
      # 总价
      xpath_total = './/div[@class="totalPrice"]/span/text()'
      total_list = li.xpath(xpath_total)
      item['total_price'] = [
        total_list[0].strip() if total_list else None
      ][0]
      # 单价
      xpath_unit = './/div[@class="unitPrice"]/span/text()'
      unit_list = li.xpath(xpath_unit)
      item['unit_price'] = [
        unit_list[0].strip() if unit_list else None
      ][0]

      print(item)

  def main(self):
    for pg in range(1,101):
      url = self.url.format(pg)
      self.get_html(url)
      time.sleep(random.randint(1,3))
      # 对self.blog进行一下初始化
      self.blog = 1


if __name__ == '__main__':
  start = time.time()
  spider = LianjiaSpider()
  spider.main()
  end = time.time()
  print('执行时间:%.2f' % (end-start))