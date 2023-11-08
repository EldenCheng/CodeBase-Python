from appium.webdriver.common.appiumby import AppiumBy
from locator.AppBase import scrollable, selector

monitor = {
    'home_pic': selector('resourceId("com.ynashk.had:id/vp_advs")'),
    'id_card_pic': selector('resourceId("com.ynashk.had:id/logo")'),
    # When the client check the voter detail and click next step
    'voter_name': selector('resourceId("com.ynashk.had:id/voterChiName")'),
    'vote_to_voter': selector('textMatches("(?i)已向投票人發出的選票.*")'),
}
