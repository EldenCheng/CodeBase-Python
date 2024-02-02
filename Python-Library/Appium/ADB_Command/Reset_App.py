#coding=utf-8
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
import os
import time

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '7.1.1'
desired_caps['deviceName'] = 'Android Emulator'
desired_caps['appPackage'] = 'com.android.calculator2'
desired_caps['appActivity'] = '.Calculator'

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

# 这个命令就跟在菜单中清除App数据的操作一样,会关闭App,清楚cache与Data
os.system('adb shell "pm clear ' + desired_caps['appPackage'] + '"')