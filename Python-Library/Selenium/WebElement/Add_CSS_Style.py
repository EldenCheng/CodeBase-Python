import time

from selenium import webdriver

driver = webdriver.Firefox(executable_path="../WebDriver/geckodriver.exe")
driver.implicitly_wait(10)

if __name__ == '__main__':

    # 打开网页并登录
    driver.get("https://www.baidu.com")

    element = driver.find_element_by_id('su')

    attribute_name = 'style'

    value = 'height: 200px;'

    # 其实这个语句也可以作为Set Attribute(CSS Style)使用
    driver.execute_script("arguments[0].{0}=arguments[1]".format(attribute_name), element, value)

    time.sleep(10)

    driver.quit()
