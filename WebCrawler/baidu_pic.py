from urllib.request import urlretrieve
import time
from selenium import webdriver


class Crawler:

    def __init__(self):
        self.url = 'http://image.baidu.com/i?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&sf=1&' \
                   'fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8' \
                   '&word=%E6%89%8B%E6%9C%BA&oq=shouji&rsp=1'  # url to crawl
        self.img_css = 'div.imgbox > a > img'  # xpath of img element
        self.download_css = 'div.hover > div > div > div > a.down'  # xpath of download link element
        self.img_url_dic = {}

    # kernel function
    def launch(self):
        # launch driver
        driver = webdriver.Firefox(executable_path='./WebDrivers/geckodriver.exe')
        driver.maximize_window()
        driver.get(self.url)
        img_url_dic = self.img_url_dic

        # 模拟滚动窗口以浏览下载更多图片
        pos = 0
        for i in range(10):
            pos += i * 500  # 每次下滚500
            js = "document.documentElement.scrollTop=%d" % pos
            driver.execute_script(js)
            el1 = driver.find_elements_by_css_selector(self.img_css)
            el2 = driver.find_elements_by_css_selector(self.download_css)
            elements = zip(el1, el2)


            # get image desc and download
            for img_element, link_element in elements:
                img_desc = img_element.get_attribute('data-desc')  # description of image
                img_desc = self.filter_filename_str(img_desc)

                img_url = link_element.get_attribute('href')  # url of source image
                if img_url is not None and not img_url_dic.get(img_url):
                    img_url_dic[img_url] = ''
                    ext = img_url.split('.')[-1]
                    filename = img_desc + '.' + ext
                    print(img_desc)
                    print(img_url)
                    urlretrieve(img_url, './yourfolder/%s' % filename)  # 下载图片
                    time.sleep(1)
        driver.close()

    # filter invalid characters in filename
    def filter_filename_str(self, s):
        invalid_set = ('\\', '/', ':', '*', '?', '"', '<', '>', '|', ' ')
        for i in invalid_set:
            s = s.replace(i, '_')
        return s


if __name__ == '__main__':
    crawler = Crawler()
    crawler.launch()
