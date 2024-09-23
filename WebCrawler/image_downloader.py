import time

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


def download_image(link, image_name, proxy=None):
    try:

        headers = {'Referer': f'https://18comic.org/photo/0123456/',
                   'Sec-Fetch-Mode': 'no-cors',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
                   }

        proxies = {"http": proxy, "https": proxy}
        requests.adapters.DEFAULT_RETRIES = 3  # 增加重连次数

        s = requests.session()

        s.keep_alive = False  # 关闭多余连接

        retry = Retry(connect=3, backoff_factor=1)

        adapter = HTTPAdapter(max_retries=retry)

        s.mount('http://', adapter)

        s.mount('https://', adapter)

        response = s.get(link, stream=True, headers=headers, proxies=proxies)

        with open('{0}'.format(image_name), 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
    except Exception as msg:
        print(msg)


if __name__ == '__main__':
    gallery_url = 'https://m1.imhentai.xxx/005/tc9vd6qo0y/'
    image_title = 'ManguSta(－恥辱風紀委員会)'
    image_index_begin, image_index_end = (1, 1197)
    proxy = "http://127.0.0.1:7890"

    folder_dir = f'./{image_title}'
    check_and_mkdir(folder_dir)
    # test_link = "https://m1.imhentai.xxx/005/tc9vd6qo0y/1.jpg"
    # test_filename = "test.jpg"
    # download_image(test_link, folder_dir + '/' + test_filename, proxy)
    for img_id in range(image_index_begin, image_index_end + 1):
        filename = f"{img_id}.jpg"
        url2 = gallery_url + str(img_id) + ".jpg"
        download_image(url2, folder_dir + '/' + filename, proxy)
        print(f"Image {url2} downloaded")
        time.sleep(3)
