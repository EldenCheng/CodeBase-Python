from data import mobile_caps01, mobile_caps02, mobile_caps03

# 一个设备组会开启一个进程
devices_group1 = list()
devices_group2 = list()
devices_group3 = list()

for c in mobile_caps01.caps_list:
    pair_device = {
            "sender_caps": c[0],
            "receiver_caps": c[1],
        }
    devices_group1.append(pair_device)

for c in mobile_caps02.caps_list:
    pair_device = {
            "sender_caps": c[0],
            "receiver_caps": c[1],
        }
    devices_group2.append(pair_device)

for c in mobile_caps03.caps_list:
    pair_device = {
            "sender_caps": c[0],
            "receiver_caps": c[1],
        }
    devices_group3.append(pair_device)


