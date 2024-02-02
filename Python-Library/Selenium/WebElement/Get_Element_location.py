import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

driver =webdriver.Chrome(executable_path='../WebDriver/chromedriver.exe')
driver.implicitly_wait(10)

if __name__ == '__main__':
    #打开网页并登录
    driver.get("http://www.baidu.com")

    # driver.maximize_window()

    time.sleep(5)

    title_img = driver.find_element(By.CSS_SELECTOR, "img.index-logo-src")

    print(title_img.location)

    ActionChains(driver).move_to_element(title_img).click(title_img).perform()

    # driver.close()