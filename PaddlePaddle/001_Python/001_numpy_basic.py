"""
numpy(Nuerical Python Extension)是一个用于科学计算的Python包
"""

import numpy as np
import time

if __name__ == "__main__":
    '''
    numpy中的array
    array是numpy中的最基础的数据结构, 它像Python中的list一样也支持下标操作,但numpy中的array能支持一些数学运算, 对多维数组的支持也
    更加好
    '''
    a = [1, 2, 3, 4, -1, -2, -3, -4]
    b = np.array(a)  # 将数组转化为numpy中的array类型
    print("numpy的array的对象类型: ", type(b))
    print("使用下标获取元素b[0]: ", b[0])
    print("获取array的大小b.shape: ", b.shape)  # shape参数表示array的大小, 这里是(4,)
    print("获取array中最大值所有的位置b.argmax: ", b.argmax())  # 获得array中最大值的索引(位置),这里是3(因为数组下标从0开始计算)
    print("获取array中的最大值b.max: ", b.max())  # 获得array中的最大值, 这里是4
    print("获取array中所有元素的平均值: ", b.mean())  # 获得array中的平均值, 这里是2.5

    '''
    numpy中的基础数学运算
    numpy中有一些进行基础数学运算的静态方法, 对比起Python中对应的方法, 最大的不同是numpy中的基础数学运算方法支持numpy中的array的类型作为
    运算对你
    '''
    print("绝对值运算: ", np.abs(b))
    print("次方运算: ", np.power(b, 2))
    print("开方运算: ", np.sqrt(abs(b)))  # 负数开方为虚数, sqrt方法会报错, 所以先求绝对值再开方
    print("标准差运算: ", np.std(b))

    '''
    numpy中的random
    numpy中的random方法与Python中的random都是用来生成随机数的,但numpy的random支持生成随机数的方法比Python的random多
    '''
    np.random.seed(42)  # 设置随机数种子, 种子一样, 基本上生成的随机数都一样
    print("产生一个元素介于0-1之间的随机浮点数: ", np.random.random())
    print("产生一个1X3, 元素介于0-1之间的随机值(浮点)的array: ", np.random.rand(1, 3))
    print("在一个已存在的array中随机选择4个数(选出的数有可能重复): ", np.random.choice(b, 4))
    print("在一个已存在的array中随机选择4个数(选出的数不能重复): ", np.random.choice(b, 4, replace=False))
    print("打乱一个已存在的array中的元素顺序并生成一个新的array: ", np.random.permutation(b))

    '''
    numpy中的向量化
    numpy中处理向量化的数据比处理没有向量化的数据快得多,所以在可能的情况下我们都应该将数据向量化
    '''

    # 初始化两个1000000给的随机向量v1, v2用于矩阵相乘
    v1 = np.random.rand(1000000)
    v2 = np.random.rand(1000000)
    v = 0

    # 矩阵相乘非向量版本
    tic = time.time()
    for i in range(1000000):
        v += v1[i] * v2[i]
    toc = time.time()
    print("非向量化用时: {0} ms".format(str((toc-tic)*1000)))

    # 矩阵相乘向量版本
    tic = time.time()
    v = np.dot(v1, v2)  # np.dot方法作用是点乘
    toc = time.time()
    print("向量化用时: {0} ms".format(str((toc-tic)*1000)))


