import time
import execjs
import requests

username = input('请输入steam用户名：')
password = input('请输入steam密码：')
headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
'Host': 'store.steampowered.com',
'Origin': 'https://store.steampowered.com',
'Pragma': 'no-cache',
'Referer': 'https://store.steampowered.com/login/?redir=&redir_ssl=1',
'Sec-Fetch-Dest': 'empty',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Site': 'same-origin',
'X-Requested-With': 'XMLHttpRequest',
}


session = requests.session()
donotcache = int(time.time()*1000)

form_data = {
    'donotcache':donotcache,
    'username':username
}
response = session.post(url='https://store.steampowered.com/login/getrsakey/',data=form_data,headers=headers).json()

publickey_mod = response['publickey_mod']
publickey_exp = response['publickey_exp']
timestamp = response['timestamp']
# token_gid = response['token_gid']


with open(r'steam_login.js',encoding='gbk') as f:
    JsData = f.read()
pwd = execjs.compile(JsData).call('test',username,publickey_mod,publickey_exp)


data = {
'donotcache':int(time.time()*1000),
'password':pwd,
'username':username,
'twofactorcode':'',
'emailauth':'',
'loginfriendlyname':'',
'captchagid':'-1',
'captcha_text':'',
'emailsteamid':'',
'rsatimestamp':timestamp,
'remember_login':'false',
}

response = session.post(url='https://store.steampowered.com/login/dologin/',data=data,headers=headers).json()
print(response['message'])

# The account name or password that you have entered is incorrect.
# Please verify your humanity by re-entering the characters in the captcha.
# There have been too many login failures from your network in a short time period.  Please wait and try again later.