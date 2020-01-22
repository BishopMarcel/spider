import os

import requests,random,time,re
from fake_useragent import UserAgent
from lxml import etree
from multiprocessing import Process



class Car:
    def __init__(self):
        self.url = 'http://hsck8.com/vodtype/2-{}.html'
        self.title = ''
        self.i = 0

    def get_html(self,url):
        headers = {'User-Agent':UserAgent().random}
        html = requests.get(url=url,headers=headers).text
        return html

    def parse_html(self,html):
        p = etree.HTML(html)
        bds = '//li/div/a[@class="stui-vodlist__thumb lazyload"]/@href'
        r_list = p.xpath(bds)
        href_list = []
        for r in r_list:
            href = 'http://hsck8.com' + r
            href_list.append(href)
            self.i += 1
            time.sleep(random.uniform(1,3))

            print('正在抓取第{}个{}网址数据'.format(self.i,href))
            html = self.get_html(href)

            p = etree.HTML(html)
            self.title = p.xpath('/html/body/div[2]/div/div[2]/div[1]/div[1]/h3/text()')[0].strip()

            m3u8 = self.re_parse_html(html)

            m3u8 = ''.join(m3u8.split('\\'))
            print('正在下载解析{}文件'.format(m3u8))

            data = requests.get(url=m3u8,headers={'User-Agent':UserAgent().random}).text
            #通过正则表达式获取ts的url
            p = re.compile(r',(.*?)#EXT',re.S)
            ts_list = p.findall(data)
            # print(ts_list)
            m3u8_href = m3u8.split('index.m3u8')[0]
            ts_href_list = []
            for ts in ts_list:
                ts_href = m3u8_href + ts.strip()
                ts_href_list.append(ts_href)
            # print(ts_href_list)

            # print(self.title)
            filename = 'H:\\spider\\'+ self.title+ '.mp4'
            # print(filename)
            num  = 0
            with open(filename,'wb') as f:
                start = time.time()
                for ts_link in ts_href_list:
                    data = self.handle(ts_link)
                    f.write(data)
                    num += 1
                    # /r 指定行第一个字符开始，搭配end属性完成覆盖进度条
                    print('\r'+'[下载进度]：%s%.2f%%'%('>'*int(num/len(ts_href_list)*100),num/len(ts_href_list)*100),end='')
                end = time.time()
                print('\n'+'下载完成！用时%.2f秒'%(end-start))


    def handle(self,url):
        data = requests.get(url=url,headers={'User-Agent':UserAgent().random}).content
        return data


    def re_parse_html(self,html):
        re_bds = '''<script type="text/javascript">.*?"url":"(.*?)",.*?</script>'''
        p = re.compile(re_bds, re.S)
        result = p.findall(html)
        #['http:\\/\\/c1.ckcdn2000.com:12345\\/video\\/m3u8\\/2019\\/12\\/28\\/0ac55f2a\\/index.m3u8']
        m3u8 = result[0]
        return m3u8


        # print(href_list)



    def write_html(self):
        pass

    def run(self):
        for page in range(1,7):
            url = self.url.format(page)
            html = self.get_html(url)
            self.parse_html(html)
            time.sleep(random.uniform(1,3))

if __name__ == '__main__':
    car = Car()
    car.run()