from selenium import webdriver

driver =webdriver.Firefox()
driver.implicitly_wait(10)


#打开网页并登录
driver.get("http://www.baidu.com")

#Selenium does not support set the CSS Style directly, we can use JavaScript to do this

JScript = "document.getElementById('su').style.display = 'none';" #Hide the button on Home page

driver.execute_script(JScript)
