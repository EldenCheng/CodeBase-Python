import os

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

# 这个命令就跟在菜单中强制关闭App一样
os.system('adb shell "am force-stop ' + desired_caps['appPackage'] + '"')