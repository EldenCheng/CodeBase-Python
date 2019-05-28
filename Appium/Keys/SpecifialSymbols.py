#coding=utf-8
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

import time

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '8.1'
desired_caps['deviceName'] = 'Android Emulator'
desired_caps['appPackage'] = 'com.google.android.apps.messaging'
desired_caps['appActivity'] = '.ui.ConversationListActivity'

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

# 如果是双引号",在使用单引号包围起来,对应单引号就相反用双引号包围起来
# 而\号则可以直接使用
txt = '\'"\''

txt2 = "\"'\""

txt3 = txt + txt2

WebDriverWait(driver, 5, 0.5).until(EC.element_to_be_clickable((MobileBy.ANDROID_UIAUTOMATOR, "new UiSelector().description(\"%s\")" % "Start new conversation"))).click()

txtview = WebDriverWait(driver, 5, 0.5).until(EC.element_to_be_clickable((MobileBy.ANDROID_UIAUTOMATOR, "new UiSelector().resourceId(\"%s:id/%s\")" % (desired_caps['appPackage'], "recipient_text_view"))))

driver.set_value(txtview,txt)

time.sleep(2)

driver.set_value(txtview,txt2)

time.sleep(2)

driver.set_value(txtview,txt3)

time.sleep(5)

driver.quit()

'''
    def exchange_symbol(text):

        txt = ""
        for t in text:
            if t == "'":
                txt = txt + "\"'\""
            elif t == '"':
                txt = txt + '\'"\''
            elif t == "`":
                txt = txt + "\'`\'"
            elif t == "(":
                txt = txt + "\'(\'"
            elif t == ")":
                txt = txt + "\')\'"
            elif t == "|":
                txt = txt + "\'|\'"
            elif t == "<":
                txt = txt + "\'<\'"
            elif t == ">":
                txt = txt + "\'>\'"
            elif t == "&":
                txt = txt + '\'&\''
            elif t == ";":
                txt = txt + '\';\''
            else:
                txt = txt + t
        return txt
'''

