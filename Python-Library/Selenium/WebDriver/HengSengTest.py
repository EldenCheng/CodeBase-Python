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
driver.get("https://bank.hangseng.com/1/2/home")
time.sleep(60)

driver.maximize_window()

time.sleep(3)

#print(driver.title)

#WH =driver.window_handles

#for i in WH:
#    print(str(i))
try:
    #Link = driver.find_element(By.CSS_SELECTOR, "a.rvp_homePageV01_a3")
    Btn = driver.find_element(By.CSS_SELECTOR, "a.rvp_btnShowHideLogon")
    Personal = driver.find_element(By.CSS_SELECTOR, ".rvp_btnPersonal")
    #BtnContenter = driver.find_element(By.CSS_SELECTOR, ".rvp_container")
    #print(Btn.get_attribute("href"))
    #print(Link.get_attribute("title"))
    for i in range(20):
        Btn.click()
        time.sleep(3)
        print("2nd Level menu displayed: " + str(Personal.is_displayed()))
        if Personal.is_displayed() == True:
            Personal.click()
            break
        else:
            continue
    #alert = driver.switch_to.alert()
    #time.sleep(3)
    #alert.accept()
    time.sleep(20)

    print(driver.title)

    driver.switch_to.window(driver.window_handles[1])

    print(driver.title)

except Exception as msg:
    print(msg)

#driver.quit()