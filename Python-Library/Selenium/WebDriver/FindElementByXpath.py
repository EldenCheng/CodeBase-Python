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

    # 下标[]中表达式中使用not()加属性就代表找所有不带这个属性的标签
    try:
        Div3 = driver.find_elements(By.XPATH, "/html/body/div[not(@id)]")  # 查找所有不带id属性的div
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

    # 下标[]中表达式中可以指定兄元素(前一个)或者弟元素(后一个), 作为表达式的兄弟元素本身也可以使用[]来筛选
    try:
        a_with_text = driver.find_element(By.XPATH, '//a[preceding-sibling::div[@id="u1"]]')  # 查找a元素, 它的兄节点(前一个)是id为u1的div元素
        print(a_with_text.text)

        # 查找是id为u1的div元素与id为u2的div元素之间存在的a元素
        a_with_text = driver.find_element(By.XPATH, '//a[preceding-sibling::div[@id="u1"] and following-sibling::div[@id="u2"]]')
        print(a_with_text)

        # 查找后面只有一个id为u2的div元素的a元素 (如果有a元素后面跟着两个id为u2的div元素的话, 就不符合条件)
        a_with_text = driver.find_element(By.XPATH, '//a[count(following-sibling::div[@id="u2"])=1]')
        print(a_with_text)

    except Exception as msg:
        print(msg)

    # 查找一个元素后, 可以通过关键字来获得它的父, 子, 兄弟节点
    try:
        # 先查找一个包括文字包括"术"的a元素, 再通过它来获得id为u1的兄元素div元素(注意结果是div元素而不是a元素)
        div_with_text = driver.find_element(By.XPATH, '//a[contains(text(),"术")]/preceding-sibling::div[@id="u1"]]')
        print(div_with_text.text)

        # 先查找一个包括文字包括"术"的a元素, 再通过它来获得上一层元素的子元素中id为u1的兄元素div元素(注意结果是div元素而不是a元素)
        div_with_text = driver.find_element(By.XPATH, '//a[contains(text(),"术")]/../preceding-sibling::div[@id="u1"]]')
        print(div_with_text)

        '''
        相对关系的关键字收集如下
        XPath轴(XPath Axes)可定义某个相对于当前节点的节点集： 
        1、child 选取当前节点的所有子元素 
        2、parent 选取当前节点的父节点 
        3、descendant 选取当前节点的所有后代元素（子、孙等） 
        4、ancestor 选取当前节点的所有先辈（父、祖父等） 
        5、descendant-or-self 选取当前节点的所有后代元素（子、孙等）以及当前节点本身 
        6、ancestor-or-self 选取当前节点的所有先辈（父、祖父等）以及当前节点本身 
        7、preceding-sibling 选取当前节点之前的所有同级节点 
        8、following-sibling 选取当前节点之后的所有同级节点 
        9、preceding 选取文档中当前节点的开始标签之前的所有节点 
        10、following 选取文档中当前节点的结束标签之后的所有节点 
        11、self 选取当前节点 
        12、attribute 选取当前节点的所有属性 
        13、namespace 选取当前节点的所有命名空间节点
        '''

    except Exception as msg:
        print(msg)

    driver.quit()


