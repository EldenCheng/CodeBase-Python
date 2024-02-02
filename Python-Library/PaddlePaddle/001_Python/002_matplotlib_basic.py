"""
matplotlib是Python中最常用的可视化工具之一, 可以非常方便地创建海量类型2D图表与一些基本的3D图表
"""

import numpy as np
import matplotlib.pyplot as plt

def func(x):
    """
    目标函数: y = x ^ 2
    :param x:
    :return:
    """
    return np.square(x)

def dfunc(x):
    """
    目标函数一阶导数也即是偏导数 dy/dx = 2 * x
    :param x:
    :return:
    """
    return 2 * x

def gradient_descent(x_start, df, epochs, learning_rate):
    """
    梯度下降法,给定起始点与目标函数的一阶导数, 求在epochs次迭代中x的更新值
    :param x_start: x的起始点
    :param df:
    :param epochs: 迭代周期
    :param learning_rate: 学习率
    :return: xs在每次迭代后的位置, 长度为epochs + 1
    """
    theta_x = np.zeros(epochs + 1)  # 返回一个指定长度为(epochs +1)的,所有元素为0的array
    temp_x = x_start
    theta_x[0] = temp_x
    for i in range(epochs):
        deri_x = df(temp_x)
        delta = -deri_x * learning_rate
        temp_x = temp_x + delta
        theta_x[i+1] = temp_x
    return theta_x


def mat_plot():
    line_x = np.linspace(-5, 5, 100)  # 生成一个线性(一维)的array, 元素数值范围-5至5, 包含100个元素
    line_y = func(line_x)

    x_start = -5
    epochs = 5
    lr = 0.3
    x = gradient_descent(x_start, dfunc, epochs, lr)

    color = 'r'

    plt.plot(line_x, line_y, c='b')  # 画线, 由于y是x的平方, 所以图像应该就是一个平方函数的图像
    plt.plot(x, func(x), c='g', label='lr={0}'.format(str(lr)))  # 带图例画线, 这是梯度下降法的图像
    plt.scatter(x, func(x), c='r')  # 画点, 这是梯度下降法计算的那几个点
    plt.legend()  # 在图中显示图例
    plt.show()  # 显示图像


if __name__ == "__main__":

    mat_plot()
