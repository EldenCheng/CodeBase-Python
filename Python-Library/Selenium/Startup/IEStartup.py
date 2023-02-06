# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

#IE有保护模式，如果使用selenium调用IE，要先将IE的保护模式关闭，否则报错
#解决办法是IE选项设置的安全页中，4个区域的启用保护模式的勾选都去掉（或都勾上）
#其他可能的问题有IE的代理服务器设置被打勾了需要去掉勾选，进程里有IEDRIVERSERVER.EXE的进程没有杀掉等等。
driver =webdriver.Ie(".\\Webdrivers\\IEDriverServer.exe")
driver.implicitly_wait(10)

driver.get("http://192.168.8.253")