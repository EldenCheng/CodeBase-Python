#coding=utf-8
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from appium.webdriver.switch_to import MobileSwitchTo
import time

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '7.1.1'
desired_caps['deviceName'] = 'Android Emulator'
desired_caps['appPackage'] = 'com.google.android.apps.messaging'
desired_caps['appActivity'] = '.ui.ConversationListActivity'

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

cont = driver.contexts

name = cont[0]

#driver.switch_to.


#不知道有什么功能,按照官方的说法是可以在WEBVIEW与NATIVE APP之间转换

