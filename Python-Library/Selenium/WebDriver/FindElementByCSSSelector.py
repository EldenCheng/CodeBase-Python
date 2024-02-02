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

#在CSS Selector里，标签.xxx表示这个标签的类是xxx, 标签#xxx表示这个标签的ID是xxx, 标签[xxx=yyy]表示这个标签的xxx属性的值是yyy
#下面的例子是查找一个类为"nive-caption-inner"的div标签
#然后再在div下面搜索标签为strong的元素
try:
    Slider = driver.find_element(By.CSS_SELECTOR, "div.nivo-caption-inner")
    Caption = Slider.find_element(By.TAG_NAME,"Strong")
    print(Caption.text)
except Exception as msg:
    print(msg)

#但上面的写法其实可以直接用CSS Selector, 标签(xxx)>标签表示查找符合xxx条件的标签后下的子标签
try:
    Caption2 = driver.find_element(By.CSS_SELECTOR, "div.nivo-caption-inner>strong")
    print(Caption2.text)
except Exception as msg:
    print(msg)

#CSS Selector查找节点可以使用多条件组合，例如下面就用ID与Class共同定位节点
try:
    DivFather = driver.find_element(By.CSS_SELECTOR, "div.nivoSlider#slider")
    print(DivFather.get_attribute("style"))
except Exception as msg:
    print(msg)

#同样可以支持使用多个属性的组合来查找节点，比如使用herf属性与tilte属性来定位一个a元素

try:
    Link = driver.find_element(By.CSS_SELECTOR,"a[href=company][title=More]")
    print(Link.get_attribute("class"))
except Exception as msg:
    print(msg)

#CSS Selector查找子节点可以使用多种方法, 标签:nth-child(n)这种写法可以以标签查找第n个子节点，本身这个n可以是常数，关键字(?)或者表达式
#这个排序可能是先把子节点排完，再排孙节点
try:
    Child1 = driver.find_element(By.CSS_SELECTOR, "div.nivoSlider#slider a:nth-child(1)")
    print("Child node 1: " + Child1.get_attribute("href")) #应该显示nivo-imageLink
except Exception as msg:
    print(msg)

try:
    Child2 = driver.find_element(By.CSS_SELECTOR, "div.nivoSlider#slider a:nth-child(2)")
    print("Child node 2: " + str(Child2.get_attribute("class")) + " " + str(Child2.get_attribute("href")))
except Exception as msg:
    print(msg)

#CSS Selector查找子节点可以使用多种方法, 标签:nth-child(n)这种写法可以以标签查找从后面数起第n个子节点，本身这个n可以是常数，关键字(?)或者表达式
#要注意这个从后面数起是要包括子节点下面的孙节点的，所以如果孙节点中有对应的标签，那么可能查找出来的第一个要从最后的孙节点算起
try:
    Child3 = driver.find_element(By.CSS_SELECTOR, "div.nivoSlider#slider a:nth-last-child(1)")
    print("Last Child node 3: "  + str(Child3.get_attribute("class")) + " " + str(Child3.get_attribute("href")) + " " + str(Child2.get_attribute("style")))
except Exception as msg:
    print(msg)

'''
CSS Selector的类名查找可以支持不完全查找，比如完全类名为Classname, 可以使用标签{class$=assname}, 或者标签[class^=class], 又或者标签[class*=lass]作为关键字查找到对应的节点
其实这里的class可以替换成id,或者任何标签里面有写的属性
'''
try:
    Node1 = driver.find_element(By.CSS_SELECTOR, "div[class$=html-caption]")  # 以html-caption结尾的div
    Node2 = driver.find_element(By.CSS_SELECTOR, "div[class^=nivo-html-c]")  # 以nivo-html-c开头的div
    Node3 = driver.find_element(By.CSS_SELECTOR, "div[class*=html-c]")  # 包含html-c的div
    print("Find by end of Node 1: " + Node1.get_attribute("id"))
    print("Find by begin of Node 2: " + Node2.get_attribute("id"))
    print("Find by any place of Node 3: " + Node3.get_attribute("id"))
except Exception as msg:
    print(msg)

#

#CSS Selector与Xpath不同，不支持由当前节点找到父节点，下面会报错
try:
    Div1 = driver.find_element(By.CSS_SELECTOR, "div.nivo-caption-inner>..") #报错
    print(Div1.get_attribute("class"))
except Exception as msg:
    print(msg)

#CSS Selector可以使用"+"来查找节点同一层，但排在节点之后的节点，同理，CSS Selector同样不支持查找与节点同一层，但排在节点之前的节点
try:
    Div2 = driver.find_element(By.CSS_SELECTOR, "div.nivo-caption + div")
    print("Brother Node: " + Div2.get_attribute("class")) #这里应该是div.nivo-directionNav
except Exception as msg:
    print(msg)


#driver.quit()



