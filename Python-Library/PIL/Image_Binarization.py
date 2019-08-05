"""
图片二值化
所谓的图片二值化就是将图片转化为灰度图之后, 再尝试指定一个灰度值(范围0 - 255)为界限,高于这个界限的
灰度直接设置为黑色, 高于这个灰度的直接设置为白色(换句话说,临界值越高, 图片上的黑色越多)

二值化图片的主要作用是消除一些阴影与杂讯的干扰, 突出图像中物体(人的轮廓),所以在人物抠图,识别验证码方面有应用(当然还有其它的应用)

但是要注意的事这个临界的灰度值不是一成不变的,可能这个临界在一张图片上能很好的分离到需要的东西,在另一张图片上
就不起作用,所以这个临界值可能需要动态去查找直到满足需要为止
"""

from PIL import Image

if __name__ == '__main__':
    image = Image.open('./sample.jpg')
    image.show()
    image = image.convert('L')  # 先将图片转成灰度
    image.show()
    threshold = 80  # 设置转换值, 一般来说转换值越高, 图片
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    image = image.point(table, '1')
    image.show()
