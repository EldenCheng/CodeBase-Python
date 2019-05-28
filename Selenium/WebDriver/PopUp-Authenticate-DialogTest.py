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

driver.get("http://192.168.8.253")

time.sleep(5)


#switch_to_alert会返回一个Alert 实例，要注意Alert没有继承webdriver的方法与属性，所以不能使用webdriver的方法
alert = driver.switch_to.alert

#print("Alert title: " + alert.title) #这个是错误的
print("Alert content: " + alert.text)

#与switch_to_frame与switch_window不同，driver还是引用刚才的网页没变
print("Driver title: " + driver.title)




#Alert实例的所能使用的方法是根据webdriver.common.alert里面的
#因为send_keys方法所指向的是当前第一个输入框，而在alert dialog里查找元素不方便，所以直接将TAB键也一起输入
alert.send_keys('admin' + Keys.TAB + 'password')

#alert.send_keys("admin") #下面这样输入的话，会将用户名与密码都输入到第一个输入框，通常是用户名框
#alert.send_keys(Keys.TAB)
#alert.send_keys("password")

time.sleep(3)

alert.accept() #自动点确定

#不是所有alert都可以用authenticate方法的，这个例子里的网页就不行(也有可能是Firefox的问题)
#alert.authenticate("admin","password")


