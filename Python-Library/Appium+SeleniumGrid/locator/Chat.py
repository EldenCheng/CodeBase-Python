from appium.webdriver.common.appiumby import AppiumBy
from locator.AppBase import scrollable, selector

sender_screen = {
    'more': (AppiumBy.ACCESSIBILITY_ID, 'More options'),
    'message_input_box': selector('resourceId("com.pelagic.simplebluetoothchat:id/main_outEditText")'),
    # When the client check the voter detail and click next step
    'send_btn': selector('resourceId("com.pelagic.simplebluetoothchat:id/main_chatSendImageView")'),
    'clear_chat_btn': selector('resourceId("com.pelagic.simplebluetoothchat:id/title").text("Clear Chat")'),
}

receiver_screen = {
    'more': (AppiumBy.ACCESSIBILITY_ID, 'More options'),
    'last_message': (AppiumBy.XPATH, '(//android.widget.TextView[@resource-id="com.pelagic.simplebluetoothchat:id/text_message_body"])[last()]'),
    'message_by_text': lambda msg : scrollable(f'text("{msg}")'),  # 通过滚动屏幕查找msg
    'clear_chat_btn': selector('resourceId("com.pelagic.simplebluetoothchat:id/title").text("Clear Chat")'),
}

dialog = {
        'OK': selector(['resourceIdMatches(".*button.*")', 'textMatches("(?i)OK.*")']),
        'NO': selector(['resourceIdMatches(".*button.*")', 'textMatches("(?i)NO.*")']),
}
