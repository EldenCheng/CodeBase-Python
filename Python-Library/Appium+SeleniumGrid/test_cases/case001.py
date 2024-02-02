import time
from queue import Queue

from data.constant import hub_url
from locator.AppBase import appPackage
from locator.Chat import sender_screen, receiver_screen
from page.BasePage import BasePage


class MixPage(BasePage):
    pass


def test_steps(data_list, sender_caps, receiver_caps, message_queue: Queue = None):
    sender = MixPage(hub_url, sender_caps)
    receiver = MixPage(hub_url, receiver_caps)

    sender_driver = sender.connect()
    print(f"Sender {sender_caps['deviceName']} is connected")
    receiver_driver = receiver.connect()
    print(f"Receiver {receiver_caps['deviceName']} is connected")

    sender_driver.activate_app(appPackage['bluetooth_chat'])
    receiver_driver.activate_app(appPackage['bluetooth_chat'])
    time.sleep(5)

    for data in data_list:
        # Clear the chat history
        # sender.clear_chat_history(sender_screen)
        # receiver.clear_chat_history(receiver_screen)

        # Sender send message
        # print(f"Sender {sender_caps['deviceName']} want to send {data}")
        sender.get_element(*sender_screen['message_input_box']).clear()
        sender.get_element(*sender_screen['message_input_box']).send_keys(data)
        send_time = time.time()
        sender.get_element(*sender_screen['send_btn']).click()

        # Check message in receiver
        if receiver.is_element_text_appear(receiver_screen['last_message'], data, timeout=10, interval=1):
            spend_time = round(time.time() - send_time, 3)
            result = [time.strftime(f"%H:%M:%S.{time.time_ns() % 1000}", time.localtime()), "Send and receive message", "P", str(spend_time - 1)]
        else:
            result = [time.strftime(f"%H:%M:%S.{time.time_ns() % 1000}", time.localtime()), "Send and receive message", "F", "0"]
        if message_queue:
            message_queue.put(result)
        else:
            print(result)

        time.sleep(5)
    sender_driver.quit()
    receiver_driver.quit()


