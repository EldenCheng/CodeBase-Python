import time
from Appium.AppControl import Webdriver

if __name__ == '__main__':

    driver = Webdriver.create_webdriver(platform='ios', bundle_id='bunny')
    time.sleep(3)
    # 好像在iOS上要先通过Appium launch的App, Appium才有它的session id可以访问它
    # 但Appium自带的launch_app方法只支持重新launch desired_caps里指定的app
    # 所以这里直接使用webdriver语句来尝试打开另一个App
    # args = {
    #     'bundleId': Webdriver.appBundleId['gmail']
    # }
    # driver.execute_script('mobile: launchApp', args)
    # time.sleep(5)
    # driver.activate_app(Webdriver.appBundleId['bunny'])
    # time.sleep(3)
    driver.close_app()
    time.sleep(3)
    try:
        driver.activate_app(Webdriver.appBundleId['bunny'])
    except Exception as msg:
        print("Close app后, 对应的App session就关闭了, Appium就访问不了这个App")
        print("或者说Close app后, 内存里已经没有这个App的数据了, 所以就访问不了")
        print(msg)

    time.sleep(10)
    driver.quit()


