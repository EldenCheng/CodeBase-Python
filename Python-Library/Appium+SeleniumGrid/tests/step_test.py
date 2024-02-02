from data.constant import hub_url
from data.mobile_by_group import devices_group1
from test_cases.case001 import test_steps

if __name__ == '__main__':
    # device = devices_group1[0]
    # test_steps(device['monitor_name'], device['client_name'], device['monitor_ops'], device['client_ops'], hub_url)
    device = devices_group1[0]
    data_list = [
        "Hello",
        "I'm Elden",
        "How are you"
    ]
    test_steps(data_list, device['sender_caps'], device['receiver_caps'])

