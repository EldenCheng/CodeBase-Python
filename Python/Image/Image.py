#!/usr/bin/env python3
# encoding: utf-8
"""
@version: v1.0
@author: WESOFT
"""

import colorsys
import glob
import logging
import os
import platform
import time
from pathlib import Path

import aircv as ac
import cv2
import numpy as np
from PIL import ImageDraw, Image, ImageChops, ImageFont
# from aip import AipOcr
# from skimage import measure

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))


def cut_picture(pic_path: [str, Path], box: tuple, save_path: [str, Path]):
    """
    根据提供的4元组定义左，上，右和下像素坐标裁剪图片，然后保存
    :param pic_path: 图片的路径
    :param box: 裁剪矩形，作为（左，上，右，下）元组
    :param save_path: 裁剪图片之后保存的路径
    :return:
    """
    image = Image.open(pic_path)
    cut = image.crop(box)
    cut.save(save_path)


def image_compare(pic: [str, Path], base_pic: [str, Path], pic_name: str):
    """
    图片对比，如果与baseline图片对比一致则返回None，不一致则返回Not None
    :param pic: 需要对比的图片路径
    :param base_pic: Baseline的图片路径
    :param pic_name: 图片后缀, 如需对比Sony_Z5_button_red.png, 则pic_name为"button_red"
    :return: None或者Not None
    """
    result = black_or_b(Image.open(pic).convert('RGBA'), Image.open(base_pic).convert('RGBA'))
    if result is not None:
        raise Exception('%s image compare fail' % pic_name)


def black_or_b(a, b, opacity=0.80):
    diff = ImageChops.difference(a, b)

    if diff.getbbox():
        diff = diff.convert('L')

        thresholded_diff = diff
        for repeat in range(3):
            thresholded_diff = ImageChops.add(thresholded_diff, thresholded_diff)
        size = diff.size
        mask = new_gray(size, int(255 * opacity))
        shade = new_gray(size, 0)
        new = a.copy()
        new.paste(shade, mask=mask)

        new.paste(b, mask=thresholded_diff)
        return new


def new_gray(size: tuple, color: int):
    img = Image.new('L', size)
    dr = ImageDraw.Draw(img)
    dr.rectangle((0, 0) + size, color)
    return img


def same_as_by_pixel(target_image: [str, Path], sample_image: [str, Path], percent: [int,float], to_gray=True, debug=False):
    """
    用pixel-to-pixel对传入的图片进行对比
    :param target_image: 目标图片的路径
    :param sample_image: 对比图片的路径
    :param percent: 容差，int
    :param to_gray: 要不要先转换成灰度图，int
    :return: True: 图片相同，False：图片不相同
    """
    n = 0
    img1 = cv2.imread(target_image)
    img2 = cv2.imread(sample_image)
    if to_gray:
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    if img1.shape == img2.shape:
        height, width = img1.shape
        for line in range(height):
            for pixel in range(width):
                if img1[line][pixel] != img2[line][pixel]:
                    n = n + 1

        if debug:
            logging.info("difference: %f%%" % float(n / float(height * width) * 100))
        if n /float(height * width) * 100 <= percent:
            return True
        else:
            return False
    else:
        logging.info("size not the same")
        return False


def get_match_pos(source_path: [str, Path], template_path: [str, Path]):
    """
    根据局部图片在屏幕截图中匹配对应区域
    :param source_path: 运行时屏幕截图路径
    :param template_path: 模板图片路径
    :return: 屏幕截图中匹配区域的中心点坐标
    """
    try:
        source_img = cv2.imread(source_path)
        template_img = cv2.imread(template_path)
        h, w = template_img.shape[:-1]
        res = cv2.matchTemplate(source_img, template_img, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        left_top = max_loc  # 左上角
        return int(left_top[0] + w / 2), int(left_top[1] + h / 2)
    except Exception as msg:
        raise Exception(msg)


def rectangle(source_path: [str, Path], rect: dict, file_name=None):
    """
    根据坐标在图片中画出一个红色矩形
    :param source_path: 原图片路径
    :param rect: 需要画红色边框的元素的坐标字典, 用element.rect获取
    :param file_name: 新图片输出文件名，生成在原图片同一目录，为空是覆盖源文件
    :return:
    """
    try:
        source_img = Image.open(source_path)
        if rect['height'] < 500 or rect['width'] < 500:
            width = 3
        else:
            width = 9
        draw = ImageDraw.Draw(source_img, 'RGBA')
        draw.line([rect['x'], rect['y'], rect['x'], rect['y'] + rect['height']], fill=(255, 0, 0, 128), width=width)
        draw.line([rect['x'], rect['y'], rect['x'] + rect['width'], rect['y']], fill=(255, 0, 0, 128), width=width)
        draw.line([rect['x'] + rect['width'], rect['y'] + rect['height'], rect['x'], rect['y'] + rect['height']],
                  fill=(255, 0, 0, 128), width=width)
        draw.line([rect['x'] + rect['width'], rect['y'] + rect['height'], rect['x'] + rect['width'], rect['y']],
                  fill=(255, 0, 0, 128), width=width)
        if file_name:
            source_img.save(str(Path(source_path).parent / Path(file_name)))
        else:
            source_img.save(source_path.split('.png')[0] + '_rect.png')
    except Exception as msg:
        raise Exception(msg)


def to_gif(filename_prefix: str):
    """
    将多张相同前缀文件名的png图片合并成gif
    :param filename_prefix: 文件名前缀,
    例如传入"swire3_Dataset1_step1_Fail"将匹配"swire3_Dataset1_step1_Fail.png"和
    "swire3_Dataset1_step1_Fail_rect.png"
    """
    try:
        img_list = glob.glob(filename_prefix + '*.png')
        images = [Image.open(fn) for fn in img_list]
        images[0].save('%s.gif' % filename_prefix, save_all=True, append_images=images[1:], duration=500, loop=0)
    except Exception as msg:
        raise Exception(msg)


def text_dump(source_path: [str, Path], text: str, xy=(10, 20), font_size=13, file_name=None):
    """
    在图片上输出文字
    :param source_path: 原图片路径
    :param text: 需要输出的字符串
    :param xy: 输出文字的坐标
    :param font_size: 字体大小
    :param file_name: 新图片文件保存路径，为空时覆盖原图
    :return:
    """
    try:
        img = Image.open(source_path)
        draw = ImageDraw.Draw(img, 'RGBA')
        fnt_name = 'Arial Unicode.ttf' if platform.system().lower() == 'darwin' else 'ARIALUNI.TTF'
        fnt = ImageFont.truetype(fnt_name, font_size)
        draw.text(xy, text, fill=(255, 127, 80, 128), font=fnt)
        if file_name:
            img.save(str(Path(source_path).parent / Path(file_name)))
        else:
            img.save(source_path)
    except Exception as msg:
        raise Exception(msg)


def get_dominant_color(image_path: [str, Path]):
    """
    :param image_path: 图片路径
    :return: 返回元组(r, g, b)
    """
    try:
        image = Image.open(image_path)
        image = image.convert('RGB')
        max_score = 0.0001
        dominant_color = None
        for count, (r, g, b) in image.getcolors(image.size[0] * image.size[1]):
            # 转为HSV标准
            saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]
            y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)
            y = (y - 16.0) / (235 - 16)
            # 忽略高亮色
            if y > 0.9:
                continue
            score = (saturation + 0.1) * count
            if score > max_score:
                max_score = score
                dominant_color = (r, g, b)
        return dominant_color
    except Exception as msg:
        raise Exception(msg)


def rgb_to_color(r: int, g: int, b: int, e=True):
    """
    判断元素的颜色, 目前只支持绿色、黄色、红色、灰色、纯白、纯黑
    :param r
    :param g
    :param b
    :param e
    :return: 返回color值
    """
    try:
        color = None
        # print('r,g,b:', r, g, b)
        if (g - r) > 30 and (g - b) > 30:
            color = 'green'
        elif (r - b) > 100 and (g - b) > 100 and ((r - g) < 30 or (g - r) < 30):
            color = 'yellow'
        elif (r - g) > 30 and (r - b) > 30:
            color = 'red'
        elif 253 > r > 85 and 253 > g > 85 and 253 > b > 85 \
                and ((0 <= (r - g) < 10 and 0 <= (r - b) < 10) or (0 <= (g - r) < 10 and 0 <= (g - b) < 10)
                     or (0 <= (b - r) < 10 and 0 <= (b - g) < 10)):
            color = 'grey'
        elif r < 85 and g < 85 and b < 85:
            color = 'black'
        elif r >= 253 and g >= 253 and b >=253:
            color = 'white'
        elif b >=1.25*r and (b-g)>=15 and (abs(g-r) < 85 if g<=85 and r<=85 else g-r>=20):
            color = 'blue'

        if color is None and e:
            raise Exception('Unexpected rgb: {}'.format((r, g, b)))
        # print('Element color:', color)
        return color
    except Exception as msg:
        raise Exception(msg)


def get_text_from_image(image_path: [str, Path], accurate=False, get_coord=False):
    """
    调用百度API进行图片识别
    :param image_path: 文件路径
    :param accurate: 是否高精度识别，默认为FALSE
    :param get_coord: 是否获取文字的坐标，默认为FALSE
    :type accurate: bool
    :return: 图片识别到的文字列表，
    """
    try:
        # 通过百度, 有道, Google等的API实际图像文字识别
        app_id = "BAIDU_APP_ID"
        api_key = "BAIDU_API_KEY"
        secrect_key = "BAIDU_SECRECT_KEY"
        client = AipOcr(app_id, api_key, secrect_key)
        i = open(image_path, 'rb')
        img = i.read()
        if accurate:
            if get_coord:
                message = client.accurate(img)  # 通用文字高精度含位置识别，每天 50 次免费
            else:
                message = client.basicAccurate(img)  # 通用文字高精度识别，每天 500 次免费
        else:
            if get_coord:
                message = client.general(img)  # 通用文字含位置识别，每天 500 次免费
            else:
                message = client.basicGeneral(img)  # 通用文字识别，每天 50 000 次免费,
        all_text = []
        if message:
            for i in message['words_result']:
                if get_coord:
                    all_text.append({'word': i.get('words'), 'location': i.get('location')})
                else:
                    all_text.append(i.get('words'))
        return all_text
    except Exception as msg:
        raise Exception(msg)


def get_coordinate_by_image_identify(source, template, get_rect=False):
    """获取目标图片在原图片中的坐标

    :param source:
    :param template:
    :param get_rect:
    :return: get_rect=True
    """
    try:
        imsrc = ac.imread(template)  # 原始图像
        imsch = ac.imread(source)  # 待查找的部分
        position = ac.find_template(imsrc, imsch)
        if position is not None:
            x, y = position['result']
            rect = position['rectangle']
        else:
            raise Exception("Cannot find the image that you provided.")
        if get_rect:
            return x, y, rect
        else:
            return x, y
    except Exception as msg:
        raise Exception(msg)


def compare_images_use_ssim(target_image, base_image, percent=0.8):
    """

    :param target_image: 目标图片的路径
    :param base_image: 基准图片的路径
    :param percent: 接受的范围，1为两张图片100%相同，0为两张图片完全不同，0.8即两张图片有80%相同即认为是同一张图片
    :return: True/ False
    """
    # load the images
    original = cv2.imread(target_image)
    contrast = cv2.imread(base_image)
    # convert the images to grayscale
    original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    contrast = cv2.cvtColor(contrast, cv2.COLOR_BGR2GRAY)
    same = measure.compare_ssim(original, contrast)
    if same < percent:
        return False
    return True


def __non_zero_average(counting_number):
    r = counting_number.ravel()[np.flatnonzero(counting_number)]
    return sum(r) / len(r)


def get_average_hls(target_image: [str, Path], return_result='all'):
    """
    获取传入图像的色相, 明度与饱和度的平均值
    :param target_image: 目标图片的路径
    :param return_result: 返回值的类型, all = h,l,s全部返回, h = 返回色相平均值, l = 明度平均值, s = 饱和度平均值
    :return:
    """
    '''
    色相(h), 指的是颜色的纯度, 其中, 红色色相值约为120, 黄色色相值约为为90, 绿色色相值为60, 蓝色色相值约为30, 紫色约为150, 
             黑色,白色与灰色不应该获取色相, 只有饱和度与明度; 平均值越接近某一个原色的值, 表明图片整体上更加接近某一个原色
             注: 色相理论中使用的是360度圆环表示不同的颜色, 由于存储的原因, OpenCV中会将实际H作出一定的换算, 所以在OpenCV中获取与某一个
                 颜色的H值在圆环所处的位置不一定一样, 比如红色在色相圆环位置是0度或者360度, 但实际我在OpenCV中获取一张纯红色的图片到的平均
                 H值约为120
    饱和度(s), 指的是颜色的鲜艳程度, 其中, 平均值越小, 表明图片整体上更加接近中性灰色
    明度(l), 指的是颜色的明亮程度, 其中, 平均值越大, 颜色越浅越接近白色, 平均值越小, 颜色越深越接近黑色
    '''
    hls = cv2.cvtColor(cv2.imread(target_image), cv2.COLOR_RGB2HLS)
    h, l, s = cv2.split(hls)
    result = {
        'all': (__non_zero_average(h), __non_zero_average(l), __non_zero_average(s)),
        'h': __non_zero_average(h),
        'l': __non_zero_average(l),
        's': __non_zero_average(s),
    }
    return result.get(return_result, -1)


class ImageCoordinate:
    @staticmethod
    def find_coordinate(search_img, source_img, loop_time=3):
        """判断原始图片中是否存在目标图片

        :param search_img: 待查找图片的路径
        :param source_img: 原始图片的路径
        :param loop_time: 循环次数
        :return: boolean
        """
        try:
            flag = False
            while loop_time > 0:
                source = ac.imread(source_img)  # 原始图像
                search = ac.imread(search_img)  # 待查找的部分
                position = ac.find_template(source, search)
                loop_time -= 1
                if position is not None:
                    flag = True
                    break
                time.sleep(3)
            return flag
        except Exception as msg:
            raise Exception(msg)

    @staticmethod
    def get_coordinate_by_image_identify(search_img, source_img, get_rect=False):
        """获取目标图片在原始图片中的坐标

        :param search_img: 待查找图片的路径
        :param source_img: 原始图片的路径
        :param get_rect: 是否返回待查找图片的四角坐标 (左上, 左下, 右上, 右下)
        :return: 中心点坐标，get_rect为True时返回四角坐标
        """
        try:
            source = ac.imread(source_img)  # 原始图像
            search = ac.imread(search_img)  # 待查找的部分
            position = ac.find_template(source, search)
            if position is not None:
                x, y = position['result']
                rect = position['rectangle']
            else:
                raise Exception("Cannot find the image that you provided.")
            if get_rect:
                return x, y, rect
            else:
                return x, y
        except Exception as msg:
            raise Exception(msg)

    def get_coordinates_by_image_identify(self, search_img, source_img, get_rect=False):
        """
        通过图像识别来查找全部符合条件的待查找图片的坐标
        :param search_img: 待查找图片的路径
        :param source_img: 原始图片的路径
        :param get_rect: 是否返回待查找图片的四角坐标 (左上, 左下, 右上, 右下)
        :return:
        所有符合条件的图片坐标列表
        例如：
        get_rect=False -> [(960.5, 243.5), (960.5, 243.5),...]
        get_rect=True -> [{'center': (x,y), 'rectangle': ((x,y),(x,y),(x,y),(x,y))}, ...]）
        """
        try:
            source = ac.imread(source_img)  # 原始图像
            search = ac.imread(search_img)  # 待查找的部分

            positions = ac.find_all_template(source, search)
            cor = []
            if positions is not None:
                for position in positions:
                    x, y = position['result']
                    rect = position['rectangle']
                    if get_rect:
                        cor.append({'center': (x, y), 'rectangle': rect})
                    else:
                        cor.append((x, y))
            else:
                raise Exception("Cannot find the images that you provided.")
            return cor
        except Exception as msg:
            raise Exception(msg)

