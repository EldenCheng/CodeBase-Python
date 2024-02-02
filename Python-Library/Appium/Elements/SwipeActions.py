from appium import webdriver
import unittest
import time

class SwipeAction(unittest.TestCase):
    def setUp(self):
        print("initialization")
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4.4'
        desired_caps['deviceName'] = 'Android Emulator'
        desired_caps['appPackage'] = 'com.fortysevendeg.android.swipelistview'
                                      #com.fortysevendeg.android.swipelistview
        desired_caps['appActivity'] = 'com.fortysevendeg.android.swipelistview.sample.activities.SwipeListViewExampleActivity'
                                      # com.fortysevendeg.android.swipelistview.sample.activities.SwipeListViewExampleActivity
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub',desired_caps)
    def tearDown(self):
        print("Ending")
        #self.driver.quit()
    def getSize(self):
        x = self.driver.get_window_size()['width']
        y = self.driver.get_window_size()['height']
        print(x)
        print(y)
        return (x, y)
    def swipeLeft(self):
        #Swipe from Right to Left.
        size = self.getSize()
        startX = int(size[0] * 0.7)
        startY = int(size[1] * 0.5)
        endX = int(size[0] * 0.3)
        print(startX,':',startY,':',endX)
        self.driver.swipe(startX,startY,endX,startY,3000)
    def swipeRight(self):
        #Swipe from Left to Right.
        size = self.getSize()
        startX = int(size[0] * 0.3)
        startY = int(size[1] * 0.5)
        endX = int(size[0] * 0.7)
        print(startX, ':', startY, ':', endX)
        self.driver.swipe(startX,startY,endX,startY,3000)
    def swipeUp(self):
        #Swipe from Bottom to Top.即页面滚动条向下
        size = self.getSize()
        startX = int(size[0] * 0.5)
        startY = int(size[1] * 0.8)
        endY = int(size[1] * 0.2)
        print(startX, ':', startY, ':', endY)
        self.driver.swipe(startX,startY,startX,endY,3000)
    def swipeDown(self):
        # Swipe from Top to Bottom.即页面滚动条向上
        size = self.getSize()
        startX = int(size[0] * 0.5)
        startY = int(size[1] * 0.2)
        endY = int(size[1] * 0.8)
        print(startX, ':', startY, ':', endY)
        self.driver.swipe(startX, startY, startX, endY,3000)
    def testSwipe(self):
        # 对警报信息进行处理
        #self.driver.implicitly_wait(30)
        # self.driver.find_element_by_class_name('android.widget.CheckBox').click()
        # self.driver.find_element_by_id('android:id/button1').click()
        time.sleep(2)
        self.swipeLeft()
        time.sleep(5)
        self.swipeRight()
        time.sleep(5)
        self.swipeUp()
        time.sleep(5)
        self.swipeDown()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(SwipeAction)
    unittest.TextTestRunner(verbosity=2).run(suite)