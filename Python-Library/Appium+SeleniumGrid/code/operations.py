from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy


class MobileOperations(object):
    """

    """

    def __init__(self, device_name, url, ops):
        self.device_name = device_name
        self.remote_url = url
        self.options = ops
        self.driver = None

    def connect(self):
        """
        :return: driver
        """
        try:
            self.driver = webdriver.Remote(self.remote_url, options=self.options)
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


