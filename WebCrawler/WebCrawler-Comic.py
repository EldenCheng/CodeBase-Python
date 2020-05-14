#!usr/bin/python
# coding: utf-8
import shutil
import unittest
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
import requests
import os
import zipfile
import shutil
import argparse

from urllib3 import Retry

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))


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

    # 直接从命令行中获取漫画的CID
    # 注意如果没有分页, 直接把CID作为参数传入 比如 python WebCrawler-Comic.py 122020
    # 如果有分页, 就需要把CID之后整个字符串传入, 比如 python WebCrawler-Comic.py 122020/?page=2
    parser = argparse.ArgumentParser(description='Please input cid.')
    parser.add_argument('cid', metavar='N', type=str, help='cid of the 18comic alarm')
    args = parser.parse_args()

    if args.cid:
        cid = args.cid

    # title = '[苦渡众生汉化组] (C80) [クリムゾン] 停波総集編 (ファイナルファンタジーVII)'

    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数

    s = requests.session()

    s.keep_alive = False  # 关闭多余连接

    retry = Retry(connect=5, backoff_factor=1)

    adapter = HTTPAdapter(max_retries=retry)

    s.mount('http://', adapter)

    s.mount('https://', adapter)

    headers = {'authority': '18comic.org',
               'method': 'GET',
               'path': '/photo/{0}/'.format(cid),
               'scheme': 'https',
               'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,'
                         'image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

    # 由于有些漫画太长造成了分页, CID会加上分布的页号如下, 所以需要判断CID中是否有分页
    # html = s.get("https://18comic.org/photo/122020/?page=2", headers=headers)
    if "page=" in cid:
        html = s.get("https://18comic.org/photo/{0}".format(cid), headers=headers)
    else:
        html = s.get("https://18comic.org/photo/{0}/".format(cid), headers=headers)

    url = "https://18comic.org"

    # 创建 Beautiful Soup 对象
    bs = BeautifulSoup(html.text, 'html5lib')

    web_title = ''.join(bs.title.text.split())
    web_title = web_title.split("|")[0]
    print(web_title)
    folder_dir = './{0}'.format("{0}".format(web_title))
    check_and_mkdir(folder_dir)

    # 从得到的HTML页面中解析图片连接
    print("Searching images...")
    img_with_class = bs.select('img.lazy_img')

    # 下载所有图片
    for i in img_with_class:
        if i.attrs.get('data-original'):
            url2 = i.attrs.get('data-original')
        else:
            url2 = i.attrs.get('src')
        if url2 is not None:
            filename = url2.split('/')[-1]
            # 因为有些预览图是带'x'的, 而我们又不需要, 所以跳过这种图片
            if 'x' not in filename:
                print("Downloading pic {0}".format(filename))
                # download_image(url + url2, folder_dir + '/' + filename)
                download_image(url2, folder_dir + '/' + filename)
        else:
            continue

    # 将下载的目录打包方便传输
    print("Zipping")

    # 同样为分页做准备, 有分页的就在文件名后面加上分页的页号
    if "page=" in cid:
        cid_f = cid.split("/?page=")[0]
        cid_e = cid.split("/?page=")[1]
        cid = cid_f + "_" + cid_e
    z = zipfile.ZipFile(cid + '.zip', 'w')
    if os.path.isdir(folder_dir):
        for d in os.listdir(folder_dir):
            z.write(folder_dir+os.sep+d)
    # close() 是必须调用的！
    z.close()

    print("Removing folder")
    shutil.rmtree(folder_dir)
