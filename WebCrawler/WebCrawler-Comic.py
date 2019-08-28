#!usr/bin/python
# coding: utf-8
import os
import shutil

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def check_and_mkdir(folder_name):
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)


def download_image(link, filename):
    try:

        headers = {'Referer': 'https://18comic.org/photo/{0}/'.format(cid),
                   'Sec-Fetch-Mode': 'no-cors',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
                   }

        requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接
        retry = Retry(connect=5, backoff_factor=1)
        adapter = HTTPAdapter(max_retries=retry)
        s.mount('http://', adapter)
        s.mount('https://', adapter)

        response = s.get(link, stream=True, headers=headers)
        with open('{0}'.format(filename), 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
    except Exception as msg:
        print(msg)


if __name__ == '__main__':

    # 输入漫画所在的根网址
    url = "https://18comic.pro"
    # 输入漫画所有的目录ID
    cid = '40394'
    # 输入本地存放漫画的目录
    title = '约会大作战 旗袍ver. 時崎狂三同人'
    # 输入图片连接所在元素的CSS selector
    img_locator = 'img.lazy_img'

    # 建立request session, 以免未关闭的连接过多导致网站reject新连接
    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接
    retry = Retry(connect=5, backoff_factor=1)
    adapter = HTTPAdapter(max_retries=retry)
    s.mount('http://', adapter)
    s.mount('https://', adapter)

    # 模拟浏览器的请求头以免简单被网站认出是爬虫
    headers = {'authority': '18comic.org',
               'method': 'GET',
               'path': '/photo/{0}/'.format(cid),
               'scheme': 'https',
               'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,'
                         'image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

    html = s.get("{0}/photo/{1}/".format(url, cid), headers=headers)  # 获得漫画所在页面的html

    # 创建 Beautiful Soup 对象并解释所有图片的url
    bs = BeautifulSoup(html.text, 'html5lib')
    print("Searching images...")
    img_with_class = bs.select(img_locator)

    if img_with_class:
        # 建立本地图片存放目录
        folder_dir = './{0}'.format("{0}".format(title))
        check_and_mkdir(folder_dir)

        # 由于图片是动态加载的, 已加载图片与未加载图片url的获取位置不一样,所以需要分开处理
        for i in img_with_class:
            if i.attrs.get('data-original'):
                url2 = i.attrs.get('data-original')
            else:
                url2 = i.attrs.get('src')
            if url2 is not None:
                filename = url2.split('/')[-1]
                print("Downloading pic {0}".format(filename))
                # download_image(url + url2, folder_dir + '/' + filename)
                download_image(url2, folder_dir + '/' + filename)
            else:
                continue
    else:
        print("Can't find any pics")
