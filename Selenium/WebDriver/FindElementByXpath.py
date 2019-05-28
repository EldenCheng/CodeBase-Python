# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
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
time.sleep(15)

#使用Xpath的绝对路径，就是从最高一层节点开始查找
#一般来说一个网站的根目录就是html，所以/html与html是一样的
try:
    Div1 = driver.find_element(By.XPATH, "/html/body/div")
    print(Div1.get_attribute("id"))
except Exception as msg:
    print(msg)

#如果同一层有多个相同的图标，可以使用下标来确定要选取的元素
try:
    Div1 = driver.find_element(By.XPATH, "/html/body/div/div[2]")
    print(Div1.get_attribute("class"))
except Exception as msg:
    print(msg)

#如果同一层有多个相同的标签，还可以在[]中使用last()从后面开始访问
#下标[]中是可以使用表达式的
try:
    Div1 = driver.find_element(By.XPATH, "/html/body/script[last()]") #最后的节点
    Div2 = driver.find_element(By.XPATH, "/html/body/script[last()-1]") #第二后的节点
    print(Div1.get_attribute("type"))
    print(Div2.get_attribute("type"))
except Exception as msg:
    print(msg)

#下标[]中使用@属性=值可以查找相应的标签
try:
    Div1 = driver.find_element(By.XPATH, "/html/body/div/div[@class='extra_content']")
    print(Div1.get_attribute("class"))
except Exception as msg:
    print(msg)

#下标[]中表达式中只使用属性就代表找所有这个属性的标签
try:
    Div3 = driver.find_elements(By.XPATH, "/html/body/div/div[@class]") #查找所有带class属性的div
    for i in Div3:
        print(i.get_attribute("class"))

except Exception as msg:
    print(msg)

driver.quit()


