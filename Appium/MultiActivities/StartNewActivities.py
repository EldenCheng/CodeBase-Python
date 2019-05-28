#coding=utf-8
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '7.1.1'
desired_caps['deviceName'] = 'Android Emulator'
desired_caps['appPackage'] = 'com.android.calculator2'
desired_caps['appActivity'] = '.Calculator'

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

time.sleep(1)

# 切换之前按一下Home button显得更自然,不是必须步骤
driver.press_keycode(3)

time.sleep(2)

# 打开另一个新的App
driver.start_activity('com.google.android.apps.messaging', '.ui.ConversationListActivity')

time.sleep(1)

# 新打开的App自动变成当前driver指向的对象,这个与Seleniumg不同,可以直接云Find Eldement
WebDriverWait(driver, 5, 0.5).until(EC.element_to_be_clickable((MobileBy.ANDROID_UIAUTOMATOR, "new UiSelector().description(\"%s\")" % "Start new conversation"))).click()

# 这个方法是关闭desired_caps指定的App而不是当前的App
driver.close_app()

#print(driver.window_handles)

time.sleep(3)

driver.quit()
