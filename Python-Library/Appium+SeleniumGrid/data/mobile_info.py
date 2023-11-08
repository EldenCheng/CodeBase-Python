from appium.options.android import UiAutomator2Options

capabilities_9vqr = dict(
    platformName='Android',
    deviceName="Galaxy S23 FE ",
    platformVersion='13',
    udid='R3CW70H9VQR',
    appPackage='=com.android.settings',
    appActivity='.Settings',
    noReset=True
)

capabilities_9mqb = dict(
    platformName='Android',
    deviceName="Galaxy S23 FE ",
    platformVersion='13',
    udid='R3CW70H9MQB',
    appPackage='=com.android.settings',
    appActivity='.Settings',
    noReset=True
)

capabilities_9msn = dict(
    platformName='Android',
    deviceName="Galaxy S23 FE ",
    platformVersion='13',
    udid='R3CW70H9MSN',
    appPackage='=com.android.settings',
    appActivity='.Settings',
    noReset=True
)

capabilities_9vkf = dict(
    platformName='Android',
    deviceName="Galaxy S23 FE ",
    platformVersion='13',
    udid='R3CW70H9VKF',
    appPackage='=com.android.settings',
    appActivity='.Settings',
    noReset=True
)

devices_group1 = list()

# 每一个测试需要两台手机, 一个负责发消息, 一个负责收消息
cap_list1 = ((capabilities_9vqr, capabilities_9mqb), (capabilities_9msn, capabilities_9vkf))

for c in cap_list1:
    pair_device = {
            "sender_caps": c[0],
            "receiver_caps": c[1],
        }
    devices_group1.append(pair_device)


