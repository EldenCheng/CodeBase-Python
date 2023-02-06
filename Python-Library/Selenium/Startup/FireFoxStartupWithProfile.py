# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

# 如果不指定Firefox的profile,webdriver每次打开的firefox都会使用一个全新的临时profile
# 有时这样会导致一些问题发生，比如https的证书不合规格，需要在firefox里加例外，但如果不使用已添加例外的profile, webdriver就有可能报错
# Firefox本身的profile管理器打开的方法是在运行窗口输入 firefox.exe -ProfileManager
# 在Selenium上使用的话就如下面所写
driver =webdriver.Firefox(".\\FirefoxProfile\\9ar61g3i.default")
driver.implicitly_wait(10)

driver.get("http://192.168.8.253")




