from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


driver =webdriver.Firefox()
driver.implicitly_wait(10)


#打开网页并登录
driver.get("http://www.baidu.com")


#将JavaScript的变量返回到Python，不过没什么用，因为Python不会等待JavaScript执行完就会执行下一句，所以除非是即时赋值，
#不然的话实际上等Java Script的值返回的时候，Python语句已经不会再赋值给变量了，所以暂时来说，下面注释的部分是必然出错的
#或者可以用WebDriverWait的unit来实现，这个要试验后才能确定
JScript = "var s='Hello World'; return s"

s = driver.execute_script(JScript)

print(s)

'''
JScript = "var code =prompt('Hello World'); return code;"

s = driver.execute_async_script(JScript)

WebDriverWait(driver, 20, 1).until_not(EC.alert_is_present())

print(s)
'''

#下面这种做法一样不行
#JScript = "var code =prompt('Hello World'); return code;"

#WebDriverWait(driver,20,0.5).until(lambda x: x.execute_script(JScript))

#print(s)

#这样也不行
#JScript = "var code =prompt('Hello World'); setTimeout('return code', 10000);"

#driver.execute_script(JScript)

#print(s)

#将Python的变量引入Javascript
s = "Hello World!"

JScript = "alert('%s');" % s #要注意，这里引入的就算是字符串变量，也要加引号

driver.execute_script(JScript)

WebDriverWait(driver, 20, 1).until_not(EC.alert_is_present()) #等待弹出对话框关闭

print(s)

#使用Java script  定位