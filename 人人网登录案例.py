# 1、将self.url改为 个人主页的URL地址
# 2、将Cookie的值改为 登录成功的Cookie值
import requests
from lxml import etree

class RenrenLogin(object):
  def __init__(self):
    self.url = 'xxxxxxx'
    self.headers = {
      'Cookie':'xxxxxx',
      'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    }

  def get_html(self):
    html = requests.get(url=self.url,headers=self.headers).text
    self.parse_html(html)

  def parse_html(self,html):
    parse_html = etree.HTML(html)
    r_list = parse_html.xpath('//*[@id="operate_area"]/div[1]/ul/li[1]/span/text()')
    print(r_list)

if __name__ == '__main__':
  spider = RenrenLogin()
  spider.get_html()