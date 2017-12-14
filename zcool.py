import sys
from bs4 import BeautifulSoup
import requests
import os
import uuid
import threading


def startRequest(url):
    print("【提示】正在抓取 - %s " % url)
    res = requests.get(url)
    if res.status_code == 200:
        res_html = res.content.decode()
        doc = BeautifulSoup(res_html)
        work_box = doc.find('div', class_={'work-list-box'})
        card_box_list = work_box.find_all('div', class_={'card-box'})
        for item in card_box_list:
            getContent(item)
    else:
        print("【文档获取失败】【状态为%s】 - %s，" % (url, res.status_code))


def getContent(item):
    title_content = item.find("a", class_={'title-content'})
    avatar = item.find('span', class_={'user-avatar'})
    if title_content is not None and avatar is not None:
        title = title_content.text
        author = avatar.find("a")["title"]
        href = title_content['href']
        # print("%s - 【%s】- %s" % (title, author, href))
        res = requests.get(href)
        if res.status_code == 200:
            # 获取所有的图片链接
            img_list = getDocImgLinks(res.content.decode())
            path_str = "【%s】-【%s】" % (author, title)
            path_str_mk = pathBase('./data/'+nameEncode(path_str))
            if path_str_mk is None:
                return
            else:
                for img_item in img_list:
                    downloadImg(img_item, path_str_mk)

        else:
            print("【文档获取失败】【状态为%s】 - %s，" % (href, res.status_code))
    else:
        return


def getDocImgLinks(html):
    doc = BeautifulSoup(html)
    work_box = doc.find("div", class_={'work-show-box'})
    revs = work_box.find_all("div", class_={'reveal-work-wrap'})
    img_list = []
    for item in revs:
        img = item.find("img")
        if img is not None:
            img_url = img["src"]
            img_list.append(img_url)
        else:
            print("【提示】：没有图片")
            continue
    return img_list


def pathBase(file_path):
    file_name_s = file_path.split("/")
    file_name = file_name_s[len(file_name_s) - 1]
    file_name_s[len(file_name_s) - 1] = file_name
    path = "/".join(file_name_s)
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def nameEncode(file_name):
    file_stop_str = ['\\', '/', '*', '?', ':', '"', '<', '>', '|']
    for item2 in file_stop_str:
        file_name = file_name.replace(item2, '-')
    return file_name


def downloadImg(url, path):
    z_url = url.split("@")[0]
    hz = url.split(".")
    z_hz = hz[len(hz) - 1]
    res = requests.get(z_url)
    if res.status_code == 200:
        img_down_path = path + "/" + str(uuid.uuid1()) + "." + z_hz
        f = open(img_down_path, 'wb')
        f.write(res.content)
        f.close()
        print("【下载成功】 -  %s" % img_down_path)
    else:
        print("【IMG下载失败】【状态为%s】 - %s，" % (z_url, res.status_code))


if __name__ == '__main__':
    threads = []

    for i in range(1, 22):
        url = 'http://www.zcool.com.cn/search/content?type=3&field=8&other=0&sort=5&word=APP%E8%AE%BE%E8%AE%A1' \
              '&recommend=0&requestId=requestId_1513228221822&p='+(str(i))+'#tab_anchor '
        threads.append(threading.Thread(target=startRequest, args={url}))

    for item in threads:
        item.start()

