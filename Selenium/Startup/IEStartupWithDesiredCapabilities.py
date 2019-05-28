# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

#在IE中有些设置可以定义DesiredCapabilities来控制，但IE11好像不支持所有的DesiredCapabilities
DS = webdriver.DesiredCapabilities.INTERNETEXPLORER.copy() #API文档里要求用这个方法初始化DesireCapabilites，实际上在Python里使用这个方法初始化返回的DesireCapabilites是一个字典
DS['ignoreProtectedModeSettings'] = True #添加关键字与属性, 这个属性起作用，但API文档里警告说有危险，所以应该尽量避免用
DS['requireWindowFocus'] = True
DS['acceptSslCerts'] = True                #这个属性是selenium webdriver的，在IE中好像不起作用

for i in DS:
    print(i + " value is: " + str(DS[i]))


driver =webdriver.Ie(executable_path=".\\Webdrivers\\IEDriverServer.exe", capabilities=DS)
driver.implicitly_wait(10)

driver.get("https://www.ap506.p2g.netd2.hsbc.com.hk/")

time.sleep(10)

print(driver.title)

driver.quit()