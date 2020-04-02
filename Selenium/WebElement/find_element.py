from selenium import webdriver
from selenium.webdriver.common.by import By


if __name__ == '__main__':
    driver = webdriver.Firefox(executable_path="../WebDriver/geckodriver.exe")
    driver.implicitly_wait(10)

    # 打开网页并登录
    driver.get("http://www.baidu.com")

    # 先找到父节点
    news_container = driver.find_element(By.CSS_SELECTOR, "div#u1")

    # 然后从父节点开始查找子节点
    news_title = news_container.find_element(By.CSS_SELECTOR, 'a#virus-2020')

    print(news_title.text)
