import time
from appium.webdriver.common.appiumby import AppiumBy
from code.operations import MobileOperations


def test_steps(remote_url, ops, device_name):
    print(f"{device_name} thread created")
    mobile = MobileOperations(device_name, remote_url, ops)
    driver = mobile.connect()
    print(f"{device_name} driver created")
    time.sleep(5)
    driver.activate_app("com.sec.android.app.clockpackage")
    time.sleep(5)
    alarm_item = mobile.get_element(AppiumBy.XPATH, '//*[contains(@content-desc, "ALARM") or contains(@content-desc, "Alarm")]')
    world_clock_item = mobile.get_element(AppiumBy.XPATH, '//*[contains(@content-desc, "WORLD CLOCK") or contains(@content-desc, "World clock")]')
    # print(f"{device_name} element found")
    for i in range(0, 4):
        alarm_item.click()
        time.sleep(1)
        world_clock_item.click()
    # print(f"{device_name} element clicked")
    time.sleep(5)
    driver.save_screenshot(f"./screen_shot_{device_name}.png")
    time.sleep(5)
    driver.terminate_app("com.sec.android.app.clockpackage")
    time.sleep(5)
    driver.quit()