# -*- encoding: utf8 -*-
"""
下面演示从中国新闻网的rss内容中获取信息, 由于这里是直接打开了具体的一个新闻连接而不是通过获取新闻列表之后再一一获取, 所以在本书中这个叫直接式爬取
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

if __name__ == '__main__':
    response = urlopen('http://www.chinanews.com/rss/scroll-news.xml')
    rss = BeautifulSoup(response.read(), 'html.parser')
    items = list()

    for item in rss.find_all('item'):
        feed_item = {
            'title': item.title.text,
            'link': item.link.text,
            'desc': item.description.text,
            'pub_date': item.pubdate.text
        }

        items.append(feed_item)  # 将结果保存到JSON文件中

    with open('result.json', 'w', encoding='utf-8') as file:
        json.dump(items, file)
