import os

from PIL import Image

import imagehash


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

    @staticmethod
    def same_as_by_hash(target_image, sample_image, percent, hashtype="ahash"):

        hash1 = str(Image_Compare.get_image_hash(hashtype, target_image))
        hash2 = str(Image_Compare.get_image_hash(hashtype, sample_image))

        n = 0
        # hash长度不同则返回-1代表传参出错
        if len(hash1) != len(hash2):
            print("Hash code occurred error!")
            return False
        # 遍历判断
        for i in range(len(hash1)):
            # 不相等则n计数+1，n最终为相似度
            if hash1[i] != hash2[i]:
                n = n + 1
        print("The difference percentage of \"" + hashtype + "\" between two images are: %d%%" % int(n/(len(hash1))*100))

        if int(n/(len(hash1))*100) <= percent:
            return True
        else:
            return False


if __name__ == "__main__":

    # print("The hash of first image: ", Image_Compare.get_image_hash("ahash", r".\testimages\0.png"))
    # print("The hash of second image: ", Image_Compare.get_image_hash("ahash", r".\testimages\1_2.png"))
    Image_Compare.same_as_by_hash(r".\testimages\0.png", r".\testimages\1.png", 90, "phash")



