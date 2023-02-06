from selenium import webdriver
from selenium.webdriver.common.by import By

driver =webdriver.Firefox()
driver.implicitly_wait(10)

#打开网页并登录
driver.get("http://www.baidu.com")

url = driver.find_element(By.CSS_SELECTOR, "a[href='http://news.baidu.com']")



url_link = url.get_attribute("href")

#由于JS里获得元素的方法有限,所以我们可以使用先获得元素,然后将元素作为参数传入JS中的方法来实现操作
#获得WebElement的属性值, JS语句里面的arguments[0]代表的是后面传入的参数url,在这里的作用就好像点位符%s, Sd % (s, d)一样的用法
url_value = driver.execute_script("return arguments[0].href;", url)

print(url_value)

#修改WebElement的属性值
driver.execute_script("return arguments[0].href = 'http://map.baidu.com';", url)

url.click()
