import requests
import time
import random
from hashlib import md5

class YdSpider(object):
  def __init__(self):
    # url一定为F12抓到的 headers -> General -> Request URL
    self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    self.headers = {
      # 检查频率最高 - 3个
      "Cookie": "OUTFOX_SEARCH_USER_ID=970246104@10.169.0.83; OUTFOX_SEARCH_USER_ID_NCOO=570559528.1224236; _ntes_nnid=96bc13a2f5ce64962adfd6a278467214,1551873108952; JSESSIONID=aaae9i7plXPlKaJH_gkYw; td_cookie=18446744072941336803; SESSION_FROM_COOKIE=unknown; ___rl__test__cookies=1565689460872",
      "Referer": "http://fanyi.youdao.com/",
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
    }

  # 获取salt,sign,ts
  def get_salt_sign_ts(self,word):
    # ts
    ts = str(int(time.time()*1000))
    # salt
    salt = ts + str(random.randint(0,9))
    # sign
    string = "fanyideskweb" + word + salt + "n%A-rKaT5fb[Gy?;N5@Tj"
    s = md5()
    s.update(string.encode())
    sign = s.hexdigest()

    return salt,sign,ts

  # 主函数
  def attack_yd(self,word):
    # 1. 先拿到salt,sign,ts
    salt,sign,ts = self.get_salt_sign_ts(word)
    # 2. 定义form表单数据为字典: data={}
    # 检查了salt sign
    data = {
      "i": word,
      "from": "AUTO",
      "to": "AUTO",
      "smartresult": "dict",
      "client": "fanyideskweb",
      "salt": salt,
      "sign": sign,
      "ts": ts,
      "bv": "7e3150ecbdf9de52dc355751b074cf60",
      "doctype": "json",
      "version": "2.1",
      "keyfrom": "fanyi.web",
      "action": "FY_BY_REALTlME",
    }
    # 3. 直接发请求:requests.post(url,data=data,headers=xxx)
    res = requests.post(
      url=self.url,
      data=data,
      headers=self.headers
    )
    # res.json() 将json格式的字符串转为python数据类型
    html = res.json()
    # html:{'translateResult': [[{'tgt': '你好', 'src': 'hello'}]], 'errorCode': 0, 'type': 'en2zh-CHS', 'smartResult': {'entries': ['', 'n. 表示问候， 惊奇或唤起注意时的用语\r\n', 'int. 喂；哈罗\r\n', 'n. (Hello)人名；(法)埃洛\r\n'], 'type': 1}}
    result = html['translateResult'][0][0]['tgt']

    print(result)

  # 主函数
  def main(self):
    # 输入翻译单词
    word = input('请输入要翻译的单词:')
    self.attack_yd(word)

if __name__ == '__main__':
  spider = YdSpider()
  spider.main()