import os
import platform
import tempfile
import shutil

from PIL import Image,ImageChops,ImageDraw
from functools import reduce

# 使用pip install opencv-python
# 使用pip install opencv-contrib-python 安装opencv的一些附属方法
import cv2
import numpy as np

# 使用python -mpip install -U matplotlib
from matplotlib import pyplot as plt

PATH = lambda p: os.path.abspath(p)


class Image_Compare(object):

    @staticmethod
    def load_image(image_path):
        #加载目标图片供对比用
        if os.path.isfile(image_path):
            load = Image.open(image_path)
            return load
        else:
            raise Exception("%s is not exist" %image_path)

    '''
    使用PIL获得图像的直方图,然后用一个公式计算两个图像直方图之间的差值,限制比较大,结果也不太准确
    '''
    @staticmethod
    def same_as_by_histogram(target_image, sample_image, percent):
        #对比图片，percent值设为0，则100%相似时返回True，设置的值越大，相差越大
        import math
        import operator

        image1 = Image_Compare.load_image(target_image)
        image2 = Image_Compare.load_image(sample_image)

        size1 = image1.size
        size2 = image2.size


        if (size1[0] * size1[1]) > (size2[0] * size2[1]):
            image1 = image1.resize((size2[0],size2[1]), Image.ANTIALIAS)
        elif (size1[0] * size1[1]) < (size2[0] * size2[1]):
            image2 = image2.resize((size1[0], size1[1]), Image.ANTIALIAS)

        #image1.save(PATH("./resize.png"))

        # 把图像对象转换为直方图数据
        histogram1 = image1.histogram()
        histogram2 = image2.histogram()

        '''
        sqrt:计算平方根，reduce函数：前一次调用的结果和sequence的下一个元素传递给operator.add
        operator.add(x,y)对应表达式：x+y
        这个函数是方差的数学公式：S^2= ∑(X-Y) ^2 / (n-1)
        '''
        differ = math.sqrt(reduce(operator.add, list(map(lambda a,b: (a-b)**2, histogram1, histogram2)))/len(histogram1))

        print("The difference percentage of histogram between two images are: %d%%" % differ)
        if differ <= percent:
            return True
        else:
            return False

    '''
    逐个像素对比,只有原来一模一样的两张图片才有可能相同,就是同一张图片经过转换,可能都会得出不相同的结果
    '''
    @staticmethod
    def same_as_by_pixel(target_image, sample_image, percent):

        n = 0
        img1 = cv2.imread(target_image, 0)
        img2 = cv2.imread(sample_image, 0)
        if img1.shape == img2.shape:
            height, width = img1.shape
            for line in range(height):
                for pixel in range(width):
                    if img1[line][pixel] != img2[line][pixel]:
                        n = n + 1
            # print(float((n/(height*width))))
            print("The difference percentage of pixcel between two images are: %f%%" % float(n/(height*width)*100))
            if float(n/(height*width)*100) <= percent:
                return True
            else:
                return False
        else:
            print("The resolution between two images are different")
            return False

    @staticmethod
    def same_as_by_PIL(target_image, sample_image):
        image1 = Image_Compare.load_image(target_image)
        image2 = Image_Compare.load_image(sample_image)

        #Returns the absolute value of the pixel-by-pixel difference between the two images.
        diff = ImageChops.difference(image1,image2)

        # Calculates the bounding box of the non-zero regions in the image.
        if diff.getbbox():
            #translating a color image to black and white (mode "L")
            diff = diff.convert('L')

            thresholded_diff = diff
            for repeat in range(3):
                #Adds two images, dividing the result by scale and adding the offset.
                thresholded_diff = ImageChops.add(thresholded_diff, thresholded_diff)
                thresholded_diff.save("thresholded_differ_%d.png" % repeat)
            h, w = size = diff.size
            mask = Image_Compare.new_gray(size, int(255 * (0.80)))
            mask.save("mask.png")
            shade = Image_Compare.new_gray(size, 0)
            shade.save("shade.png")
            new = image1.copy()
            new.paste(shade, mask=mask)
            new.paste(image2, mask=thresholded_diff)
            new.save("result.png")
            # 其实上面 if diff.getbbox()后面的语句对于判断照片是否相等无意义
            # 不过这个是某个照片处理方法,可以学学用来做什么的
            return False
        else:
            return True

    @staticmethod
    def new_gray(size, color):
        img = Image.new('L', size)
        dr = ImageDraw.Draw(img)
        dr.rectangle((0, 0) + size, color)
        return img

    @staticmethod
    def same_as_by_OpenCV(target_image, sample_image):
        image1 = cv2.imread(target_image)
        image2 = cv2.imread(sample_image)

        difference = cv2.subtract(image1, image2)

        result = not np.any(difference)  # if difference is all rece it will return False

        if result is True:
            return result
        else:
            cv2.imwrite("result_OpenCV.png", difference)
            return result

    '''
    平均哈希法(aHash)
    此算法是基于比较灰度图每个像素与平均值来实现的

    一般步骤:

        1.缩放图片，一般大小为8*8，64个像素值。
        2.转化为灰度图
        3.计算平均值：计算进行灰度处理后图片的所有像素点的平均值，直接用numpy中的mean()计算即可。
        004BasicTypeOverall.比较像素灰度值：遍历灰度图片每一个像素，如果大于平均值记录为1，否则为0.
        5.得到信息指纹：组合64个bit位，顺序随意保持一致性
        
    By Elden: 在不同的手机分辨率的截图对比下,这个算法得出的结果都是无差异,所以可以看出这个算法对图像差异比较不敏感
    '''
    @staticmethod
    def aHash(img):
        img = cv2.imread(img)
        # 缩放为8*8
        img = cv2.resize(img, (8, 8), interpolation=cv2.INTER_CUBIC)
        # 转换为灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # s为像素和初值为0，hash_str为hash值初值为''
        s = 0
        hash_str = ''
        # 遍历累加求像素和
        for i in range(8):
            for j in range(8):
                s = s + gray[i, j]
        # 求平均灰度
        avg = s / 64
        # 灰度大于平均值为1相反为0生成图片的hash值
        for i in range(8):
            for j in range(8):
                if gray[i, j] > avg:
                    hash_str = hash_str + '1'
                else:
                    hash_str = hash_str + '0'
        return hash_str

    '''
    差值感知算法(dHash算法)
    相比pHash，dHash的速度要快的多，相比aHash，dHash在效率几乎相同的情况下的效果要更好，它是基于渐变实现的。

    步骤：

         1. 缩小图片：收缩到9*8的大小，以便它有72的像素点

         2. 转化为灰度图

         3. 计算差异值：dHash算法工作在相邻像素之间，这样每行9个像素之间产生了8个不同的差异，一共8行，则产生了64个差异值

         004BasicTypeOverall. 获得指纹：如果左边的像素比右边的更亮，则记录为1，否则为0
         
    By Elden: 在不同的手机分辨率的截图对比下,这个算法得出的结果有少量不同,所以可以看出这个算法对图像差异相对aHash与pHash敏感
    '''
    @staticmethod
    def dHash(img):
        img = cv2.imread(img)
        # 缩放8*8
        img = cv2.resize(img, (9, 8), interpolation=cv2.INTER_CUBIC)
        # 转换灰度图
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hash_str = ''
        # 每行前一个像素大于后一个像素为1，相反为0，生成哈希
        for i in range(8):
            for j in range(8):
                if gray[i, j] > gray[i, j + 1]:
                    hash_str = hash_str + '1'
                else:
                    hash_str = hash_str + '0'
        return hash_str

    '''
    感知哈希算法(pHash)
    平均哈希算法过于严格，不够精确，更适合搜索缩略图，为了获得更精确的结果可以选择感知哈希算法，它采用的是DCT（离散余弦变换）来降低频率的方法

    一般步骤：

          1. 缩小图片：32 * 32是一个较好的大小，这样方便DCT计算
          2. 转化为灰度图
          3. 计算DCT：利用Opencv中提供的dct()方法，注意输入的图像必须是32位浮点型，所以先利用numpy中的float32进行转换
          004BasicTypeOverall. 缩小DCT：DCT计算后的矩阵是32 * 32，保留左上角的8 * 8，这些代表的图片的最低频率
          5. 计算平均值：计算缩小DCT后的所有像素点的平均值。
          6. 进一步减小DCT：大于平均值记录为1，反之记录为0.
          7. 得到信息指纹：组合64个信息位，顺序随意保持一致性。

    By Elden: 在不同的手机分辨率的截图对比下,这个算法得出的结果无差异,但如果截图较小,误差就比较大,所以可以看出这个算法比较适合进行全屏对比
    '''
    @staticmethod
    def pHash(img):
        img = cv2.imread(img)
        img = cv2.resize(img, (32, 32))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 将灰度图转为浮点型，再进行dct变换
        dct = cv2.dct(np.float32(gray))
        # 取左上角的8*8，这些代表图片的最低频率
        # 这个操作等价于c++中利用opencv实现的掩码操作
        # 在python中进行掩码操作，可以直接这样取出图像矩阵的某一部分
        dct_roi = dct[0:8, 0:8]
        avreage = np.mean(dct_roi)
        hash_str = ''
        for i in range(dct_roi.shape[0]):
            for j in range(dct_roi.shape[1]):
                if dct_roi[i, j] > avreage:
                    hash_str = hash_str + '1'
                else:
                    hash_str = hash_str + '0'
        return hash_str

    @staticmethod
    def same_as_by_hash(target_image, sample_image, percent, hashtype="ahash"):

        if hashtype == "ahash":
            hash1 = Image_Compare.aHash(target_image)
            hash2 =  Image_Compare.aHash(sample_image)
        elif hashtype == "dhash":
            hash1 = Image_Compare.dHash(target_image)
            hash2 = Image_Compare.dHash(sample_image)
        elif hashtype == "phash":
            hash1 = Image_Compare.pHash(target_image)
            hash2 = Image_Compare.pHash(sample_image)

        #print(hash1)
        #print(hash2)

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

    @staticmethod
    def same_as_by_kaze_bfmatch(im1_path, im2_path, percentage, showimg= False):
        # load the image and convert it to grayscale
        im1 = cv2.imread(im1_path)
        im2 = cv2.imread(im2_path)
        gray1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)

        # initialize the AKAZE descriptor, then detect keypoints and extract
        # local invariant descriptors from the image
        detector = cv2.AKAZE_create()

        # 得到特征点与特征点描述,看上去好像是会得出特征点本身, 与图像中有多少描述符(Descriptor)
        (kps1, descs1) = detector.detectAndCompute(gray1, None)
        (kps2, descs2) = detector.detectAndCompute(gray2, None)

        print("keypoints: {}, descriptors: {}".format(len(kps1), descs1.shape))
        print("keypoints: {}, descriptors: {}".format(len(kps2), descs2.shape))

        # Match the features
        # BFmatcher = BruteForceMatcher 蛮力对比
        # BFMatcher总是尝试所有可能的匹配，从而使得它总能够找到最佳匹配，这也是Brute Force（暴力法）的原始含义
        # BFmatcher的参数可以是NORM_L1, NORM_L2, NORM_HAMMING, NORM_HAMMING2其中之一
        # L1 and L2 norms are preferable choices for SIFT and SURF descriptors,
        # NORM_HAMMING should be used with ORB, BRISK and BRIEF,
        # NORM_HAMMING2 should be used with ORB when WTA_K==3 or 4 (see ORB::ORB constructor description).
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)

        # Match方法与knnMatch方法的差别是knnMatch可以指定k值
        # K = 2 ，即对每个匹配返回两个最近邻描述符，仅当第一个匹配与第二个匹配之间的距离足够小时，才认为这是一个匹配
        # The result of matches = bf.match(des1,des2) line is a list of DMatch objects.
        # This DMatch object has following attributes:
        # DMatch.distance - Distance between descriptors.The lower, the better it is.
        # DMatch.trainIdx - Index of the descriptor in train descriptors
        # DMatch.queryIdx - Index of the descriptor in query descriptors
        # DMatch.imgIdx - Index of the train image.
        matches = bf.knnMatch(descs1,descs2, k=2)    # typo fixed

        # Apply ratio test
        # "1NN/2NN<0.8"，不要诧异你未见过这样一种说法，没错，自己瞎创的一种表述。对上面1NN方法理解了，这个水到渠成。所谓“1NN/2NN<0.8”，
        # 即对于图像im1中的某个SIFT特征点point1，通过在im2图像上所有SIFT关键点查找到
        # 与point1最近的SIFT关键点point21(记该关键点point21到point1的距离为dis1)和次近的关键点point22(记该关键点point22到point1的距离为dis2)，
        # 如果dis1/dis2<0.8，则我们将其视为正确匹配的点对，否则则为错配的点对予以剔除。这种寻找匹配的方法，
        # 由Lowe在其Distinctive image features from scale-invariant keypoints中有说明，当然，0.8这个阈值是可以调整的，
        # 不过一般都采用0.8。
        good = []
        for m,n in matches:
            if m.distance < 0.8 * n.distance:
                good.append([m])
        if showimg is True:
            # cv2.drawMatchesKnn expects list of lists as matches.
            im3 = cv2.drawMatchesKnn(im1, kps1, im2, kps2, good, None, flags=2)
            cv2.imshow("AKAZE matching", im3)
            cv2.waitKey(0)
        #print("match points:", len(matches))
        print("good match points:", len(good))
        print("The percentage of bad match points of \"akaze\" are: %d%%" % int((1 - len(good)/(len(matches)))*100))

        if int((1 - len(good)/(len(matches)))*100) <= percentage:
            return True
        else:
            return False

    @staticmethod
    def same_as_by_sift_flmatch(im1_path, im2_path, percentage, showimg=False):
        # load the image
        im1 = cv2.imread(im1_path)
        im2 = cv2.imread(im2_path)

        orig_image = np.array(im1)
        skewed_image = np.array(im2)

        # 由此可见，SIFT在尺度和旋转变换的情况下效果最好，SURF在亮度变化下匹配效果最好，在模糊方面优于SIFT，
        # 而尺度和旋转的变化不及SIFT，旋转不变上比SIFT差很多。速度上看，SURF是SIFT速度的3倍。
        detector = cv2.xfeatures2d.SIFT_create(400)
        kp1, des1 = detector.detectAndCompute(orig_image, None)
        kp2, des2 = detector.detectAndCompute(skewed_image, None)

        print("keypoints: {}, descriptors: {}".format(len(kp1), des1.shape))
        print("keypoints: {}, descriptors: {}".format(len(kp2), des2.shape))

        # For FLANN based matcher, we need to pass two dictionaries which specifies the algorithm to be used, its
        # related parameters etc.First one is IndexParams.For various algorithms, the information to be passed is
        # explained in FLANN docs.As a summary, for algorithms like SIFT, SURF etc
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)

        # 而FlannBasedMatcher中FLANN的含义是Fast Library forApproximate Nearest Neighbors，
        # 从字面意思可知它是一种近似法，算法更快但是找到的是最近邻近似匹配，
        # 所以当我们需要找到一个相对好的匹配但是不需要最佳匹配的时候往往使用FlannBasedMatcher。
        # 当然也可以通过调整FlannBasedMatcher的参数来提高匹配的精度或者提高算法速度，但是相应地算法速度或者算法精度会受到影响。
        # FLANN stands for Fast Library for Approximate Nearest Neighbors.It contains a collection of
        # algorithms optimized for fast nearest neighbor search in large datasets and for
        # high dimensional features.It works more faster than BFMatcher for large datasets.
        flann = cv2.FlannBasedMatcher(index_params, search_params)

        # K = 2 ，即对每个匹配返回两个最近邻描述符，仅当第一个匹配与第二个匹配之间的距离足够小时，才认为这是一个匹配
        matches = flann.knnMatch(des1, des2, k=2)

        # store all the good matches as per Lowe's ratio test.
        # Apply ratio test
        good = []
        for m, n in matches:
            if m.distance < 0.8 * n.distance:
                good.append([m])

        if showimg is True:
             #cv2.drawMatchesKnn expects list of lists as matches.
            im3 = cv2.drawMatchesKnn(im1, kp1, im2, kp2, good, None, flags=2)
            cv2.imshow("AKAZE matching", im3)
            cv2.waitKey(0)
        #print("match points:", len(matches))
        print("good match points:", len(good))
        print("The percentage of bad match points of \"sift\" are: %d%%" % int((1 - len(good)/(len(matches)))*100))

        if int((1 - len(good)/(len(matches)))*100) <= percentage:
            return True
        else:
            return False

    @staticmethod
    def same_as_by_surf_flmatch(im1_path, im2_path, percentage, showimg=False):
        # load the image
        im1 = cv2.imread(im1_path)
        im2 = cv2.imread(im2_path)

        orig_image = np.array(im1)
        skewed_image = np.array(im2)

        # 由此可见，SIFT在尺度和旋转变换的情况下效果最好，SURF在亮度变化下匹配效果最好，在模糊方面优于SIFT，
        # 而尺度和旋转的变化不及SIFT，旋转不变上比SIFT差很多。速度上看，SURF是SIFT速度的3倍。
        detector = cv2.xfeatures2d.SURF_create(400)
        kp1, des1 = detector.detectAndCompute(orig_image, None)
        kp2, des2 = detector.detectAndCompute(skewed_image, None)

        print("keypoints: {}, descriptors: {}".format(len(kp1), des1.shape))
        print("keypoints: {}, descriptors: {}".format(len(kp2), des2.shape))

        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)

        flann = cv2.FlannBasedMatcher(index_params, search_params)

        matches = flann.knnMatch(des1, des2, k=2)

        good = []
        for m, n in matches:
            if m.distance < 0.8 * n.distance:
                good.append([m])

        if showimg is True:
            # cv2.drawMatchesKnn expects list of lists as matches.
            im3 = cv2.drawMatchesKnn(im1, kp1, im2, kp2, good, None, flags=2)
            cv2.imshow("SURF matching", im3)
            cv2.waitKey(0)
        # print("match points:", len(matches))
        print("good match points:", len(good))
        print("The percentage of bad match points of \" surf \" are: %d%%" % int((1 - len(good) / (len(matches))) * 100))

        if int((1 - len(good) / (len(matches))) * 100) <= percentage:
            return True
        else:
            return False

if __name__ == "__main__":

    '''
    # By Histogram
    print("By using Histogram:")
    print(Image_Compare.same_as_by_histogram(r".\testimages\Screenshot1440P.png", r".\testimages\Screenshot720P.png", 0))
    print(Image_Compare.same_as_by_histogram(r".\testimages\Screenshot1080P.png", r".\testimages\Screenshot1080P.png", 0))
    print(Image_Compare.same_as_by_histogram(r".\testimages\Screenshot1080P.png",r".\testimages\resize1080P.png", 0))
    '''


    # By Pixel, must with the same resolution
    # print("By using Pixel:")
    # print(Image_Compare.same_as_by_pixel(r".\testimages\0942.png",r".\testimages\0943.png", 0))

    # By Pillow internal method
    #print("By using Pillow:")
    #print(Image_Compare.same_as_by_PIL(r".\testimages\Screenshot1440P.png", r".\testimages\Screenshot1080P.png"))
    #print(Image_Compare.same_as_by_pixel2(r".\testimages\Screenshot1080P.png", r".\testimages\Other_Screenshot1080P.png", 0))

    # By OpenCV internal method
    # print("By using OpenCV:")
    # print(Image_Compare.same_as_by_OpenCV(r".\testimages\Screenshot1080P.png",r".\testimages\resize1080P.png"))
    # print(Image_Compare.same_as_by_OpenCV(r".\testimages\Screenshot1080P.png", r".\testimages\Screenshot720P.png"))
    # print(Image_Compare.same_as_by_OpenCV(r".\testimages\Screenshot1440P.png", r".\testimages\Screenshot1080P.png"))
    # print(Image_Compare.same_as_by_OpenCV(r".\testimages\0942.png",r".\testimages\0943.png"))

    '''
    # By aHash
    print("By using aHash:")
    print("1. Using the same screen capture in different resolution:")
    print(Image_Compare.same_as_by_hash(r".\testimages\Screenshot1440P.png",r".\testimages\Screenshot1080P.png", 0))
    print(Image_Compare.same_as_by_hash(r".\testimages\Screenshot1440P.png", r".\testimages\resize1080P.png", 0))
    print(Image_Compare.same_as_by_hash(r".\testimages\Screenshot1440P.png", r".\testimages\Screenshot720P.png", 0))
    print(Image_Compare.same_as_by_hash(r".\testimages\Screenshot1440P.png", r".\testimages\Screenshot360P.png", 0))
    print("2. Using the different screen capture in different resolution:")
    print(Image_Compare.same_as_by_hash(r".\testimages\Screenshot1080P.png", r".\testimages\Other_Screenshot1080P.png", 0))
    print("3. Using the same Element capture in different resolution:")
    print(Image_Compare.same_as_by_hash(r".\testimages\Elementshot_big.png", r".\testimages\Elementshot_small.png", 0))

    # By dHash
    print("By using dHash:")
    print("1. Using the same screen capture in different resolution:")
    print(Image_Compare.same_as_by_hash(r".\testimages\Screenshot1440P.png",r".\testimages\Screenshot1080P.png", 0, "dhash"))
    print(Image_Compare.same_as_by_hash(r".\testimages\Screenshot1440P.png", r".\testimages\resize1080P.png", 0, "dhash"))
    print(Image_Compare.same_as_by_hash(r".\testimages\Screenshot1440P.png", r".\testimages\Screenshot720P.png", 0, "dhash"))
    print(Image_Compare.same_as_by_hash(r".\testimages\Screenshot1440P.png", r".\testimages\Screenshot360P.png", 0, "dhash"))
    print("2. Using the different screen capture in different resolution:")
    print(Image_Compare.same_as_by_hash(r".\testimages\Screenshot1080P.png", r".\testimages\Other_Screenshot1080P.png", 0, "dhash"))
    print("3. Using the same Element capture in different resolution:")
    print(Image_Compare.same_as_by_hash(r".\testimages\Elementshot_big.png", r".\testimages\Elementshot_small.png", 0, "dhash"))

    # By pHash
    print("By using pHash:")
    print("1. Using the same screen capture in different resolution:")
    print(Image_Compare.same_as_by_hash(r".\testimages\Screenshot1440P.png",r".\testimages\Screenshot1080P.png", 0, "phash"))
    print(Image_Compare.same_as_by_hash(r".\testimages\Screenshot1440P.png", r".\testimages\resize1080P.png", 0, "phash"))
    print(Image_Compare.same_as_by_hash(r".\testimages\Screenshot1440P.png", r".\testimages\Screenshot720P.png", 0, "phash"))
    print(Image_Compare.same_as_by_hash(r".\testimages\Screenshot1440P.png", r".\testimages\Screenshot360P.png", 0, "phash"))
    print("2. Using the different screen capture in different resolution:")
    print(Image_Compare.same_as_by_hash(r".\testimages\Screenshot1080P.png", r".\testimages\Other_Screenshot1080P.png", 0, "phash"))
    print("3. Using the same Element capture in different resolution:")
    print(Image_Compare.same_as_by_hash(r".\testimages\Elementshot_big.png", r".\testimages\Elementshot_small.png", 0, "phash"))
    '''

    # print("By using pHash:")
    # print("登录成功:登录中:", Image_Compare.same_as_by_hash(r".\testimages\screen_ele2.png", r".\testimages\0.png", 5,
    #                                     "phash"))
    #
    # print("登录成功:登录成功带圈:", Image_Compare.same_as_by_hash(r".\testimages\screen_ele2.png", r".\testimages\1_1.png", 5,
    #                                     "phash"))
    #
    # print("By using dHash:")
    # print("登录成功:登录中:", Image_Compare.same_as_by_hash(r".\testimages\screen_ele2.png", r".\testimages\0.png", 10,
    #                                     "dhash"))
    #
    # print("登录成功:登录成功带圈:", Image_Compare.same_as_by_hash(r".\testimages\screen_ele2.png", r".\testimages\1_1.png", 10,
    #                                     "dhash"))
    #
    # print("By using aHash:")
    # print("登录成功:登录中:", Image_Compare.same_as_by_hash(r".\testimages\screen_ele2.png", r".\testimages\0.png", 5,
    #                                     "ahash"))
    # print("登录成功:登录成功带圈:", Image_Compare.same_as_by_hash(r".\testimages\screen_ele2.png", r".\testimages\1_1.png", 5,
    #                                     "ahash"))
    #print("By using bfmatch:")
    #print("1. Using the same screen capture in different resolution:")
    #print("1440:1080", Image_Compare.kaze_bfmatch(r".\testimages\Screenshot1440P.png", r".\testimages\Screenshot1080P.png"))

    #print("2. Using the differnet screen capture in same resolution:")
    #print("One:Another:",
    #      Image_Compare.kaze_bfmatch(r".\testimages\Screenshot1080P.png", r".\testimages\Other_Screenshot1080P.png"))
    #print("3. Using an element of the screen capture in same resolution:")
    #print("Ele:Full:",
    #      Image_Compare.kaze_bfmatch(r".\testimages\Elementshot_big.png", r".\testimages\Screenshot1440P.png"))

    # print("4. Using an element and compare with some mask on it:")
    # print("登录成功:登录中:",
    #       Image_Compare.same_as_by_kaze_bfmatch(r".\testimages\screen_ele2.png", r".\testimages\0.png",30))
    # print("登录成功:登录成功带圈:",
    #       Image_Compare.same_as_by_kaze_bfmatch(r".\testimages\screen_ele2.png", r".\testimages\1_1.png",30))
    #
    #
    # print("By using flmatch:")
    #print("1. Using the same screen capture in different resolution:")
    #print("1440:1080:",
    #      Image_Compare.kaze_flmatch(r".\testimages\Screenshot1080P.png", r".\testimages\Screenshot1440P.png", m))
    #print("1440:720:",
    #      Image_Compare.kaze_flmatch(r".\testimages\Screenshot720P.png", r".\testimages\Screenshot1440P.png", m))
    #print("1440:360:",
    #      Image_Compare.kaze_flmatch(r".\testimages\Screenshot360P.png", r".\testimages\Screenshot1440P.png", m))

    #print("2. Using the differnet screen capture in same resolution:")
    #print("One:Another:",
    #      Image_Compare.kaze_flmatch(r".\testimages\Screenshot1080P.png", r".\testimages\Other_Screenshot1080P.png", m))

    #print("3. Using an element of the screen capture in same resolution:")
    #print("Ele:Full:",
    #      Image_Compare.kaze_flmatch(r".\testimages\Elementshot_big.png", r".\testimages\Screenshot1440P.png", m))
    # print("登录成功:登录中-sift:",
    #       Image_Compare.same_as_by_sift_flmatch(r".\testimages\screen_ele2.png", r".\testimages\0.png",30))
    # print("登录成功:登录成功带圈-sift:",
    #       Image_Compare.same_as_by_sift_flmatch(r".\testimages\screen_ele2.png", r".\testimages\1_1.png",30))
    # print("登录成功:登录中-surf:",
    #       Image_Compare.same_as_by_surf_flmatch(r".\testimages\screen_ele2.png", r".\testimages\0.png",30))
    # print("登录成功:登录成功带圈-surf:",
    #       Image_Compare.same_as_by_surf_flmatch(r".\testimages\screen_ele2.png", r".\testimages\1_1.png",30))



