import requests
from bs4 import BeautifulSoup
import sys,os,threading

proxies = {
    'http':'101.68.73.54:53281'
}

def save_img(s_url):
    print("->>>正在获取二级页面内容：%s" % s_url)
    s_resp = requests.get(s_url,headers=headers,proxies=proxies)
    if s_resp.status_code != 200:
        print('->>>获取二级页面失败：%s' % s_url)
    else:
        s_html = s_resp.content.decode('utf-8')
        page_html = BeautifulSoup(s_html)
        div_box = page_html.find('div',id='fontzoom')
        ps = div_box.find_all('p')
        img_box = ps[(len(ps))-1]
        imgs = img_box.find_all('img')
        for item in imgs:
            src = 'http://qq.yh31.com'+item['src']
            src_split = src.split("/")
            img_rep = requests.get(src,headers=headers,proxies=proxies)
            if img_rep.status_code != 200:
                print('->>>获取图片资源失败：%s' % src)
            else:
                print("->>>当前正在写入文件：%s" % src)
                path = 'F:/tem/2/'
                f = open(path+src_split[5],'wb')
                f.write(img_rep.content)
                f.close()


headers = {'Referer':'http://qq.yh31.com'}

rep = requests.get('http://qq.yh31.com/zjbq/0551964.html',headers=headers,proxies=proxies)


if rep.status_code != 200:
    print('获取页面失败')
    sys.exit(1)
else:
    html = rep.content.decode('utf-8')
    threads = []
    # save_img(html)
    for i in range(2,86):
        s_url = 'http://qq.yh31.com/zjbq/0551964_%s.html' % i
        t = threading.Thread(target=save_img, args={s_url})
        threads.append(t)

    for item in threads:
        item.start()

