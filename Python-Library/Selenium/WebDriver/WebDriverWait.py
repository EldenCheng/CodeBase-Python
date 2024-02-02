from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


driver =webdriver.Firefox()
driver.implicitly_wait(10)


#打开网页并登录
driver.get("http://www.wesoft.com")

# 使用Python内置的 lambda 关键字建立一个内联函数作为WebDriverWait的method参数，可以直接让Selenium等待查找元素并进行一定的动作
WebDriverWait(driver,5,0.5).until(lambda x: x.find_element_by_css_selector("a[title=More]")).click()

# 使用Selenium内置的expected_eonditions 类(通常用别名EC)中预定义的函数作用method参数也可以
WebDriverWait(driver,5,0.5).until(EC.title_is("Company _ We Software Limited"))


