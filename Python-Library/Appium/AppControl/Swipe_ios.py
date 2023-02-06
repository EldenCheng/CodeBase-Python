import time
from Appium.AppControl import Webdriver

if __name__ == '__main__':

    driver = Webdriver.create_webdriver(platform='ios', bundle_id='gmail')
    time.sleep(3)
    # iOS原生不支持W3C标准滚屏操作, 所以只能指定滚屏的方向, 不能指定滚动多少个像素
    # 一样来说一次滚动就是一个屏幕的距离
    driver.execute_script("mobile: swipe", {"direction": "down"})  # 要注意手机上方向与屏幕运动方向相反的

    # 尝试使用page source对比实现一直向下滚动
    # 原理是如果滚动到底, 两次滚动之后的页面应该保持不变
    # 但实际上是不可行的, 因为iOS中获取到的page source包括手机的时间, 所以page source怎么都不会完全一样
    # ps1 = driver.page_source
    # while True:
    #     driver.execute_script("mobile: swipe", {"direction": "up"})
    #     time.sleep(2)
    #     ps2 = driver.page_source
    #     if ps1 == ps2:
    #         break
    #     else:
    #         ps1 = ps2
    time.sleep(3)

    driver.quit()

