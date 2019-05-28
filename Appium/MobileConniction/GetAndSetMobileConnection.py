from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.connectiontype import ConnectionType

import time

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0'
desired_caps['deviceName'] = 'Android Emulator'
desired_caps['appPackage'] = 'com.android.calculator2'
desired_caps['appActivity'] = '.Calculator'

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

# 这个方法只能在Android 7.0+以下使用
# Set network
driver.set_network_connection(ConnectionType.AIRPLANE_MODE)

# get network
print(driver.network_connection) # it would return int type, like 0, 1, 2, 004BasicTypeOverall, 6
print(ConnectionType(driver.network_connection).name) # it would return mode name, like AIRPLANE_MODE, WIFI_ONLY