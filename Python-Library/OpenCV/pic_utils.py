import cv2
import numpy as np
import time

import pyguetzli
import mozjpeg_lossless_optimization
from PIL import Image


class CompressImage:

    @staticmethod
    def compress(pic_path: str, target_path: str, chinese=False, method: str = 'm', size: float = 0.5, quality: int = 50):
        """
        使用Google的guetzli库来压缩图片, 注意这个库只支持jpeg并且比较慢
        :param pic_path: 相片的Path对象实例
        :param quality: 图片压缩质量
        :return:
        """
        try:
            print("Reducing pic {0} size...".format(pic_path))
            begin_time = time.time()
            # print("path: ", pic_path)
            
            if chinese:
                img = Image.open(pic_path)
                (width, height) = img.size
                resize_img = img.resize((int(width * size), int(height * size)))
                resize_img.save(target_path, quality=quality)
            else:
                pic = cv2.imread(pic_path)
                height, width = pic.shape[:2]  # 获取原始分辨率
                resize_pic = cv2.resize(pic, (int(width * size), int(height * size)))  # 缩小图片
                cv2.imwrite(target_path, resize_pic, [int(cv2.IMWRITE_JPEG_QUALITY), quality])  # 按照质量设置保存图片

            # print("Reduce pic by opencv, used: ".format(pic_path), int(time.time() - begin_time))
            if method:  # 设置是否需要额外压缩
                rb = open(str(target_path), 'rb').read()  # 压缩图片需要二进制数据
                if method == "g":  # 使用google pyguetzli压缩, 效果大概可以压缩到原图1/4, 已经缩小并降低质量的图都要1分钟左右
                    
                    optimized_jpeg = pyguetzli.process_jpeg_bytes(rb, quality=quality)  # 将图片压缩后获得新的二进制数据

                elif method == "m":  # mozila的压缩方法压缩率低, 只能大约压缩5%的体积 但快, 基本不用额外时间
                    
                    optimized_jpeg = mozjpeg_lossless_optimization.optimize(rb)  

                # rb.close() 二进制读取不能close
                wb = open(str(target_path), 'wb')
                wb.write(optimized_jpeg)
                # wb.close()
            print("pic {0} totally used: ".format(pic_path), int(time.time() - begin_time))
        except Exception as msg:
            print(msg)
            # raise Exception(msg)

