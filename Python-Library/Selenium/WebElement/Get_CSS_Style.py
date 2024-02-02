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
driver.get("http://www.baidu.com")

element = driver.find_element_by_id("su")

#dGet CSS Style value
print(element.value_of_css_property("width"))
