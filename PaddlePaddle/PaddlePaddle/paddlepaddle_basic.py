from __future__ import print_function

import sys

import paddle as paddle
import paddle.fluid as fluid
import six
import numpy
import math

"""
以下代码对应的文章是 - 词向量
(https://www.paddlepaddle.org.cn/documentation/docs/zh/1.5/beginners_guide/basics/word2vec/index.html)
背景介绍
本章我们介绍词的向量表征，也称为word embedding。词向量是自然语言处理中常见的一个操作，是搜索引擎、广告系统、推荐系统等互联网服务背后常见的基础技术。
在这些互联网服务里，我们经常要比较两个词或者两段文本之间的相关性。为了做这样的比较，我们往往先要把词表示成计算机适合处理的方式。最自然的方式恐怕莫过于
向量空间模型(vector space model)。 在这种方式里，每个词被表示成一个实数向量（one-hot vector），其长度为字典大小，每个维度对应一个字典里
的每个词，除了这个词对应维度上的值是1，其他元素都是0。One-hot vector虽然自然，但是用处有限。比如，在互联网广告系统里，
如果用户输入的query是“母亲节”，而有一个广告的关键词是“康乃馨”。虽然按照常理，我们知道这两个词之间是有联系的——母亲节通常应该送给母亲一束康乃馨；
但是这两个词对应的one-hot vectors之间的距离度量，无论是欧氏距离还是余弦相似度(cosine similarity)，由于其向量正交，都认为这两个词毫无相关性。
 得出这种与我们相悖的结论的根本原因是：每个词本身的信息量都太小。所以，仅仅给定两个词，不足以让我们准确判别它们是否相关。要想精确计算相关性，
 我们还需要更多的信息——从大量数据里通过机器学习方法归纳出来的知识。

在机器学习领域里，各种“知识”被各种模型表示，词向量模型(word embedding model)就是其中的一类。通过词向量模型可将一个 one-hot vector映射到
一个维度更低的实数向量（embedding vector），如embedding(母亲节)=[0.3,4.2,−1.5,...],embedding(康乃馨)=[0.2,5.6,−2.3,...]。
在这个映射到的实数向量表示中，希望两个语义（或用法）上相似的词对应的词向量“更像”，这样如“母亲节”和“康乃馨”的对应词向量的余弦相似度就不再为零了。
词向量模型可以是概率模型、共生矩阵(co-occurrence matrix)模型或神经元网络模型。在用神经网络求词向量之前，传统做法是统计一个词语的共生矩阵X。
X是一个|V|×|V| 大小的矩阵，Xij表示在所有语料中，词汇表V(vocabulary)中第i个词和第j个词同时出现的词数，|V|为词汇表的大小。
对X做矩阵分解（如奇异值分解，Singular Value Decomposition [5]），得到的U即视为所有词的词向量：

但这样的传统做法有很多问题：
1) 由于很多词没有出现，导致矩阵极其稀疏，因此需要对词频做额外处理来达到好的矩阵分解效果；
2) 矩阵非常大，维度太高(通常达到106×106的数量级)；
3) 需要手动去掉停用词（如although, a,...），不然这些频繁出现的词也会影响矩阵分解的效果。
基于神经网络的模型不需要计算和存储一个在全语料上统计产生的大表，而是通过学习语义信息得到词向量，因此能很好地解决以上问题。在本章里，我们将展示基于
神经网络训练词向量的细节，以及如何用PaddlePaddle训练一个词向量模型。

模型概览
在这里我们介绍三个训练词向量的模型：N-gram模型，CBOW模型和Skip-gram模型，它们的中心思想都是通过上下文得到一个词出现的概率。对于N-gram模型，
我们会先介绍语言模型的概念，并在之后的训练模型中，带大家用PaddlePaddle实现它。而后两个模型，是近年来最有名的神经元词向量模型，
由 Tomas Mikolov 在Google 研发[3]，虽然它们很浅很简单，但训练效果很好。

数据介绍
本教程使用Penn Treebank （PTB）（经Tomas Mikolov预处理过的版本）数据集。PTB数据集较小，训练速度快，应用于Mikolov的公开语言模型训练工具[2]中。
其统计情况如下：

    训练数据	         验证数据	       测试数据
ptb.train.txt	ptb.valid.txt	ptb.test.txt
    42068句      	3370句       	3761句
    
数据预处理
本章训练的是5-gram模型，表示在PaddlePaddle训练时，每条数据的前4个词用来预测第5个词。PaddlePaddle提供了对应PTB数据集的python包
paddle.dataset.imikolov，自动做数据的下载与预处理，方便大家使用。

预处理会把数据集中的每一句话前后加上开始符号<s>以及结束符号<e>。然后依据窗口大小（本教程中为5），从头到尾每次向右滑动窗口并生成一条数据。

如"I have a dream that one day" 一句提供了5条数据：

<s> I have a dream
I have a dream that
have a dream that one
a dream that one day
dream that one day <e>
最后，每个输入会按其单词次在字典里的位置，转化成整数的索引序列，作为PaddlePaddle的输入。
"""

'''
更大的BATCH_SIZE将使得训练更快收敛，但也会消耗更多内存。由于词向量计算规模较大，如果环境允许，请开启使用GPU进行训练，能更快得到结果。 
不同于之前的PaddlePaddle v2版本，在新的Fluid版本里，我们不必再手动计算词向量。PaddlePaddle提供了一个内置的方法fluid.layers.embedding，
我们就可以直接用它来构造 N-gram 神经网络。
'''

EMBED_SIZE = 32      # embedding维度
HIDDEN_SIZE = 256    # 隐层大小
N = 5                # ngram大小，这里固定取5
BATCH_SIZE = 100     # batch大小
PASS_NUM = 100       # 训练轮数

use_cuda = False  # 如果用GPU训练，则设置为True
word_dict = paddle.dataset.imikolov.build_dict()
dict_size = len(word_dict)
params_dirname = "word2vec.inference.model"
place = fluid.CUDAPlace(0) if use_cuda else fluid.CPUPlace()
train_reader = paddle.batch(paddle.dataset.imikolov.train(word_dict, N), BATCH_SIZE)
test_reader = paddle.batch(paddle.dataset.imikolov.test(word_dict, N), BATCH_SIZE)
main_program = fluid.default_main_program()
star_program = fluid.default_startup_program()
test_program = main_program.clone(for_test=True)
exe = fluid.Executor(place)
feed_order = ['firstw', 'secondw', 'thirdw', 'fourthw', 'nextw']

'''
我们来定义我们的 N-gram 神经网络结构。这个结构在训练和预测中都会使用到。因为词向量比较稀疏，我们传入参数 is_sparse == True, 可以加速稀疏矩阵的更新。
'''
def inference_program(words, is_sparse):
    embed_first = fluid.layers.embedding(
        input=words[0],
        size=[dict_size, EMBED_SIZE],
        dtype='float32',
        is_sparse=is_sparse,
        param_attr='shared_w')
    embed_second = fluid.layers.embedding(
        input=words[1],
        size=[dict_size, EMBED_SIZE],
        dtype='float32',
        is_sparse=is_sparse,
        param_attr='shared_w')
    embed_third = fluid.layers.embedding(
        input=words[2],
        size=[dict_size, EMBED_SIZE],
        dtype='float32',
        is_sparse=is_sparse,
        param_attr='shared_w')
    embed_fourth = fluid.layers.embedding(
        input=words[3],
        size=[dict_size, EMBED_SIZE],
        dtype='float32',
        is_sparse=is_sparse,
        param_attr='shared_w')

    concat_embed = fluid.layers.concat(
        input=[embed_first, embed_second, embed_third, embed_fourth], axis=1)
    hidden1 = fluid.layers.fc(input=concat_embed,
                              size=HIDDEN_SIZE,
                              act='sigmoid')
    predict_word = fluid.layers.fc(input=hidden1, size=dict_size, act='softmax')
    return predict_word

'''
基于以上的神经网络结构，我们可以如下定义我们的训练方法
'''
def train_program(predict_word):
    # 'next_word'的定义必须要在inference_program的声明之后，
    # 否则train program输入数据的顺序就变成了[next_word, firstw, secondw,
    # thirdw, fourthw], 这是不正确的.
    next_word = fluid.layers.data(name='nextw', shape=[1], dtype='int64')
    cost = fluid.layers.cross_entropy(input=predict_word, label=next_word)
    avg_cost = fluid.layers.mean(cost)
    return avg_cost

def optimizer_func():
    return fluid.optimizer.AdagradOptimizer(
        learning_rate=3e-3,
        regularization=fluid.regularizer.L2DecayRegularizer(8e-4))

'''
现在我们可以开始训练啦。如今的版本较之以前就简单了许多。我们有现成的训练和测试集：paddle.dataset.imikolov.train()和
paddle.dataset.imikolov.test()。两者都会返回一个读取器。在PaddlePaddle中，读取器是一个Python的函数，每次调用，会读取下一条数据。
它是一个Python的generator

paddle.batch 会读入一个读取器，然后输出一个批次化了的读取器。我们还可以在训练过程中输出每个步骤，批次的训练情况。
'''

def train(if_use_cuda, params_dirname, is_sparse=True):
    # place = fluid.CUDAPlace(0) if if_use_cuda else fluid.CPUPlace()
    # train_reader = paddle.batch(paddle.dataset.imikolov.train(word_dict, N), BATCH_SIZE)
    # test_reader = paddle.batch(paddle.dataset.imikolov.test(word_dict, N), BATCH_SIZE)

    first_word = fluid.layers.data(name='firstw', shape=[1], dtype='int64')
    second_word = fluid.layers.data(name='secondw', shape=[1], dtype='int64')
    third_word = fluid.layers.data(name='thirdw', shape=[1], dtype='int64')
    forth_word = fluid.layers.data(name='fourthw', shape=[1], dtype='int64')
    next_word = fluid.layers.data(name='nextw', shape=[1], dtype='int64')

    word_list = [first_word, second_word, third_word, forth_word, next_word]
    # feed_order = ['firstw', 'secondw', 'thirdw', 'fourthw', 'nextw']

    main_program = fluid.default_main_program()
    # star_program = fluid.default_startup_program()

    predict_word = inference_program(word_list, is_sparse)
    avg_cost = train_program(predict_word)
    # test_program = main_program.clone(for_test=True)

    sgd_optimizer = optimizer_func()
    sgd_optimizer.minimize(avg_cost)

    # exe = fluid.Executor(place)
    return predict_word, avg_cost

def train_test(program, reader):
    count = 0
    predict_word, avg_cost = train(None, None)
    feed_var_list = [program.global_block().var(var_name) for var_name in feed_order]
    feeder_test = fluid.DataFeeder(feed_list=feed_var_list, place=place)
    test_exe = fluid.Executor(place)
    accumulated = len([avg_cost]) * [0]
    for test_data in reader():
        avg_cost_np = test_exe.run(
            program=program,
            feed=feeder_test.feed(test_data),
            fetch_list=[avg_cost])
        accumulated = [
            x[0] + x[1][0] for x in zip(accumulated, avg_cost_np)
        ]
        count += 1
    return [x / count for x in accumulated]


def train_loop():
    step = 0
    predict_word, avg_cost = train(None, None)
    feed_var_list_loop = [main_program.global_block().var(var_name) for var_name in feed_order]
    feeder = fluid.DataFeeder(feed_list=feed_var_list_loop, place=place)
    exe.run(star_program)
    for pass_id in range(PASS_NUM):
        for data in train_reader():
            avg_cost_np = exe.run(
                main_program, feed=feeder.feed(data), fetch_list=[avg_cost])

            if step % 10 == 0:
                outs = train_test(test_program, test_reader)

                print("Step %d: Average Cost %f" % (step, outs[0]))

                # 整个训练过程要花费几个小时，如果平均损失低于5.8，
                # 我们就认为模型已经达到很好的效果可以停止训练了。
                # 注意5.8是一个相对较高的值，为了获取更好的模型，可以将
                # 这里的阈值设为3.5，但训练时间也会更长。
                if outs[0] < 5.8:
                    if params_dirname is not None:
                        fluid.io.save_inference_model(params_dirname, [
                            'firstw', 'secondw', 'thirdw', 'fourthw'
                        ], [predict_word], exe)
                    return
            step += 1
            if math.isnan(float(avg_cost_np[0])):
                sys.exit("got NaN loss, training failed.")

    raise AssertionError("Cost is too large {0:2.2}".format(avg_cost_np[0]))

'''
我们可以用我们训练过的模型，在得知之前的 N-gram 后，预测下一个词
'''
def infer(use_cuda, params_dirname=None):
    place = fluid.CUDAPlace(0) if use_cuda else fluid.CPUPlace()

    exe = fluid.Executor(place)

    inference_scope = fluid.core.Scope()
    with fluid.scope_guard(inference_scope):
        # 使用fluid.io.load_inference_model获取inference program，
        # feed变量的名称feed_target_names和从scope中fetch的对象fetch_targets
        [inferencer, feed_target_names,
         fetch_targets] = fluid.io.load_inference_model(params_dirname, exe)

        # 设置输入，用四个LoDTensor来表示4个词语。这里每个词都是一个id，
        # 用来查询embedding表获取对应的词向量，因此其形状大小是[1]。
        # recursive_sequence_lengths设置的是基于长度的LoD，因此都应该设为[[1]]
        # 注意recursive_sequence_lengths是列表的列表
        data1 = numpy.asarray([[211]], dtype=numpy.int64)  # 'among'
        data2 = numpy.asarray([[6]], dtype=numpy.int64)  # 'a'
        data3 = numpy.asarray([[96]], dtype=numpy.int64)  # 'group'
        data4 = numpy.asarray([[4]], dtype=numpy.int64)  # 'of'
        lod = numpy.asarray([[1]], dtype=numpy.int64)

        first_word = fluid.create_lod_tensor(data1, lod, place)
        second_word = fluid.create_lod_tensor(data2, lod, place)
        third_word = fluid.create_lod_tensor(data3, lod, place)
        fourth_word = fluid.create_lod_tensor(data4, lod, place)

        assert feed_target_names[0] == 'firstw'
        assert feed_target_names[1] == 'secondw'
        assert feed_target_names[2] == 'thirdw'
        assert feed_target_names[3] == 'fourthw'

        # 构造feed词典 {feed_target_name: feed_target_data}
        # 预测结果包含在results之中
        results = exe.run(
            inferencer,
            feed={
                feed_target_names[0]: first_word,
                feed_target_names[1]: second_word,
                feed_target_names[2]: third_word,
                feed_target_names[3]: fourth_word
            },
            fetch_list=fetch_targets,
            return_numpy=False)

        print(numpy.array(results[0]))
        most_possible_word_index = numpy.argmax(results[0])
        print(most_possible_word_index)
        print([
                  key for key, value in six.iteritems(word_dict)
                  if value == most_possible_word_index
              ][0])


def main(use_cuda, is_sparse):
    if use_cuda and not fluid.core.is_compiled_with_cuda():
        return

    train(
        if_use_cuda=use_cuda,
        params_dirname=params_dirname,
        is_sparse=is_sparse)

    infer(use_cuda=use_cuda, params_dirname=params_dirname)


if __name__ == '__main__':

    running_mode = "Training"

    if running_mode == "Training":
        train_loop()
    elif running_mode == "Testing":
        main(use_cuda=use_cuda, is_sparse=True)






