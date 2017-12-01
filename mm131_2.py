import sys
from bs4 import BeautifulSoup
import requests
import os
import threading

headers = {'Referer': 'http://www.mm131.com/'}


def start(url):
    global headers
    rp = requests.get(url,  headers=headers)
    if rp.status_code != 200:
        print('数据未能抓取成功->>> %s ' % url)
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
            else:
                s2 = BeautifulSoup(res.content.decode('gbk'))
                page_number = s2.find('span', class_='page-ch').string.replace('共', '').replace('页', '')
                img_box = s2.find('div', class_='content-pic')
                img_url = img_box.img['src']
                img_desc = img_box.img['alt']
                url_ids = img_url.split('/')
                url_id = url_ids[4]
                for items in range(1, (int(page_number)+1)):
                    img_req_url = url_ids[0]+'/'+url_ids[1]+'/'+url_ids[2]+'/'+url_ids[3]+'/'+url_ids[4]+'/'\
                                  + str(items) + '.jpg'
                    img_res = requests.get(img_req_url,headers=headers)
                    if img_res.status_code == 200:
                        print('正在下载->>>', img_req_url)
                        sss = 'F:/tem/mv/'+img_desc+'/'
                        if not os.path.exists(sss):
                            os.mkdir(sss)
                        f = open(sss + str(items) + '.jpg', 'wb')
                        f.write(img_res.content)
                        f.close()
                    else:
                        print(img_req_url, '数据未能抓取成功')


threads = [threading.Thread(target=start, args={'http://www.mm131.com/qingchun/'})]

for i in range(2,32):
    url_str = 'http://www.mm131.com/qingchun/list_1_%s.html' % i
    threads.append(threading.Thread(target=start,args={url_str}))

for item in threads:
    item.start()

