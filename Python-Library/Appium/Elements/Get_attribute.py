#coding=utf-8
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy

import time

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '7.1.1'
desired_caps['deviceName'] = 'Android Emulator'
desired_caps['appPackage'] = 'com.android.calculator2'
desired_caps['appActivity'] = '.Calculator'

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)


el = driver.find_element_by_android_uiautomator("new UiSelector().text(\"7\")")

#获取text
print(el.text)

print(el.get_attribute("text"))

#获取description
#print(el.get_attribute("content-desc"))
print(el.get_attribute("name"))

#获取class
print(el.tag_name)

print(el.get_attribute("className"))

#获取Index

print(el.id)

#获取ID

print(el.get_attribute("resourceId"))

#获取Size

print(el.size)

#获取Position

print(el.location)

print(el.location_once_scrolled_into_view)

#获取上级

print(el.parent.name)

#未实现的属性

#print(el.rect)

'''
get_attribute可用参数
字符串类型：
ps:获取 content-desc 的方法为 get_attribute("name")，而且还不能保证返回的一定是 content-desc （content-desc 为空时会返回 text 属性值）

name(返回 content-desc 或 text)
text(返回 text)
className(返回 class，只有 API=>18 才能支持)
resourceId(返回 resource-id，只有 API=>18 才能支持)

布尔类型（如果无特殊说明， get_attribute 里面使用的属性名称和 uiautomatorviewer 里面的一致）：
enabled
checkable
checked
clickable
focusable
focused
longClickable
scrollable
selected

获取不到，但会显示在 uiautomatorviewer 中的属性：
index(可以直接用mobileelement.id来获取)
package
password
bounds（可通过 get_position 来获取其中部分内容）

'''


driver.quit()