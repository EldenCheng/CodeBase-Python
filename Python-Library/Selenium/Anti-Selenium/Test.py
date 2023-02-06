
from selenium.webdriver import Chrome

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
if __name__ == "__main__":
    option = ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = Chrome(executable_path='../WebDriver/chromedriver.exe', options=option)
    driver.get("https://login.taobao.com")
    element = driver.find_element(By.ID, "TPL_username_1")
    element.send_keys("jim")
    driver.close()

    mobile_emulation = {
    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"}

    chrome_options = Options()

    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation) # 这里看清楚了，不是add_argument

    driver = webdriver.Chrome(executable_path='../WebDriver/chromedriver.exe', options=chrome_options)
    # driver.get("https://dun.163.com/trial/jigsaw")
    driver.get('https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html')