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


def init_requests(get_url, header, stream=False):
    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数

    s = requests.session()

    s.keep_alive = False  # 关闭多余连接

    retry = Retry(connect=5, backoff_factor=1)

    adapter = HTTPAdapter(max_retries=retry)

    s.mount('http://', adapter)

    s.mount('https://', adapter)

    return s.get(get_url, headers=header, stream=stream)


def download_image(link, filename):
    try:

        headers = {# 'Referer': 'https://18comic.org/photo/{0}/'.format(cid),
                   'Sec-Fetch-Mode': 'no-cors',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
                   }
        response = init_requests(link, header=headers, stream=True)

        with open('{0}'.format(filename), 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
    except Exception as msg:
        print(msg)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Please input tid.')
    parser.add_argument('tid', metavar='N', type=str, help='tid of the 2048')
    args = parser.parse_args()

    if args.tid:
        tid = args.tid

    host_name = 'hjd.sysy2048.net'
    page_path = '/2048/read.php?tid-{0}.html'.format(tid)
    url = "https://{0}{1}".format(host_name, page_path)
    headers = {'authority': host_name,
               'method': 'GET',
               'path': page_path,
               'scheme': 'https',
               'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,'
                         'image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}

    html = init_requests(url, header=headers)
    html.encoding = 'utf-8'  # requests在获取response时会尝试自动匹配编码, 但有时候中文网页匹配失败造成会乱码, 这时候就要显式指定编码

    # 创建 Beautiful Soup 对象
    bs = BeautifulSoup(html.text, 'html5lib')
    # print(bs)
    web_title = ''.join(bs.title.text.split())
    web_title = web_title.split(",")[0]
    # web_title = web_title.encode(encoding='big5').decode(encoding='utf-8')
    print("将要获取的内容: ", web_title)
    folder_dir = './2048/{0}'.format("{0}".format(web_title))
    check_and_mkdir(folder_dir)
    #
    # 从得到的HTML页面中解析图片连接
    print("Searching images...")
    img_with_class = bs.select('div.tpc_content img')

    # 下载所有图片
    for i in img_with_class:
        url2 = i.attrs.get('src')
        if url2 is not None:
            filename = url2.split('/')[-1]
            print("Downloading pic {0}".format(filename))
            download_image(url2, folder_dir + '/' + filename)
        else:
            continue

    # # 将下载的目录打包方便传输
    # print("Zipping")
    #
    # z = zipfile.ZipFile(tid + '.zip', 'w')
    # if os.path.isdir(folder_dir):
    #     for d in os.listdir(folder_dir):
    #         z.write(folder_dir+os.sep+d)
    # # close() 是必须调用的！
    # z.close()
    #
    # print("Removing folder")
    # shutil.rmtree(folder_dir)
