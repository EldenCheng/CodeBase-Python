# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

driver =webdriver.Ie(".\\Webdrivers\\IEDriverServer.exe")
driver.implicitly_wait(10)

driver.get("https://www.ap506.p2g.netd2.hsbc.com.hk/")
time.sleep(5)

#print(driver.title)

if driver.title.find("Certificate") != -1:
    try:
        # 如果遇到证书错误，可以点击那条继续去xxx网站的连接来继续
        driver.find_element_by_id("overridelink").click()
        time.sleep(5)
    except Exception as msg:
        print(msg)

try:
    alert = driver.switch_to_alert()
    #在IE中，可以直接用authenticate方法，不知道为什么不能在Firefox上面用
    alert.authenticate('aplogin','swdhasp2g16')
except Exception as msg:
    print(msg)

time.sleep(10)

print(driver.title)