from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome("../Webdriver/chromedriver.exe")
driver.implicitly_wait(10)

driver.get("http://www.wesoft.com")

menu = driver.find_element_by_css_selector("li#menu-item-21")

hidden_submenu = driver.find_element_by_css_selector("li#menu-item-40")

ActionChains(driver).move_to_element(menu).click(hidden_submenu).perform()
