import tempfile
import time
import random
import numpy as np
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image

class GS:

    def __init__(self, url):
        self.driver = webdriver.Chrome(executable_path="../WebDriver/chromedriver.exe")
        self.driver.maximize_window()
        self.driver.get(url)
        time.sleep(5)
        title = self.driver.find_element(By.CSS_SELECTOR, 'p.pageHeading')
        time.sleep(2)
        ActionChains(self.driver).move_to_element(title).perform()
        time.sleep(1)
        ActionChains(self.driver).click(title).perform()
        time.sleep(5)
        verify_btn = self.driver.find_element(By.CSS_SELECTOR, 'div.geetest_btn')
        ActionChains(self.driver).move_to_element(verify_btn).perform()
        time.sleep(3)
        ActionChains(self.driver).click(verify_btn).perform()

    def get_driver(self):
        return self.driver

    def slider_auth_code(self, code_type='geetest'):

        if code_type == 'geetest':
            slider = self.driver.find_element(By.CLASS_NAME, 'geetest_slider_button')
            canvas = self.driver.find_element(By.XPATH, '//canvas[@class="geetest_canvas_slice geetest_absolute"]')
            picture1 = self.capture_element_pic(canvas)
            self.driver.execute_script('document.querySelectorAll("canvas")[2].style=""')
            time.sleep(1)
            picture2 = self.capture_element_pic(canvas)

            space_position = self.get_space_position(picture1, picture2)
            tracks = self.generate_tracks(space_position)

            ActionChains(self.driver).click_and_hold(slider).perform()
            for track in tracks['forward_tracks']:
                # print("forward track: ", track)
                ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()
            time.sleep(0.5)
            for back_track in tracks['back_tracks']:
                ActionChains(self.driver).move_by_offset(xoffset=back_track, yoffset=0).perform()
            x_off = random.randint(1, 5)
            ActionChains(self.driver).move_by_offset(xoffset=-x_off, yoffset=0).perform()
            ActionChains(self.driver).move_by_offset(xoffset=x_off, yoffset=0).perform()
            # self.driver.save_screenshot('./Logs/Snapshots/{0}.png'.format(str(time.time())))
            time.sleep(3)
            ActionChains(self.driver).release().perform()
            time.sleep(3)
        else:
            print("print something")

    def get_space_position(self, picture1, picture2):
        # 开始点是根据geetest的常用开始点来定义的
        # 用于避免图像对比时滑块图像本身影响对比结果
        start = 60
        threhold = 60  # 阀值本身也是经验的产物

        # 每一个像素点都要作对比
        for i in range(start, picture1.size[0]):  # 横向
            for j in range(picture1.size[1]):  # 竖向
                rgb1 = picture1.load()[i, j]  # 打开picture1的像素点(一般是一个包含rgb值的元组)
                rgb2 = picture2.load()[i, j]  # 打开picture2的像素点
                # 对比像素点的rgb值的绝对差距
                res1 = abs(rgb1[0] - rgb2[0])
                res2 = abs(rgb1[1] - rgb2[1])
                res3 = abs(rgb1[2] - rgb2[2])

                # 如果rgb值的差距都比阀值要大, 那么表明已经找到阴影的最左边的位置
                # 返回这个位置
                if not (res1 < threhold and res2 < threhold and res3 < threhold):
                    return i
        return i - 10  # 如果整幅图像都找不到阴影,那返回最右边边缘位置-10

    def generate_tracks(self, space):
        # 模拟人工滑动，避免被识别为机器
        additional = random.choice([10, 15, 20, 25, 30])
        print("space postion: {0}".format(space))
        print("additional space: {0}".format(additional))

        space += additional  # 先滑过一点，最后再反着滑动回来

        # 定义向前滑动轨迹
        v = 0  # 初始速度为0
        t = 0.2
        forward_tracks = []
        current = 0
        # mid为减速点,在mid之前,滑块会逐渐加速,在mid之后,滑块会逐渐减速
        # 随机选择一个比例作为滑块减速点
        mid = space * random.choice([3 / 5, 4 / 5, 1 / 2, 2 / 3, 5 / 7])
        print("mid: {0}".format(mid))
        while current < space:
            if current < mid:
                a = 4  # 加速度, 数值越大滑块加速越快
            else:
                a = -5  # 减速度, 数值越大滑块减速越快
            s = v * t + 0.5 * a * (t ** 2)
            v = v + a * t
            current += s
            # s为每次滑动的距离, 在mid前每次滑动的距离会慢慢增加以模拟加速
            # 而经过mid后每次滑动的距离会慢慢减少以模拟减速
            forward_tracks.append(round(s))
        print("forward tracks: {0}".format(forward_tracks))

        # 反着滑动到准确位置
        # 由于定位位置与滑动轨迹多数都会存在误差,而这种误差一般都是会滑过头(即位置会偏右)
        # 所以back_tracks最后一个滑动轨迹我就加大了一点以尝试修正误差
        back_tracks = {10: [-3, -3, -2, -1, -3],
                       15: [-3, -3, -2, -2, -2, -2, -3],
                       20: [-3, -3, -2, -2, -2, -2, -2, -1, -5],
                       25: [-3, -3, -2, -2, -4, -2, -3, -1, -3, -4],
                       30: [-3, -5, -2, -2, -4, -2, -5, -1, -3, -5]}

        # 使用numpy来获得forward_tracks的所有元素的和
        # 然后获得位置与元素和的差
        f = np.array(forward_tracks)
        final_end_position = f.sum()
        different = final_end_position - space
        print("different: {0}".format(different))

        # 打乱back_tracks的轨迹顺序
        b = np.array(back_tracks[additional])
        final_back_tracks = list(np.random.permutation(b))

        # 有差就把差加回forward_tracks
        if different != 0:
            final_back_tracks.append(-different)

        print("final back tracks: {0}".format(final_back_tracks))
        return {'forward_tracks': forward_tracks, 'back_tracks': final_back_tracks}

    def capture_element_pic(self, element, save_path=None):

        left = element.location['x']
        top = element.location['y']
        pic_width = element.location['x'] + element.size['width']
        pic_height = element.location['y'] + element.size['height']
        full_screen_temp = tempfile.mktemp(suffix='.png')
        self.driver.save_screenshot(full_screen_temp)
        picture = Image.open(full_screen_temp)
        picture = picture.crop((left, top, pic_width, pic_height))
        if save_path:
            picture.save(save_path)
            return save_path
        else:
            return picture

    def close(self):
        self.driver.quit()

if __name__ == '__main__':
    gs = GS("https://www.globalsources.com/")
    driver = gs.get_driver()
    time.sleep(10)
    for retry in range(3):
        gs.slider_auth_code()
        try:
            time.sleep(5)
            driver.find_element(By.CSS_SELECTOR, 'div.GS_searchType')
            break
        except Exception as msg:
            continue

    time.sleep(10)
    gs.close()