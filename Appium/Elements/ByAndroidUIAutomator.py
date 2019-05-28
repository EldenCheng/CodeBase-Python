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

'''
1. UI Automator locator是调用了Android SDK的内容, 所有具体的类文档可以参考
   https://developer.android.com/reference/android/support/test/uiautomator/UiSelector.html
2. 使用UI Automator locator, 在UI Automator Viewer里见到的所有元素的属性都可以用来查找元素, 
   但对应的方法名不一定与UI Automator Viewer里是一样的,所以具体还是要参看上面的连接
'''

driver.find_element_by_android_uiautomator("new UiSelector().text(\"7\")").click()

driver.find_element(MobileBy.ANDROID_UIAUTOMATOR, "new UiSelector().text(\"+\").clickable(true)").click()

driver.find_element(MobileBy.ANDROID_UIAUTOMATOR, "new UiSelector().text(\"6\").clickable(true).index(5)").click()

driver.find_element(MobileBy.ANDROID_UIAUTOMATOR, "new UiSelector().resourceId(\"com.android.calculator2:id/digit_3\")").click()

driver.find_element(MobileBy.ANDROID_UIAUTOMATOR, "new UiSelector().description(\"equals\")").click()

time.sleep(10)

driver.quit()

