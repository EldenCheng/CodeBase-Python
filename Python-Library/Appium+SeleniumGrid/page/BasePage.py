import time

from common.operations import MobileOperations
from locator.Chat import sender_screen, receiver_screen, dialog


class BasePage(MobileOperations):
    def __init__(self, url, ops):
        super(BasePage, self).__init__(url, ops)
        # self.driver = driver if driver else self.driver

    def clear_chat_history(self, locator):
        self.get_element(*locator['more']).click()
        time.sleep(0.5)
        self.get_element(*locator['clear_chat_btn']).click()
        time.sleep(0.5)
        self.get_element(*dialog['OK']).click()


