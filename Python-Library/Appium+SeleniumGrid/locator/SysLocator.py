#!/usr/bin/env python3
# encoding: utf-8
"""
@version: v1.0
@author: WESOFT
"""

from appium.webdriver.common.appiumby import AppiumBy

from locator.AppBase import selector, scrollable

app_package = {
    'google_map': 'com.google.android.apps.maps',
    'fake_gps': 'com.incorporateapps.fakegps.fre',
    'settings': 'com.android.settings',
    'had': 'com.ynashk.had',
}

app_activity = {
    'google_map': 'com.google.android.maps.MapsActivity',
    'fake_gps': 'com.incorporateapps.fakegps.fre.Maps',
    'settings': 'com.android.settings.DevelopmentSettings',
    'had': 'com.ynashk.had.activity.Login$_7779',
}

permission_popup = {
    'allow': selector(['resourceIdMatches(".*button.*")', 'textMatches("(?i)允許.*")']),
    'pair': selector(['resourceIdMatches(".*button.*")', 'textMatches("(?i)配對.*")']),
}

settings = {
    'nothing_en': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("%s")' % 'Nothing'),
    'nothing_zh': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("%s")' % '无'),
    'None': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("%s")' % 'None'),
    'FakeGPS_Free': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("{0}")'.format('FakeGPS Free')),
    'FakeGPS_Free_package_name': (
        AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("{0}")'.format(app_package['fake_gps'])),
    'fake_location': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("{0}")'.format('Fake Location')),
    'select_mock_app_en': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("%s")' % 'Mock'),
    'select_mock_app_zh': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("%s")' % '模拟位置'),
    'select_text_zh': '选择模拟位置信息应用',
    'select_text_en': 'Select mock location app',

    # *** Date and time setting ***
    'datetime_menu_btn': scrollable('textMatches(".*Date and time.*")'),
    'automatic_datetime_switch': selector('resourceId("android:id/switch_widget")'),
    '24hr_switch': selector(['resourceId("android:id/switch_widget")', 'instance(1)']),
    'set_time_btn': selector('textMatches("Set time")'),
    'timer_section': lambda idx=1: (AppiumBy.XPATH, '//android.widget.NumberPicker[%s]' % idx),
    'hour_picker': (AppiumBy.XPATH, '//android.widget.NumberPicker[1]/android.widget.EditText'),
    'minute_picker': (AppiumBy.XPATH, '//android.widget.NumberPicker[2]/android.widget.EditText'),
    'ampm_margin': selector('resourceId("android:id/sem_timepicker_ampm_picker_margin_left")'),
    'ampm_picker': (AppiumBy.XPATH, '//*[@resource-id="android:id/sem_timepicker_layout"]/android.widget.NumberPicker'),
    'done_btn': selector('textMatches("Done")'),
    'set_date_btn': selector('textMatches("Set date")'),
    'current_month': (AppiumBy.ID, 'android:id/sem_datepicker_calendar_header_text'),
    'previous_month': (AppiumBy.ID, 'android:id/sem_datepicker_calendar_header_prev_button'),
    'next_month': (AppiumBy.ID, 'android:id/sem_datepicker_calendar_header_next_button'),
    'date_section': lambda month, day: (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().descriptionContains("{month} {day}")'),

    # pixel date and time
    'pixel_time': scrollable('textMatches(".*Languages, gestures, time, backup.*")'),
    'pixel_date_and_time': scrollable('textMatches("^Date & time$")'),
    'pixel_24hr_switch': (AppiumBy.XPATH,
                          '//android.widget.TextView[@text="Use 24-hour format"]/../following-sibling::android.widget.LinearLayout/android.widget.Switch'),
    'pixel_set_time_btn': selector('textMatches("^Time$")'),
    'pixel_toggle_mode': (AppiumBy.ID, 'android:id/toggle_mode'),  # 点击切换为键盘输入
    'pixel_hour': (AppiumBy.ID, 'android:id/input_hour'),
    'pixel_min': (AppiumBy.ID, 'android:id/input_minute'),
    'pixel_ampm_picker': selector('className("android.widget.Spinner")'),
    'pixel_ampm_item': lambda item: selector(f'text("{item}")'),
    'pixel_done_btn': selector('textMatches("OK")'),
    'pixel_set_date_btn': selector('textMatches("^Date$")'),
    'pixel_previous_month': (AppiumBy.ID, 'android:id/prev'),
    'pixel_next_month': (AppiumBy.ID, 'android:id/next'),
    'pixel_date_section': lambda d: selector(f'text("{d}")'),
}

fake_location = {
    'menu_btn': (AppiumBy.ACCESSIBILITY_ID, 'Open navigation drawer'),
    'start_to_fake': (AppiumBy.ID, 'com.lerist.fakelocation:id/f_fakeloc_tv_service_switch'),
    'add_btn': (AppiumBy.ID, 'com.lerist.fakelocation:id/fab'),
    'current_coords': (AppiumBy.ID, 'com.lerist.fakelocation:id/f_fakeloc_tv_current_latlong'),
    'running_mode': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("{0}")'.format('运行模式')),
    'no_root_mode': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("{0}")'.format('NOROOT')),
    'root_mode': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("{0}")'.format('ROOT（推荐）')),
    'permission_allow': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("{0}")'.format('允许')),
    'permission_allow_id': (AppiumBy.ID, 'com.android.packageinstaller:id/dialog_container'),
    'title_choose_location': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("{0}")'.format('选择位置')),
    'search_btn': (AppiumBy.ID, 'com.lerist.fakelocation:id/m_item_search'),
    'search_box': (AppiumBy.ID, 'com.lerist.fakelocation:id/l_search_panel_et_input'),
    'confirm_btn': (AppiumBy.ID, 'com.lerist.fakelocation:id/a_map_btn_done'),
    'back_btn': (AppiumBy.ACCESSIBILITY_ID, '转到上一层级'),
    'update_next_time': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("{0}")'.format('下次再说')),
    'forward_toset': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("{0}")'.format('前往设置')),
    'get_permission': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("{0}")'.format('前往授权')),

    # 通用元素-提示框&提示框的确认取消按钮
    'native_dialog': (AppiumBy.ID, 'android:id/parentPanel'),
    'prompt_dialog': (AppiumBy.ID, 'com.lerist.fakelocation:id/parentPanel'),
    'dialog_confirm_btn': (AppiumBy.ID, 'android:id/button1'),
    'dialog_cancel_btn': (AppiumBy.ID, 'android:id/button2'),
}


Coords = {
    'Sydney': (-33.880028, 151.180284),
}

via = {
    'ok_btn_xpath_en': (AppiumBy.XPATH, '//android.widget.Button[@text="{0}"]'.format('OK')),
    'ok_btn_xpath_zh': (AppiumBy.XPATH, '//android.widget.Button[@text="{0}"]'.format('确认')),
    'permission_allow_xpath_en': (AppiumBy.XPATH, '//android.widget.Button[@text="{0}"]'.format('Allow')),
    'permission_allow_xpath_zh': (AppiumBy.ANDROID_UIAUTOMATOR, '//android.widget.Button[@text="{0}"]'.format('允许')),
    'Home_btn': (AppiumBy.XPATH, '//android.widget.ImageView[@content-desc="主页"]'),
    'search_box': (AppiumBy.ID, 'search_input'),
    'search_submit_btn': (AppiumBy.ID, 'search_submit'),
    'input_city_box': (AppiumBy.ID, 'input_city'),
    'city_confirm': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("{0}")'.format('确定')),
    'city_cancel': (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("{0}")'.format('取消')),
}

BaiduApi_coords = {
    'create_map': 'http://api.map.baidu.com/lbsapi/createmap/index.html',  # cm
    'get_coords': 'http://api.map.baidu.com/lbsapi/getpoint/index.html',  # gc
    'cm_input_site_editbox': (AppiumBy.ID, 'input_site'),
    'submit_btn': (AppiumBy.XPATH, '//android.view.View[@text=\'{0}\']'.format('查找')),
    'address_not_found_text': (
        AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("{0}")'.format('没有检索到')),
    'cm_longitude': (AppiumBy.ID, 'input_x'),
    'cm_latitude': (AppiumBy.ID, 'input_y'),
}
