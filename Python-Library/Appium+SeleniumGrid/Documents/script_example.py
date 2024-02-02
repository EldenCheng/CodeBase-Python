import time

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

if __name__ == '__main__':
    capabilities = dict(
        platformName='Android',
    )
    options = UiAutomator2Options().load_capabilities(capabilities)
    driver = webdriver.Remote('http://localhost:4444', options=options)
    time.sleep(10)
    driver.quit()
