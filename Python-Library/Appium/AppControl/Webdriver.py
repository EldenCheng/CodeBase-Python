from appium import webdriver


driver = None

param = {
    'ios': {
            'deviceName': 'iPhone Xs',
            'devicePlatform': 'iOS',
            'platformVersion': '12',
            'udid': '00008020-0002259E3628002E',
            # 'host': 'http://127.0.0.1',
            # 'p': '4723',
            # 'bp': '4724',
            # 'system_port': '8100'
    },
    'android': {
        'deviceName': 'SamsungNote8',
        'devicePlatform': 'Android',
        'platformVersion': '8',
        'udid': 'ce05171555e9e40f037e',
    }
             }

appPackage = {
    'fake_location': 'com.lerist.fakelocation',
    'chrome': "com.android.chrome",
    'settings': 'com.android.settings',
    'gmail': 'com.google.android.gm',
    'bunny': 'com.fisher_price.android',
    'ios_bunny': 'com.fisher-price.smart-connect',
}
appActivity = {
    'fake_location': '.ui.activity.MainActivity',
    'chrome': "com.google.android.apps.chrome.Main",
    'settings': '.Settings',
    'gmail': '.ConversationListActivityGmail',
    'gmail_wel': '.welcome.WelcomeTourActivity',
    'bunny': 'com.mattel.cartwheel.ui.activity.MainView'
}

appBundleId = {'chrome': 'com.google.chrome.ios',
               'gmail': 'com.google.Gmail',
               'safari': 'com.apple.mobilesafari',
               'settings': 'com.apple.Preferences',
               'bunny': 'com.fisher-price.smart-connect',}


def create_webdriver(platform, bundle_id=None, package=None):

    desired_caps = dict()
    if platform.lower() == 'ios':
        desired_caps['automationName'] = 'XCUITest'  # Xcode8.2以上无UIAutomation,需使用XCUITest
        desired_caps['platformName'] = param[platform.lower()]['devicePlatform']  # 系统平台
        desired_caps['platformVersion'] = param[platform.lower()]['platformVersion']  # 系统版本
        desired_caps['deviceName'] = param[platform.lower()]['deviceName']  # 机型名称
        desired_caps['bundleId'] = appBundleId[bundle_id]  # App的bundleID
        desired_caps['wdaLocalPort'] = '8100'  # 指定不同的端口,如8100,8900 以此参数实现多设备执行,不指定时默认为8100
        # desired_caps['app']= os.path.abspath('/XXX/XXX.app') #使用此参数时，无需使用bundleID;会卸载原有的包，安装指定路径的app
        desired_caps['udid'] = param[platform.lower()]['udid']
    else:
        desired_caps['automationName'] = 'uiautomator2'  # Xcode8.2以上无UIAutomation,需使用XCUITest
        desired_caps['platformName'] = param[platform.lower()]['devicePlatform']  # 系统平台
        desired_caps['platformVersion'] = param[platform.lower()]['platformVersion']  # 系统版本
        desired_caps['deviceName'] = param[platform.lower()]['deviceName']  # 机型名称
        desired_caps['appPackage'] = appPackage[package]
        desired_caps['appActivity'] = appActivity[package]
        desired_caps["newCommandTimeout"] = 3600
        desired_caps["recreateChromeDriverSessions"] = True
        desired_caps["autoGrantPermissions"] = True
        desired_caps['noReset'] = True

    return webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_capabilities=desired_caps)
