#!/usr/bin/env python3
# encoding: utf-8
"""
@version: v1.0
@author: WESOFT
"""

from appium.webdriver.common.appiumby import AppiumBy


def scrollable(locators: [list, str]):
    if isinstance(locators, list):
        return (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().%s)' % '.'.join(locators))
    elif isinstance(locators, str):
        return (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().%s)' % locators)


def selector(locators: [list, str]):
    if isinstance(locators, list):
        return (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().%s' % '.'.join(locators))
    elif isinstance(locators, str):
        return (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().%s' % locators)


appPackage = {
    'chrome': "com.android.chrome",
    'settings': 'com.android.settings',
    'gmail': 'com.google.android.gm',
    'engineering': 'com.fisherprice.engineering',
    'bluetooth_chat': "com.pelagic.simplebluetoothchat",
}

appActivity = {
    'chrome': "com.google.android.apps.chrome.Main",
    'settings': '.Settings',
    'gmail': '.ConversationListActivityGmail',
    'gmail_wel': '.welcome.WelcomeTourActivity',
    'engineering': 'com.fisherprice.engineering.activity.FPMainScreen',
    'bluetooth_chat': "com.pelagic.simplebluetoothchat.ChatActivity",
}

common = {
    'progress_bar': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ProgressBar")'),
    'please_wait': (AppiumBy.ID, 'com.fisher_price.android:id/please_wait'),
    'please_wait_': (AppiumBy.ID, 'android:id/message'),
    "please_wait_com": (AppiumBy.XPATH, '//android.widget.TextView[contains(@resource-id,"com.fisher_price.android:id/please_wait") or contains(@resource-id,"android:id/message")'),
    'banner_text': (AppiumBy.ID, 'com.fisher_price.android:id/banner_text'),  # 类似dashboard的打开蓝牙提醒横幅
    'back_btn': selector(['className("android.widget.ImageView")', 'instance(0)']),
}

dialog = {
    'title': (AppiumBy.XPATH, '//android.widget.ImageView'),
    'content': (AppiumBy.XPATH, '//android.widget.ImageView'),
    'confirm': selector('descriptionMatches("(?i)(ok(ay)?|yes.*|apply.*|confirm.*|^save$|got.*|don.*|'
                        'remove((?!tasks).)*|ready.*|replace|select|exit|^close$|^disable$|^turn on$)")'),
    'cancel': selector('descriptionMatches("(?i)(cancel.*|save and continue)")'),
    'allow': selector('textMatches("(?i)([a]|[A]llow|ok|done|允许|turn on)")'),
    'flutter_allow': selector('descriptionMatches("(?i)([a]|[A]llow|ok|done|允许|turn on)")'),
    'got_it': selector('descriptionMatches("(?i)^got it.*")'),
    'offline': selector('descriptionMatches("(?si).*offline.*")'),
    'close': selector('descriptionMatches("(?i)^close$")'),
}

permission = {
    'title': (AppiumBy.ID, 'com.android.permissioncontroller:id/permission_message'),
    'allow_only': (AppiumBy.ID, 'com.android.permissioncontroller:id/permission_allow_foreground_only_button'),
    'deny': (AppiumBy.ID, 'com.android.permissioncontroller:id/permission_deny_button')
}

android_notification = {
    'clear_btn': selector('descriptionContains("Clear all notifications")'),
}

android_base = {
    'text': lambda value: (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("{0}")'.format(value)),
    'text_contains': lambda value: (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("{0}")'.format(value)),
    'text_view': lambda value: (AppiumBy.XPATH, '//android.widget.TextView[@text="{0}"]'.format(value)),
    'button': lambda value: (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Button").text("{0}")'.format(value)),
    'edittext': lambda value: (AppiumBy.XPATH, '//android.widget.EditText[@text="{0}"]'.format(value)),
    'desc_contains': lambda value: (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("{0}")'.format(value)),  # content-desc属性
}

sys_browser = {
    'chrome_url': (AppiumBy.ID, 'com.android.chrome:id/url_bar'),
    'confirm_download': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textMatches("下载|[Dd]ownload|[Oo][Kk]|确定")'),
    'downloading': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textMatches("正在下载|[Dd]ownloading")'),
    'allow_btn': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textMatches("Allow|允许")'),  # samsung s10
    'later_btn': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textMatches("稍后|[Ll]ater")'),  # samsung s10
    'open_file': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textMatches("打开文件|[Oo]pen")'),  # samsung s10
}
