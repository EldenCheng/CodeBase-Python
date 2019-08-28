from __future__ import print_function # 将python3中的print特性导入当前版本
"""
人工智能,机器学习与深度学习

实际上的包含关系是人工智能->机器学习->深度学习, 即深度学习是机器学习的一个分支, 而机器学习也是人工智能的一个分支

具体来说, 机器学习是实现人工智能的一个方法, 而深度学习就是机器学习的实现方法之一

按照定义来说, 机器学习是指: 如果一个程序可以在任务T上, 随着经验E的增加,效果P也可以随之增加, 则称这个程序可以从经验中学习;

所以总体来说, 机器学习是一个"训练"算法的方式, 目的是使机器能够向算法传送大量的数据, 并允许算法进行自我调整和改进, 而不是复用具有特定
指令的编码软件例程来完成指定任务. 它要在大数据中寻找一些"模式", 然后在没有过多的人为参与的情况 下, 用这些模式来预测结果, 而这些模式在普通
的统计分析中是看不到的. 机器学习的传统算法包括决策树学习, 推导逻辑规划, 聚类, 分类, 回归, 贝叶斯网络和神经网络等.

传统机器学习最关键的问题是必须依赖给定数据的表示, 而实际上, 在大部分任务中我们很难知道应该提取哪些特征. 例如我们想要在一堆动物的图片中辨认出猫,
通常会试图通过判断胡须,耳朵,尾巴等元素存在与否, 但如果照片中存在很多遮挡物或者猫的姿势改变等, 都会影响机器识别的特征. 在深度学习出现后, 通过其它
较简单的表示来表达复杂的表示, 解决了机器学习的核心问题

深度学习是基于多层神经网络的, 以海量数据为输入的, 规则自学习的方法, 对于图像, 语音这种直接特征不明显的问题, 深度模型能够在大规模训练数据的基础上
取得更好的效果, 由于深度学习需要大量的数据用于训练, 所以图像, 语音和自然语言处理是三个深度学习算法应用最广泛的研究领域

常见的深度学习网络结构有:
1. 全连接网络结构(FC): 这种是最基本的神经网络 / 深度神经网络, 它认为每一层的输入都与上一层的输出有关, 因为输入与输出都是相连的, 所以需要相当数量
   的存储和计算空间
2. 卷积神经网络(CNN): 它是一种专门用于处理具有网络结构的数据的神经网络(例如图像就是一个二维的像素网络). 它与FC不同的地方在于, CNN的上下层神经
   元并不都能直接连接, 而是通过"卷积核"作为中介,通过"核"的共享大大减少了隐含层的参数
3. 循环神经网络(RNN): RNN是一种用于处理序列数据的神经网络(例如音频就是基于时间线的一维时间序列)

常见的深度学习框架有:

CNTK(Microsoft), PaddlePaddle(Baidu), Caffe2(Facebook), TensorFlow(Google), PyTorch(Facebook), MXNet(Amazon)
"""

"""
0. 下面的代码对应的是文章 - 数字识别 
   (https://www.paddlepaddle.org.cn/documentation/docs/zh/1.5/beginners_guide/basics/recognize_digits/README.cn.html)
1. 首先我们可以安装PaddlePaddle包, PaddlePaddle包有分为几个操作系统也有分使用GPU与使用CPU的几个组合, 一般来说我们在Windows平台
   暂时只能使用CPU版本的, 可以使用pip install paddlepaddle来安装
2. 之前的介绍中说过深度学习十分依赖, 所以一般来说入门深度学习的话一般都是练习 MNIST 数据库(http://yann.lecun.com/exdb/mnist/)上的
   手写识别问题。原因是手写识别属于典型的图像分类问题，比较简单，同时MNIST数据集也很完备。MNIST数据集作为一个简单的计算机视觉数据集，
   包含一系列如图1所示的手写数字图片和对应的标签。图片是28x28的像素矩阵，标签则对应着0~9的10个数字。每张图片都经过了大小归一化和居中处理
   本教程中，我们从简单的Softmax回归模型开始，带大家了解手写字符识别，并向大家介绍如何改进模型，利用多层感知机（MLP）和
   卷积神经网络（CNN）优化识别效果。
3. PaddlePaddle在API中提供了自动加载MNIST数据的模块paddle.dataset.mnist。
   加载后的数据位于/home/username/.cache/paddle/dataset/mnist下, 一般来说, 会获得的文件如下:
          文件名称	                  说明
   train-images-idx3-ubyte	训练数据图片，60,000条数据
   train-labels-idx1-ubyte	训练数据标签，60,000条数据
   t10k-images-idx3-ubyte	测试数据图片，10,000条数据
   t10k-labels-idx1-ubyte	测试数据标签，10,000条数据
"""
import os
import matplotlib.pyplot as plt
import numpy
import paddle  # 导入paddle模块
import paddle.fluid as fluid
from paddle.utils.plot import Ploter
from PIL import Image  # 导入图像处理模块


'''
让我们创建一个数据层来读取图像并将其连接到分类网络
Softmax回归：只通过一层简单的以softmax为激活函数的全连接层，就可以得到分类的结果
'''
def softmax_regression(img):  # 生成神经网络的算法1
    """
    定义softmax分类器：一个以softmax为激活函数的全连接层
    Return:
        predict_image -- 分类的结果
    """
    # 我们需要将图像数据输入到分类器中。Paddle为读取数据提供了一个特殊的层layer.data层
    # 输入的原始图像数据，大小为28*28*1
    # img = fluid.layers.data(name='img', shape=[1, 28, 28], dtype='float32')
    # 以softmax为激活函数的全连接层，输出层的大小必须为数字的个数10
    predict = fluid.layers.fc(input=img, size=10, act='softmax')
    return predict


'''
多层感知器：下面代码实现了一个含有两个隐藏层（即全连接层）的多层感知器。其中两个隐藏层的激活函数均采用ReLU，输出层的激活函数用Softmax。
'''
def multilayer_perceptron(img):  # 生成神经网络的算法2
    """
    定义多层感知机分类器：
        含有两个隐藏层（全连接层）的多层感知器
        其中前两个隐藏层的激活函数采用 ReLU，输出层的激活函数用 Softmax
    Return:
        predict_image -- 分类的结果
    """
    # 输入的原始图像数据，大小为28*28*1
    # img = fluid.layers.data(name='img', shape=[1, 28, 28], dtype='float32')
    # 第一个全连接层，激活函数为ReLU
    hidden = fluid.layers.fc(input=img, size=200, act='relu')
    # 第二个全连接层，激活函数为ReLU
    hidden = fluid.layers.fc(input=hidden, size=200, act='relu')
    # 以softmax为激活函数的全连接输出层，输出层的大小必须为数字的个数10 (因为预期要判断的结果是数字0-9)
    prediction = fluid.layers.fc(input=hidden, size=10, act='softmax')
    return prediction


'''
卷积神经网络LeNet-5: 输入的二维图像，首先经过两次卷积层到池化层，再经过全连接层，最后使用以softmax为激活函数的全连接层作为输出层
'''
def convolutional_neural_network(img):  # 生成神经网络的算法3
    """
    定义卷积神经网络分类器：
        输入的二维图像，经过两个卷积-池化层，使用以softmax为激活函数的全连接层作为输出层
    Return:
        predict -- 分类的结果
    """
    # img = fluid.layers.data(name='img', shape=[1, 28, 28], dtype='float32') # 输入的原始图像数据，大小为28*28*1
    # 第一个卷积-池化层
    # 使用20个5*5的滤波器，池化大小为2，池化步长为2，激活函数为Relu
    conv_pool_1 = fluid.nets.simple_img_conv_pool(
        input=img,
        filter_size=5,
        num_filters=20,
        pool_size=2,
        pool_stride=2,
        act="relu")
    conv_pool_1 = fluid.layers.batch_norm(conv_pool_1)
    # 第二个卷积-池化层
    # 使用50个5*5的滤波器，池化大小为2，池化步长为2，激活函数为Relu
    conv_pool_2 = fluid.nets.simple_img_conv_pool(
        input=conv_pool_1,
        filter_size=5,
        num_filters=50,
        pool_size=2,
        pool_stride=2,
        act="relu")

    prediction = fluid.layers.fc(input=conv_pool_2, size=10, act='softmax')  # 以softmax为激活函数的全连接输出层，输出层的大小必须为数字的个数10
    return prediction


'''
Train Program 配置
然后我们需要设置训练程序 train_program。它首先从分类器中进行预测。 在训练期间，它将从预测中计算 avg_cost。
注意: 训练程序应该返回一个数组，第一个返回参数必须是 avg_cost。训练器使用它来计算梯度。
请随意修改代码，测试 Softmax 回归 softmax_regression, MLP 和 卷积神经网络 convolutional neural network 分类器之间的不同结果
'''
def train_program(img, label):  # 调用train_program 获取预测值，损失值
    """
    配置train_program

    Return:
        predict -- 分类的结果
        avg_cost -- 平均损失
        acc -- 分类的准确率
    """
    # 标签层，名称为label,对应输入图片的类别标签
    # label = fluid.layers.data(name='label', shape=[1], dtype='int64')

    # 这里可以使用不同的分类器来试验不同分类器所得出的结果
    # predict = softmax_regression(img) # 取消注释将使用 Softmax回归
    # predict = multilayer_perceptron(img) # 取消注释将使用 多层感知器
    predict = convolutional_neural_network(img)  # 取消注释将使用 LeNet5卷积神经网络

    # 使用类交叉熵函数计算predict和label之间的损失函数
    cost = fluid.layers.cross_entropy(input=predict, label=label)
    # 计算平均损失
    avg_cost = fluid.layers.mean(cost)
    # 计算分类准确率
    acc = fluid.layers.accuracy(input=predict, label=label)
    return predict, [avg_cost, acc]

'''
构建训练过程
现在，我们需要构建一个训练过程。将使用到前面定义的训练程序 train_program, place 和优化器 optimizer,并包含训练迭代、
检查训练期间测试误差以及保存所需要用来预测的模型参数。
'''


def train_test(train_test_program, train_test_feed, train_test_reader):  # 用于测试每个epoch的分类效果

    # 将分类准确率存储在acc_set中
    acc_set = []
    # 将平均损失存储在avg_loss_set中
    avg_loss_set = []
    # 将测试 reader yield 出的每一个数据传入网络中进行训练
    for test_data in train_test_reader():
        acc_np, avg_loss_np = exe.run(
            program=train_test_program,
            feed=train_test_feed.feed(test_data),
            fetch_list=[acc, avg_loss])
        acc_set.append(float(acc_np))
        avg_loss_set.append(float(avg_loss_np))
    # 获得测试数据上的准确率和损失值
    acc_val_mean = numpy.array(acc_set).mean()
    avg_loss_val_mean = numpy.array(avg_loss_set).mean()
    # 返回平均损失值，平均准确率
    return avg_loss_val_mean, acc_val_mean


'''
生成预测输入数据
infer_3.png 是数字 3 的一个示例图像。把它变成一个 numpy 数组以匹配数据feed格式
'''
def load_image(file):
    im = Image.open(file).convert('L')
    im = im.resize((28, 28), Image.ANTIALIAS)
    im = numpy.array(im).reshape(1, 1, 28, 28).astype(numpy.float32)
    im = im / 255.0 * 2.0 - 1.0
    return im


if __name__ == "__main__":

    runing_mode = "Training"  # 设置使用训练模式或者使用识别模式

    '''
    定义网络结构
    '''
    # 该模型运行在单个CPU上
    use_cuda = False  # 如想使用GPU，请设置为 True
    place = fluid.CUDAPlace(0) if use_cuda else fluid.CPUPlace()  # 设置使用GPU或者CPU

    img = fluid.layers.data(name='img', shape=[1, 28, 28], dtype='float32')  # 输入的原始图像数据，大小为28*28*1
    label = fluid.layers.data(name='label', shape=[1], dtype='int64')  # # 标签层，名称为label,对应输入图片的类别标签
    feeder = fluid.DataFeeder(feed_list=[img, label], place=place)  # 告知网络传入的数据分为两部分，第一部分是img值，第二部分是label值

    # 调用train_program 获取预测值，损失值
    # 生成神经网络, 再利用生成后的神经网络计算出损失值与平均损失值
    prediction, [avg_loss, acc] = train_program(img, label)
    '''
    Optimizer Function 配置
    在下面的 Adam optimizer，learning_rate 是学习率，它的大小与网络的训练收敛速度有关系。
    '''
    optimizer = fluid.optimizer.Adam(learning_rate=0.001)  # 选择Adam优化器
    optimizer.minimize(avg_loss)

    save_dirname = "recognize_digits.inference.model"  # 训练后模型参数的存储位置, 后面正式使用是可以调用训练数据

    '''
    创建执行器
    '''
    startup_program = fluid.default_startup_program()
    exe = fluid.Executor(place)
    exe.run(startup_program)

    if runing_mode == "Training":  # 如果是训练模式
        '''
        设置训练过程的超参
        '''
        PASS_NUM = 5  # 训练5轮
        epochs = [epoch_id for epoch_id in range(PASS_NUM)]  # 根据训练轮次的序号生成一个epoch_id的列表

        '''
        设置 main_program 和 test_program
        '''
        main_program = fluid.default_main_program()
        test_program = fluid.default_main_program().clone(for_test=True)

        BATCH_SIZE = 64
        train_reader = paddle.batch(paddle.dataset.mnist.train(), batch_size=BATCH_SIZE)  # 自动从mnist数据库下载训练数据
        test_reader = paddle.batch(paddle.dataset.mnist.test(), batch_size=BATCH_SIZE)  # 自动从mnist数据库下载训练测试数据
        startup_program.random_seed = 90
        main_program.random_seed = 90

        lists = []
        step = 0
        for epoch_id in epochs:
            for step_id, data in enumerate(train_reader()):
                metrics = exe.run(main_program, feed=feeder.feed(data), fetch_list=[avg_loss, acc])
                if step % 100 == 0:  # 每训练100次 打印一次log
                    print("Pass %d, Batch %d, Cost %f" % (step, epoch_id, metrics[0]))
                    # event_handler_plot(train_prompt, step, metrics[0])
                step += 1

            # 测试每个epoch的分类效果
            avg_loss_val, acc_val = train_test(train_test_program=test_program, train_test_reader=test_reader,
                                               train_test_feed=feeder)
            print("Test with Epoch %d, avg_cost: %s, acc: %s" % (epoch_id, avg_loss_val, acc_val))
            # event_handler_plot(test_prompt, step, metrics[0])
            lists.append((epoch_id, avg_loss_val, acc_val))

            # 保存训练好的模型参数用于预测
            if save_dirname is not None:
                fluid.io.save_inference_model(save_dirname, ["img"], [prediction], exe, model_filename=None,
                                              params_filename=None)

        best = sorted(lists, key=lambda list: float(list[1]))[0]  # 选择效果最好的pass
        print('Best pass is %s, testing Avgcost is %s' % (best[0], best[1]))
        print('The classification accuracy is %.2f%%' % (float(best[2]) * 100))

    elif runing_mode == "Testing":  # 如果是识别模式

        cur_dir = os.getcwd()  # 获取当前目录
        tensor_img = load_image(cur_dir + '/image/infer_3.png')  # 打开要识别的图片

        inference_scope = fluid.core.Scope()
        with fluid.scope_guard(inference_scope):
            # 使用 fluid.io.load_inference_model 获取 inference program desc,
            # feed_target_names 用于指定需要传入网络的变量名
            # fetch_targets 指定希望从网络中fetch出的变量名
            [inference_program, feed_target_names, fetch_targets] = fluid.io.load_inference_model(save_dirname, exe,
                                                                                                  None, None)

            # 将feed构建成字典 {feed_target_name: feed_target_data}
            # 结果将包含一个与fetch_targets对应的数据列表
            results = exe.run(inference_program, feed={feed_target_names[0]: tensor_img}, fetch_list=fetch_targets)
            lab = numpy.argsort(results)

            # 打印 infer_3.png 这张图片的预测结果
            img = plt.imread('image/infer_3.png')
            plt.imshow(img)
            plt.show()
            print("Inference result of image/infer_3.png is: %d" % lab[0][0][-1])
