# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

if __name__ == '__main__':
    # 注意有时候Chromedriver的版本与Chrome的版本不对的话, 虽然Chromedriver能控制Chrome, 但Chrome option会不起作用
    options = webdriver.ChromeOptions()
    options.headless=True
    driver = webdriver.Chrome(executable_path=r"Webdrivers/chromedriver.exe", chrome_options=options)
    driver.get('https://www.baidu.com')
    driver.quit()

