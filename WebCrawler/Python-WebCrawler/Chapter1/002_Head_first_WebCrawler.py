"""
最简单的爬虫就是直接发送请求到网站然后使用某些库(BS)来解释返回的网页内容
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup

if __name__ == '__main__':
    response = urlopen('https://www.wesoft.com')  # 发送一个请求, 申请www.wesoft.com的首页
    html = response.read()  # 读取首页的内容
    print(html)

    bs = BeautifulSoup(html, 'html.parser')  # 使用BS生成基于html内容的数据结构
    print(bs.title)  # 读取标题

