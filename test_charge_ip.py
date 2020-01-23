# 获取开放代理的接口
import requests

def test_ip(ip):
    url = 'http://www.baidu.com/'
    proxies = {     
        'http':'http://{}'.format(ip),
        'https':'https://{}'.format(ip),
    }
    
    try:
    	res = requests.get(url=url,proxies=proxies,timeout=8 )
    	if res.status_code == 200:
        	return True
    except Exception as e:
        return False

# 提取代理IP
def get_ip_list():
  api_url = 'http://dev.kdlapi.com/api/getproxy/?orderid=946562662041898&num=100&protocol=1&method=2&an_an=1&an_ha=1&sep=2'
  html = requests.get(api_url).content.decode('utf-8','ignore')
  # ip_port_list: ['IP:PORT','IP:PORT','']
  ip_port_list = html.split('\r\n')

  # 依次遍历代理IP,并进行测试
  for ip in ip_port_list:
    with open('proxy_ip.txt','a') as f:
    	if test_ip(ip):
            f.write(ip + '\n')

if __name__ == '__main__':
    get_ip_list()