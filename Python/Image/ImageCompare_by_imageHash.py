import os

from PIL import Image,ImageChops,ImageDraw
from functools import reduce

# 使用pip install opencv-python
# 使用pip install opencv-contrib-python 安装opencv的一些附属方法
import cv2
import numpy as np

# 使用python -mpip install -U matplotlib
from matplotlib import pyplot as plt

import imagehash

PATH = lambda p: os.path.abspath(p)


class Image_Compare(object):

    @staticmethod
    def load_image(image_path):
        #加载目标图片供对比用
        if os.path.isfile(image_path):
            load = Image.open(image_path)
            return load
        else:
            raise Exception("%s is not exist" % image_path)

    @staticmethod
    def get_image_hash(hash_method: str, image_path: str):
        # img = cv2.imread(image_path)
        if hash_method == 'ahash':
            hashfunc = imagehash.average_hash
        elif hash_method == 'phash':
            hashfunc = imagehash.phash
        elif hash_method == 'dhash':
            hashfunc = imagehash.dhash
        elif hash_method == 'whash-haar':
            hashfunc = imagehash.whash
        elif hash_method == 'whash-db4':
            hashfunc = lambda img: imagehash.whash(img, mode='db4')
        try:
            return hashfunc(Image.open(image_path))
        except Exception as e:
            print('Problem:', e, 'with', image_path)



if __name__ == "__main__":

    print("The hash of first image: ", Image_Compare.get_image_hash("ahash", r".\testimages\0.png"))
    print("The hash of second image: ", Image_Compare.get_image_hash("ahash", r".\testimages\1_2.png"))



