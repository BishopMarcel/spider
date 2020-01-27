import requests
import json
import time
import random
from useragents import ua_list

class TencentSpider(object)
  def __init__(self)
    self.one_url = 'httpscareers.tencent.comtencentcareerapipostQuerytimestamp=1563912271089&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=&pageIndex={}&pageSize=10&language=zh-cn&area=cn'
    self.two_url = 'httpscareers.tencent.comtencentcareerapipostByPostIdtimestamp=1563912374645&postId={}&language=zh-cn'
    # 打开文件
    self.f = open('tencent.json','a')
    # 存放抓取的item字典数据
    self.item_list = []

  # 获取响应内容函数
  def get_page(self,url)
    headers = {'User-Agent'random.choice(ua_list)}
    html = requests.get(url=url,headers=headers).text
    # json格式字符串 - Python
    html = json.loads(html)

    return html

  # 主线函数 获取所有数据
  def parse_page(self,one_url)
    html = self.get_page(one_url)
    item = {}
    for job in html['Data']['Posts']
      # postId
      post_id = job['PostId']
      # 拼接二级地址,获取职责和要求
      two_url = self.two_url.format(post_id)
      item['name'],item['duty'],item['require'] = self.parse_two_page(two_url)

      print(item)
      # 添加到大列表中
      self.item_list.append(item)

  # 解析二级页面函数
  def parse_two_page(self,two_url)
    html = self.get_page(two_url)
    # 职位名称
    name = html['Data']['RecruitPostName']
    # 用replace处理一下特殊字符
    duty = html['Data']['Responsibility']
    duty = duty.replace('rn','').replace('n','')
    # 处理要求
    require = html['Data']['Requirement']
    require = require.replace('rn','').replace('n','')

    return name,duty,require

  # 获取总页数
  def get_numbers(self)
    url = self.one_url.format(1)
    html = self.get_page(url)
    numbers = int(html['Data']['Count'])  10 + 1

    return numbers

  def main(self)
    number = self.get_numbers()
    for page in range(1,3)
      one_url = self.one_url.format(page)
      self.parse_page(one_url)

    # 保存到本地json文件json.dump
    json.dump(self.item_list,self.f,ensure_ascii=False)
    self.f.close()

if __name__ == '__main__'
  spider = TencentSpider()
  spider.main()