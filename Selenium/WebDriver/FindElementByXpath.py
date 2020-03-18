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

if __name__ == '__main__':

    driver = webdriver.Firefox(executable_path="../WebDriver/geckodriver.exe")
    driver.implicitly_wait(10)

    # 打开网页并登录
    driver.get("https://www.baidu.com")

    # 使用Xpath的绝对路径，就是从最高一层节点开始查找
    # 一般来说一个网站的根目录就是html，所以/html与html是一样的
    try:
        Div1 = driver.find_element(By.XPATH, "/html/body/div")
        print(Div1.get_attribute("id"))
    except Exception as msg:
        print(msg)

    # 使用Xpath的相对路径，就是根据path里写的第一个元素为节点开始查
    # path的每一层都可以加条件去筛选(怎么筛选参考下面的例子), 但如果确定某种元素只有一个, 也可以直接写
    try:
        title = driver.find_element(By.XPATH, "//head/title")
        print(title)
    except Exception as msg:
        print(msg)

    # 如果同一层有多个相同的图标，可以使用下标来确定要选取的元素
    try:
        Div1 = driver.find_element(By.XPATH, "/html/body/div[2]")
        print(Div1.get_attribute("id"))
    except Exception as msg:
        print(msg)

    # 如果同一层有多个相同的标签，还可以在[]中使用last()从后面开始访问
    # 下标[]中是可以使用表达式的
    try:
        Div1 = driver.find_element(By.XPATH, "/html/body/div[last()]")  # 最后的节点
        Div2 = driver.find_element(By.XPATH, "/html/body/div[last()-1]")  # 第二后的节点
        print(Div1.get_attribute("id"))
        print(Div2.get_attribute("id"))

    except Exception as msg:
        print(msg)

    # 下标[]中使用@属性=值可以查找相应的标签
    try:
        Div1 = driver.find_element(By.XPATH, "/html/body/div[@id='wrapper']")
        print(Div1.get_attribute("id"))
    except Exception as msg:
        print(msg)

    # 下标[]中表达式中只使用属性就代表找所有这个属性的标签
    try:
        Div3 = driver.find_elements(By.XPATH, "/html/body/div[@id]")  # 查找所有带id属性的div
        for i in Div3:
            print(i.get_attribute("id"))

    except Exception as msg:
        print(msg)

    # 下标[]中表达式中可以使用一些内置方法, 比如text()
    try:
        a_with_text = driver.find_element(By.XPATH, '//a[text()="地图"]')  # 查找显示的文字为"地图"的a元素
        print(a_with_text.text)

        a_with_position = driver.find_elements(By.XPATH, '//div[@id="u1"]/a[position()<=3]')  # 查找id为u1的div下面前三个a元素
        print(a_with_position)

    except Exception as msg:
        print(msg)

    # 下标[]中表达式中使用的条件或者方法可以套用或者使用逻辑表达式
    try:
        a_contain_text = driver.find_element(By.XPATH, '//a[contains(text(),"术")]')  # 查找显示的文字包含"术"的a元素
        print(a_contain_text.text)

        # 查找class中包含layer或者wrapper的div元素
        divs = driver.find_elements(By.XPATH, '//div[contains(@class,"layer") or contains(@class,"wrapper")]')
        print(divs)

        # 依靠子节点定位
        body_with_sub_div = driver.find_element(By.XPATH, '//body[div[@id="wrapper"]]')
        print(body_with_sub_div)

    except Exception as msg:
        print(msg)

    driver.quit()


