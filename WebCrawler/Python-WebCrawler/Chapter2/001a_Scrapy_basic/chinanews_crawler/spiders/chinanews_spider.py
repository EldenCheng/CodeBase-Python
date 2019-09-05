import scrapy
from bs4 import BeautifulSoup
from ..items import ChinanewsCrawlerItem


class chinanews(scrapy.Spider):  # 需要继承scrapy.Spider类
    """
    下面演示基础的spider的写法, 一般来说, 爬取的流程大概是这样:
    1. 根据start_urls调用start_requests发送请求, 获取返回内容时调用callback方法(默认的callback方法是self.parse)来处理返回的原始内容
    2. 在callback方法中通过分析原始内容, 获取需要的内容后:
        a. 如果已经能直接获取所需要的内容(即直接获取), 就把获取的内容写入到预定义的item的Field里
        b. 如果获取的只是所需内容的连接(即间接获取), 就使用获取到的连接再调用Request方法发送请求, 获取的返回内容可以使用一个新的callback方法
           去处理, 也可以在所在的callback方法中通过建立不同的分支去处理
        c. 获取所需内容之后如果这些内容需要先作一定处理后再存放的话,可以在pipelines里定义一些item的处理方法, spider在完成所有数据的爬取后
           会调用pipelines时的方法处理后item数据后,将更新后的数据再次存放到item的Field里
        d. 在访问完预先定义好的所有的连接后, Scrapy会根据settings.py里的输出设定把所有item都输出
    """

    name = "chinanews"  # 定义蜘蛛名, 实际我们开始运行一个爬虫就是从指定蜘蛛名开始的
    allowed_domains = ['chinanews.com']  # 这个是可选项,作用是限制爬虫只在需要的站点中爬取数据

    '''
    下面的演示中是使用了start_rquests方法, 但如果比较简单不需要自定义太多东西的话
    可以直接定义start_urls:
    start_urls = [
        'http://www.example.com/1.html',
        'http://www.example.com/2.html',
        'http://www.example.com/3.html',
    ]
    如果定义了start_urls, 就不需要显式定义start_requests了
    '''

    def start_requests(self):  # 由此方法通过下面链接爬取页面

        # 定义爬取的链接
        urls = ('http://www.chinanews.com/rss/rss_2.html', )
        for url in urls:
            if url is not None:
                # yield在这里是用于替代return, yield不会立即返回而是将结果放入一个迭代器里面, 直到最后所有语句运行完成后
                # 直接返回这个迭代器
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        start_requests已经爬取到页面，那如何提取我们想要的内容呢？那就可以在这个方法里面定义。
        1、定义链接；
        2、通过链接爬取（下载）页面；
        3、定义规则，然后提取数据；
        :param response:
        :return:
        """

        rss_page = BeautifulSoup(response.body, 'html.parser')
        # 获取页面中所有a 标签中的href的值, 然后放到一个set里面去
        # 使用set的目的是过滤掉重复的连接(set的特性就是不能存放多个相同值的内容)
        rss_links = set([item['href'] for item in rss_page.find_all('a')])
        # 由于已经知道当前页面没有需要的数据, 所以根据获取得连接再次发送请求, 另外使用parse_feed来处理新获取的内容
        for link in rss_links:
            yield scrapy.Request(url=link, callback=self.parse_feed)

    def parse_feed(self, response):
        rss = BeautifulSoup(response.body, 'lxml')
        for item in rss.find_all('item'):
            feed_item = ChinanewsCrawlerItem()  # 将items里定义的item类实例化, 用于存放获取到的数据
            feed_item['title'] = item.title.text
            feed_item['link'] = item.link.text
            feed_item['desc'] = item.description.text
            feed_item['pub_date'] = item.pubdate.text
            yield feed_item
