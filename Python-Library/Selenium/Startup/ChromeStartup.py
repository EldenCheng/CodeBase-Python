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
    driver =webdriver.Chrome(".\\Webdrivers\\chromedriver.exe")
    driver.implicitly_wait(10)

    driver.get("https://www.baidu.com")

    print(driver)