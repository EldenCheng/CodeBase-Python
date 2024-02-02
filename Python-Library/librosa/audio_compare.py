import librosa
import librosa.display
import matplotlib.pyplot as plt
from dtw import dtw
from numpy.linalg import norm

if __name__ == '__main__':
    # 代码来源 https://github.com/pollen-robotics/dtw/blob/master/examples/MFCC%20%2B%20DTW.ipynb
    # Loading audio files
    y1, sr1 = librosa.load('song1_re1.m4a')
    y2, sr2 = librosa.load('song2_po2_re1.m4a')

    # Try to remove silent of the beginning / ending of the audio files
    y1 = librosa.effects.trim(y1, top_db=10)[0]
    y2 = librosa.effects.trim(y2, top_db=10)[0]

    '''
    MFCC (梅尔频率倒谱系数)
    MFCC是音频信号特征中最重要的一个，基本上处理音频信号就会用到。
    信号的MFCC参数是一个小集合的特征（一般10-20个），它能够简洁的表示频谱的包络。
    '''
    # plt.subplot(1, 2, 1)
    mfcc1 = librosa.feature.mfcc(y=y1, sr=sr1)  # Computing MFCC values
    # librosa.display.specshow(mfcc1)

    # plt.subplot(1, 2, 2)
    mfcc2 = librosa.feature.mfcc(y=y2, sr=sr2)
    # librosa.display.specshow(mfcc2)

    '''
    参考文章: https://www.jianshu.com/p/4c905853711c
    DTW(Dynamic Time Warping)是一种衡量序列相似性的手段，值越小一般代表两个序列越相近
    DTW可以计算两个时间序列的相似度，尤其适用于不同长度、不同节奏的时间序列（比如不同的人读同一个词的音频序列）。
    DTW将自动warping扭曲 时间序列（即在时间轴上进行局部的缩放），使得两个序列的形态尽可能的一致，得到最大可能的相似度
    其中, 返回值dist代表两个序列的距离, 距离越小表示两个序列越相似, cost表示accumulated cost, 
    
    为了对齐这两个序列，我们需要构造一个n x m的矩阵网格，矩阵元素(i, j)表示qi和cj两个点的距离d(qi, cj)（也就是序列Q的每一个点和C的每一个点之间的相似度，
    距离越小则相似度越高。这里先不管顺序），一般采用欧式距离，d(qi, cj)= (qi-cj)2（也可以理解为失真度）。
    每一个矩阵元素(i, j)表示点qi和cj的对齐。DP算法可以归结为寻找一条通过此网格中若干格点的路径，路径通过的格点即为两个序列进行计算的对齐的点,
    而返回值path是一个集合, 包含有the shortest path里所有点, 可以把path进行可视化, 
    '''
    dist, cost, acc_cost, path = dtw(mfcc1.T, mfcc2.T, dist=lambda x, y: norm(x - y, ord=1))
    print("The normalized distance between the two : ", dist)   # 0 for similar audios

    '''
    就算完全相同的一段音频, 由于每次录音都会有一定差异, 所以需要设置一个临界值来判断两个音频是否相同
    而不是直接使用0(无差异)来判断
    经过一些音频的对比, 发现相同音频的差异一般在十万级(100000)以下, 不同音频的差异会比相同音频的差异大几倍, 所以暂定临界值为100000
    注意, 这个阈值要根据实际环境测试后确定, 不同环境可能不能使用同一个阈值 
    '''
    threshold = 100000
    if int(dist) > threshold:
        print("Different")
    else:
        print("Same")

    # plt.imshow(cost.T, origin='lower', cmap=plt.get_cmap('gray'), interpolation='nearest')
    plt.plot(path[0], path[1], 'b')   # 可视化DTW的最短路径
    plt.show()  # To display the plots graphically
