import time
from queue import Queue

from data.constant import hub_url
from locator.AppBase import appPackage
from page.BasePage import BasePage


class MixPage(BasePage):
    pass


def test_steps(data_list, sender_caps, receiver_caps, message_queue: Queue = None):
    sender = MixPage(hub_url, sender_caps)
    receiver = MixPage(hub_url, receiver_caps)

    sender_driver = sender.connect()
    receiver_driver = receiver.connect()

    sender_driver.activate_app(appPackage['bluetooth_chat'])
    receiver_driver.activate_app(appPackage['bluetooth_chat'])
    time.sleep(5)

    # Start page

    time.sleep(5)
    sender_driver.quit()
    receiver_driver.quit()


