from appium import webdriver
import unittest
from selenium.common.exceptions import  NoSuchElementException
import time


class Find_And_Open_App(unittest.TestCase):
    def setUp(self):
        print("初始化")
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '5.0'
        desired_caps['deviceName'] = 'a36963f6'
        desired_caps['appPackage'] = 'com.sec.android.app.launcher'
        desired_caps['appActivity'] = 'com.android.launcher2.Launcher'
        desired_caps['unicodeKeyboard'] = 'true'
        desired_caps['resetKeyboard'] = 'true'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub',desired_caps)

    def tearDown(self):
        print("结束")
        self.driver.quit()
    def getSize(self):
        '''获取当前手机的分辨率'''
        size = self.driver.get_window_size()
        x = size['width']
        y = size['height']
        return (x,y)
    def SwipeLeft(self):
        size = self.getSize()
        startX = int(size[0] * 0.8)
        startY = int(size[1] * 0.5)
        endX = int(size[0] * 0.1)
        self.driver.swipe(startX,startY,endX,startY,1000)

    def testFindAndOpen(self):
        self.driver.implicitly_wait(30)
        print("开始测试")
        #click All_App button
        self.driver.find_element_by_id('com.sec.android.app.launcher:id/home_allAppsIcon').click()
        print("开始查找豆瓣App")
        #find douban(豆瓣) icon
        while 1:
            try:
                douban_icon = self.driver.find_element_by_android_uiautomator('new UiSelector().text("豆瓣")')
                if douban_icon.is_displayed():
                    #click icon to open app
                    douban_icon.click()
                    break
                else:
                    self.SwipeLeft()
            except NoSuchElementException :
                str1 = self.driver.page_source
                self.SwipeLeft()
                time.sleep(2)
                str2 = self.driver.page_source
                if str1 == str2:
                    break


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Find_And_Open_App)
    unittest.TextTestRunner(verbosity=2).run(suite)


