# 还未想到一个比较好的自动分配方式, 先手工分配设备到设备组

# 每一个测试需要两台手机, 一个负责发消息, 一个负责收消息, 一对设备会开启一个线程
caps_list = [
    (
        dict(
            platformName='Android',
            deviceName="Galaxy S23 FE 9VQR",
            platformVersion='13',
            udid='R3CW70H9VQR',
            appPackage='com.android.settings',
            appActivity='.Settings',
            noReset=True
        ),  # sender
        dict(
            platformName='Android',
            deviceName="Galaxy S23 FE 9MQB",
            platformVersion='13',
            udid='R3CW70H9MQB',
            appPackage='com.android.settings',
            appActivity='.Settings',
            noReset=True
        )  # receiver
    ),  # 第一对设备
    (
        dict(
            platformName='Android',
            deviceName="Galaxy S23 FE 9MSN",
            platformVersion='13',
            udid='R3CW70H9MSN',
            appPackage='com.android.settings',
            appActivity='.Settings',
            noReset=True
        ),
        dict(
            platformName='Android',
            deviceName="Galaxy S23 FE 9VKF",
            platformVersion='13',
            udid='R3CW70H9VKF',
            appPackage='com.android.settings',
            appActivity='.Settings',
            noReset=True
        )
    ),  # 第二对设备
]
