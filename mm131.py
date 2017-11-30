import sys
from bs4 import BeautifulSoup
import requests
import os

headers = {'Referer': 'http://www.mm131.com/'}

rp = requests.get('http://www.mm131.com/qingchun/',  headers=headers)

if rp.status_code != 200:
    print('数据未能抓取成功')
    sys.exit(1)
else:
    html = rp.content.decode('gbk')
    soup = BeautifulSoup(html)
    par = soup.find('dl', class_=['list-left', 'public-box'])
    dds = par.find_all('dd', class_='')
    for it in dds:
        link = it.a['href']
        res = requests.get(link,headers=headers)
        if res.status_code != 200:
            print('二级数据未能抓取成功')
            sys.exit(1)
        else:
            s2 = BeautifulSoup(res.content.decode('gbk'))
            pageNumber = s2.find('span', class_='page-ch').string.replace('共', '').replace('页', '')
            imgBox = s2.find('div', class_='content-pic')
            img_url = imgBox.img['src']
            img_desc = imgBox.img['alt']
            url_ids = img_url.split('/')
            url_id = url_ids[4]
            for i in range(1,(int(pageNumber)+1)):
                img_req_url = url_ids[0]+'/'+url_ids[1]+'/'+url_ids[2]+'/'+url_ids[3]+'/'+url_ids[4]+'/'+str(i)+'.jpg'
                img_res = requests.get(img_req_url, headers=headers)
                if img_res.status_code == 200:
                    print('正在下载->>>', img_req_url)
                    sss = 'E:/app/test/'+img_desc+'/'
                    if not os.path.exists(sss):
                        os.mkdir(sss)
                    f = open(sss+str(i)+'.jpg', 'wb')
                    f.write(img_res.content)
                    f.close()
                else:
                    print(img_req_url, '数据未能抓取成功')
