#coding=utf-8
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy

import time

import os
import platform
import tempfile
import shutil

from PIL import Image
from functools import reduce

PATH = lambda p: os.path.abspath(p)
TEMP_FILE = PATH(tempfile.gettempdir() + "/temp_screen.png")

class Appium_Extend(object):
    def __init__(self, driver):
        self.driver = driver

    def get_screenshot_by_element(self, element):
        #先截取整个屏幕，存储至系统临时目录下
        self.driver.get_screenshot_as_file(TEMP_FILE)

        #获取元素bounds
        location = element.location
        size = element.size
        box = (location["x"], location["y"], location["x"] + size["width"], location["y"] + size["height"])

        #截取图片
        image = Image.open(TEMP_FILE)
        newImage = image.crop(box)
        newImage.save(TEMP_FILE)

        return self

    def get_screenshot_by_custom_size(self, start_x, start_y, end_x, end_y):
        #自定义截取范围
        self.driver.get_screenshot_as_file(TEMP_FILE)
        box = (start_x, start_y, end_x, end_y)

        image = Image.open(TEMP_FILE)
        newImage = image.crop(box)
        newImage.save(TEMP_FILE)

        return self

    def write_to_file( self, dirPath, imageName, form = "png"):
        #将截屏文件复制到指定目录下
        if not os.path.isdir(dirPath):
            os.makedirs(dirPath)
        shutil.copyfile(TEMP_FILE, PATH(dirPath + "/" + imageName + "." + form))

    def load_image(self, image_path):
        #加载目标图片供对比用
        if os.path.isfile(image_path):
            load = Image.open(image_path)
            return load
        else:
            raise Exception("%s is not exist" %image_path)

    #http://testerhome.com/topics/202
    def same_as(self, load_image, percent):
        #对比图片，percent值设为0，则100%相似时返回True，设置的值越大，相差越大
        import math
        import operator

        image1 = Image.open(TEMP_FILE)
        image2 = load_image

        # 把图像对象转换为直方图数据
        histogram1 = image1.histogram()
        histogram2 = image2.histogram()

        '''
        sqrt:计算平方根，reduce函数：前一次调用的结果和sequence的下一个元素传递给operator.add
        operator.add(x,y)对应表达式：x+y
        这个函数是方差的数学公式：S^2= ∑(X-Y) ^2 / (n-1)
        '''
        differ = math.sqrt(reduce(operator.add, list(map(lambda a,b: (a-b)**2, histogram1, histogram2)))/len(histogram1))
        print(differ)
        if differ <= percent:
            return True
        else:
            return False

if __name__ == "__main__":
    desired_caps = {}
    desired_caps['platformName'] = 'Android'
    desired_caps['platformVersion'] = '7.1.1'
    desired_caps['deviceName'] = 'Android Emulator'
    desired_caps['appPackage'] = 'com.android.calculator2'
    desired_caps['appActivity'] = '.Calculator'

    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    ext = Appium_Extend(driver)
    ext.get_screenshot_by_element(driver.find_element_by_android_uiautomator("new UiSelector().text(\"7\")"))
    ext.write_to_file(".\\" , "Sample2")

    imageSample = ext.load_image(r".\Sample2.png")
    print(ext.same_as(imageSample,10))

