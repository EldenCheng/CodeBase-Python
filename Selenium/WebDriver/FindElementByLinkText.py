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

alert = driver.switch_to.alert()


alert.send_keys('admin' + Keys.TAB + 'password')

time.sleep(3)

alert.accept()

time.sleep(3)

#print("Current driver's title: " + driver.title)

#find_element_by_link_text 或者 find_element_by_partial_link_text都只能找到<a> </a>元素，不能找到其他元素的
try:
    driver.switch_to.frame("bottomLeftFrame")
    WebEL = driver.find_element_by_link_text("设置向导")
    
except Exception as msg:
    print(msg)
else:
    print(WebEL.get_attribute("href"))
#    for i in WebEL:
#        print(i.text)


