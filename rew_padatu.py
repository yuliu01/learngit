import re
import requests
import time
from urllib import request
from bs4 import BeautifulSoup
from selenium import webdriver


def get_html(driver, url):
    """获取网页html源码，包括js加载出来的"""
    # driver.get("https://www.duitang.com/search/?kw=%E5%A6%B9%E5%AD%90&type=feed#!s-p2")
    driver.get(url)
    time.sleep(5)
    # driver.find_element_by_xpath('/html/body/div[9]/div/div[1]/a').click()
    # 滚轮滑动到页面底部
    for i in range(6):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)
    # ht = driver.page_source
    bf = BeautifulSoup(driver.page_source, "lxml")
    ht = str(bf)
    # print(ht)
    return ht


def pat(html):
    # 正则匹配主页图片链接
    pat = re.compile('id=.+? class=.+?src="(.+?)" style=".+?\d+px" data-width=.+? data-height=.+?')
    al = re.findall(pat, html)
    print("主页链接")
    print(al)
    print("success")
    return al


def pat_lie(html):
    # 正则匹配大图后缀
    pat = re.compile('a class="a" href="(/blog/.+?)" target="_blank"')
    al = re.findall(pat, html)
    print("大图后缀")
    print(al)
    print("success")
    return al


def down_load(pic_list, dwd_path):
    """下载列表里面的图片"""
    num = 0
    for i in pic_list:
        try:
            date = time.strftime("%Y-%m-%d-%H-%M-%Ss", time.localtime())
            filename = "{0}{1}.jpg".format(dwd_path, date)
            request.urlretrieve(i, filename=filename)
            print("下载{}张".format(num))
            num += 1
            time.sleep(1)
        except Exception as e:
            print(e)


dwd_path = "/Users/liuyu/pythonfile/download/"
URL = "https://www.duitang.com/search/?kw=%E6%B8%85%E7%BA%AF&type=feed"
'''# html = requests.get(url=URL).text
ls = ['/blog/?id=1330642787', '/blog/?id=1320766484', '/blog/?id=1280577911']
# ls = pat_lie(html)'''
# 呼出web driver窗口
driver = webdriver.Chrome()
# 获取网页html源码，包括js加载出来的
html = get_html(driver, URL)
# 正则匹配页面图片详情页面的链接后缀
ls = pat_lie(html)
result_list = []
bigurllist = []
for i in ls:
    # 从列表中获取后缀，与域名拼接
    url = "https://www.duitang.com{0}".format(i)
    # 获取图片详情页源码
    big_html = requests.get(url).text
    # 正则匹配大图链接
    big_url = pat(big_html)
    # 将匹配到的大图链接添加到列表
    bigurllist.extend(big_url)
    time.sleep(1)
print(bigurllist)
print(result_list)
# 下载列表里面所有的大图,测试一下git
down_load(pic_list=bigurllist, dwd_path=dwd_path)
time.sleep(1)
driver.quit()
