# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

if __name__ == '__main__':
    #Option 类
    Options = webdriver.ChromeOptions()

    #添加要使用的Option, 在Windows的写法一般是"--start-maximised"，但在python里前面的"--"可要可不要
    #"test-type"参数可以避免一些警告，比如Https对不上证书错误
    Options.add_argument("start-maximized")
    Options.add_argument("test-type")
    driver =webdriver.Chrome(executable_path=".\\Webdrivers\\chromedriver.exe", chrome_options=Options)
    driver.implicitly_wait(10)

    driver.get("https://www.baidu.com/")