# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

driver =webdriver.Firefox()
driver.implicitly_wait(10)


#打开网页并登录
driver.get("http://192.168.8.253")

time.sleep(5)

# alert = driver.switch_to_alert()
alert = driver.switch_to.alert


alert.send_keys('admin' + Keys.TAB + 'password')

time.sleep(3)

alert.accept()

time.sleep(3)

#print("Current driver's title: " + driver.title)

#转到另一个frame去，因为如果不转到对应的frame,那么frame下面的element是找不到的
#也不能用find_element查找到frame(能够找到的)，再使用find_element查找子元素的方法来查找frame下面的元素
try:
    driver.switch_to.frame("bottomLeftFrame")
    WebEL = driver.find_element_by_id("a1")
    # 转回主页面
    driver.switch_to.default_content()
    
except Exception as msg:
    print(msg)
else:
    print(WebEL.text)


