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
driver.get("http://www.wesoft.com")
time.sleep(60)


try:
    Child1 = driver.find_element(By.CSS_SELECTOR, "div.nivoSlider#slider a:nth-child(1)")
    for i in range(0,6):
        print(str(i+1) + " times, Child node 1's is_displayed property: " + str(Child1.is_displayed()))
        print(str(i+1) + " times, Child node 1's is_enabled property: " + str(Child1.is_enabled()))
        time.sleep(5)
except Exception as msg:
    print(msg)

driver.quit()