# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class ChinanewsCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    """
    定义下面字段,spider从网页获取相应的数据后可以存放在对应的字段中
    实际上实例化之后的item用法与字典相似, 可以对其做与字典一样的操作, 比如可以像下面一样:
    items = ChinanewsCrawlerItem()  # 初始化
    items['title'] = 'A title'  # 赋值
    items.get('title') 或者 items['title']  # 取值
    ......
    但要注意item与字典相似但不是直接就是字典, 所以如果想把item转换成字典还是要显式转换:
    items_dict = dict(items)  # item转换为字典, 这个在写入json时会常常用到
    """
    title = Field()
    link = Field()
    desc = Field()
    pub_date = Field()

