"""
matplotlib也支持图像的存取与显示, 并且和OpenCV相比起来, 对于 一般的二维矩阵的可视化要方便很多
"""
import matplotlib.pyplot as plt

if __name__ == '__main__':
    plt.figure("A simple picture")
    simple_img = plt.imread('sample.jpg')
    plt.imshow(simple_img)

    fig = plt.figure("Auto Normalized Visualization")
    ax0 = fig.add_subplot(121)
    navigate_img = 1 - simple_img  # 生成图像的负片
    ax0.imshow(navigate_img)
    plt.show()

