"""
scikit-image is a collection of algorithms for image processing. It is available free of charge and free of restriction.
We pride ourselves on high-quality, peer-reviewed code, written by an active community of volunteers.

安装方法 pip install scikit-image
"""
import skimage as ski
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # The skimage.data submodule provides a set of functions returning example images,
    # that can be used to get started quickly on using scikit-image’s functions
    # 实际上就是一些内置的示例图, 可以用来熟悉这个库
    camera = ski.data.camera() # Gray-level “camera” image.Can be used for segmentation and denoising examples.

    # This image shows several coins outlined against a gray background. It is especially useful in,
    # e.g. segmentation tests, where individual objects need to be identified against a background.
    # The background shares enough grey levels with the coins that a simple segmentation is not sufficient.
    # 包含很多枚排列整齐的, 形状大概相同的硬币图片
    coins = ski.data.coins() # Greek coins from Pompeii.

    # 除了使用自带的图片库之外, 还可以读取磁盘上的图片, 读取后会将图片转换成一个numpy矩阵
    desk = ski.io.imread("Pics/desk1.JPG")
    desk_gray = ski.io.imread("Pics/desk1.JPG", as_gray=True) # 直接获得灰度图

    # 读取后就可以获取一些图像的属性
    print("分辨率: ", desk.shape) # 彩色的图像有额外的通道数据, 比如这个图像就有3个通道(红, 绿与蓝)
    print("分辨率: ", desk_gray.shape)  #
    print("图像的大小(size): ", desk.size) # 好像不太准
    # Retrieving statistical information about image intensity values:
    # 强度值??
    print("Min: ", desk.min())
    print("Max: ", desk.max())
    print("Mean ", desk.mean())

    # IO方面, 除了保存为文件, 需要使用其它库来输出
    plt.imshow(coins)
    plt.show()

    # 保存文件
    ski.io.imsave("Pics/save_pic.jpg", coins)


