import time

from selenium import webdriver

driver = webdriver.Firefox(executable_path="../WebDriver/geckodriver.exe")
driver.implicitly_wait(10)

if __name__ == '__main__':

    # 打开网页并登录
    driver.get("https://www.baidu.com")

    # Selenium does not support set the CSS Style directly, we can use JavaScript to do this

    JScript = "document.getElementById('su').style.display = 'none';"  # Hide the button on Home page

    driver.execute_script(JScript)

    time.sleep(5)

    # 又或者

    element = driver.find_element_by_id('su')

    attribute_name = 'style'

    value = 'display: block;'

    driver.execute_script("arguments[0].setAttribute(arguments[1],arguments[2])", element, attribute_name, value)

    driver.quit()
