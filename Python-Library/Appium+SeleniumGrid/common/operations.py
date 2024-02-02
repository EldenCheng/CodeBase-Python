import time

from appium.options.android import UiAutomator2Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy


class MobileOperations(object):

    def __init__(self, url, ops):
        self.remote_url = url
        self.options = ops
        self.driver = None

    def connect(self):
        """
        :return: driver
        """
        try:
            self.driver = webdriver.Remote(self.remote_url, options=UiAutomator2Options().load_capabilities(self.options))
            return self.driver
        except Exception as msg:
            print(msg)

    def get_element(self, locator_type: str, element_locator: str, approach: str = None, timeout: float = 10):
        """
        查找element
        :param locator_type: element的定位方式
        :param element_locator: element的具体定位参数
        :param timeout: 等待时间，默认30秒
        :param approach
        :return: element
        """
        # timeout = timeout if timeout else 120 if self.param['devicePlatform'].lower() in ['android', 'chrome'] else 10
        try:
            if approach == 'p':
                return WebDriverWait(self.driver, timeout, 0.5).until(ec.presence_of_element_located(
                    (locator_type, element_locator)))
            else:
                return WebDriverWait(self.driver, timeout, 0.5).until(ec.visibility_of_element_located(
                    (locator_type, element_locator)))

        except TimeoutException:
            raise Exception("Element not found: " + element_locator)
        except WebDriverException as webmsg:
            raise Exception(webmsg)
        except Exception as msg:
            raise Exception(msg)

    def find_element(self, locator_type: str, element_locator: str, approach: str = None, timeout: float = 3, direct_find = False) -> bool:
        """
        判断元素是否存在
        :param element_locator: 元素的id，name等
        :param locator_type: 定位的方式
        :param timeout : 等待时间，默认为10s
        :param approach: 检查元素的方式
        :return: flag(True or False)
        """
        try:
            if direct_find:
                self.driver.find_element(locator_type, element_locator)
            else:
                if approach == 'p':
                    WebDriverWait(self.driver, timeout, 0.5).until(ec.presence_of_element_located(
                        (locator_type, element_locator)))
                else:
                    WebDriverWait(self.driver, timeout, 0.5).until(ec.visibility_of_element_located(
                        (locator_type, element_locator)))
            flag = True
        except TimeoutException:
            flag = False
        except WebDriverException as webmsg:
            raise Exception(webmsg)
        except Exception as msg:
            raise Exception(msg)
        return flag

    def is_element_text_appear(self, locator, check_text, approach=None, timeout=10, interval=1):

        start_time = time.time()
        if approach == 'p':
            locator = locator + (approach,)

        for i in range(0, int(timeout / interval)):
            if self.is_element_text_contains(locator, check_text, approach):
                return True
            if round(time.time() - start_time) > timeout:
                # print("Wait too long")
                return False
            time.sleep(interval)
        else:
            return False

    def is_element_text_contains(self, locator, check_text, approach=None, debug=False):

        if approach == 'p':
            locator = locator + (approach,)
        if debug:
            # logger.info(self.driver.page_source)
            display_text = self.element_text(locator).strip()
            # print("The text want to check is ", check_text)
            print("The text on the device is ", display_text)
            return True if check_text in display_text else False
        else:
            return True if check_text in self.element_text(locator).strip() else False

    def element_text(self, locator):

        element = self.get_element(*locator)
        text = element.text.strip()
        return text
