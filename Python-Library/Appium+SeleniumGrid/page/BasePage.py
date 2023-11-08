from common.operations import MobileOperations


class BasePage(MobileOperations):
    def __init__(self, url, ops):
        super(BasePage, self).__init__(url, ops)
        # self.driver = driver if driver else self.driver

    def back_to_start_page(self):
        return True


