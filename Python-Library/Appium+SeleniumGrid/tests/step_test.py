from data.constant import hub_url
from data.mobile_info import devices_group1, devices_group3
from test_cases.case001 import test_steps

if __name__ == '__main__':
    # device = devices_group1[0]
    # test_steps(device['monitor_name'], device['client_name'], device['monitor_ops'], device['client_ops'], hub_url)
    device = devices_group3[0]
    id_cards = ["Y219000-A"]
    test_steps(device['name'], device['ops'], hub_url, id_cards)

