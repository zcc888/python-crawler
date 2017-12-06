from selenium import webdriver
import time
from bs4 import BeautifulSoup

driver = webdriver.PhantomJS()

driver.get("https://buluo.qq.com/p/barindex.html?bid=13609")
time.sleep(3)
html = driver.page_source
soup = BeautifulSoup(html)
par = soup.find('div', {'class':'center wrapper clearfix'})
ul = par.find('ul', class_='post-list')
lis = ul.find_all('li',class_='post')
for item in lis:
    href = 'http:'+item.find('a')['href']
    title = None
    try:
        title_obj = item.find('div', class_='title')
        if title_obj is None:
            title_obj = item.find('div', class_='content')
        spans = title_obj.find_all('span')
        title = spans[len(spans)-1].text
    except Exception as e:
        print("抓取数据失败 : %s " % href)
    print("标题: %s ,链接: %s " % (title, href))
