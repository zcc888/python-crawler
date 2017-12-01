import requests
from bs4 import BeautifulSoup

User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
header = {}
header['User-Agent'] = User_Agent

url = 'http://www.xicidaili.com/nn/1'
resp = requests.get(url,headers=header)
html = resp.content.decode()

soup = BeautifulSoup(html)

f = open("proxy.txt","w")

table = soup.find("table",id='ip_list')

trs = table.find_all('tr',class_={'','odd'})

for item in trs:
    tds = item.find_all('td')
    ip_str = tds[1].string + ':' + tds[2].string
    f.write(ip_str+'\n')

f.close()
