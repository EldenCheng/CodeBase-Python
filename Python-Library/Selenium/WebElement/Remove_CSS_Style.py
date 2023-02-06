import time

from selenium import webdriver

driver = webdriver.Firefox(executable_path="../WebDriver/geckodriver.exe")
driver.implicitly_wait(10)

if __name__ == '__main__':
    # 打开网页并登录
    driver.get("https://www.baidu.com")

    element = driver.find_element_by_id('su')

    attribute_name = 'style'

    driver.execute_script("arguments[0].removeAttribute(arguments[1])", element, attribute_name)

    time.sleep(10)

    driver.quit()
