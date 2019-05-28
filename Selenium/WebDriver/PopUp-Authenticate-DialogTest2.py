from selenium import webdriver

# 这个方法要在比较新的Firefox与Chrome上才可以使用
# 当访问一个要求用户名密码才可以access的web服务时
# 可以直接将username与password以下面的格式加入到url里面
# 就可以避免弹出的验证对话框不能被WebDriver捕捉到
driver = webdriver.Chrome(r"..\WebDrivers\chromedriver.exe")
driver.get("http://access3:acc3qw2@infwtcmyuat.aswatson.net/")
driver.implicitly_wait(5)

wndls = driver.window_handles

print(wndls)

#alert = driver.switch_to.alert
#print(alert.text)

print(driver.title)
