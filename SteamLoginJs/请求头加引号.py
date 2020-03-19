'''
使用正则表达式将headers转换成python字典格式的工具函数
'''

import re


headers_str = """
Host: store.steampowered.com
Origin: https://store.steampowered.com
Pragma: no-cache
Referer: https://store.steampowered.com/login/?redir=&redir_ssl=1
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36
X-Requested-With: XMLHttpRequest
"""

pattern = '^(.*?): (.*?)$'

for line in headers_str.splitlines():
    print(re.sub(pattern,'\'\\1\': \'\\2\',',line))