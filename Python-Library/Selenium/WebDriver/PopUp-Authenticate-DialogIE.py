# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

driver =webdriver.Ie("..\\Startup\\Webdrivers\\IEDriverServer.exe")
driver.implicitly_wait(10)

driver.get("http://192.168.8.253")

time.sleep(5)


#switch_to_alert会返回一个Alert 实例，要注意Alert没有继承webdriver的方法与属性，所以不能使用webdriver的方法
try:
    alert = driver.switch_to_alert()
    #在IE中，可以直接用authenticate方法，不知道为什么不能在Firefox上面用，但在IE里，KEY.TAB又变成了跳四个空格那种，而不是切换输入框，按实际键盘上的TAB键则可以成功切换输入框
    alert.authenticate('admin','password')
except Exception as msg:
    print(msg)