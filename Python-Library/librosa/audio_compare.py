import librosa
import librosa.display
import matplotlib.pyplot as plt
from dtw import dtw
from numpy.linalg import norm

if __name__ == '__main__':
    # example from https://github.com/pollen-robotics/dtw/blob/master/examples/MFCC%20%2B%20DTW.ipynb

    # Loading audio files
    y1, sr1 = librosa.load('song1_re1.m4a')
    y2, sr2 = librosa.load('song2_re1.m4a')

    # Try to remove silent of the beginning / ending of the audio files
    y1 = librosa.effects.trim(y1, top_db=10)[0]
    y2 = librosa.effects.trim(y2, top_db=10)[0]

    '''
    MFCC (梅尔频率倒谱系数)
    MFCC是音频信号特征中最重要的一个，基本上处理音频信号就会用到。
    信号的MFCC参数是一个小集合的特征（一般10-20个），它能够简洁的表示频谱的包络。
    '''
    plt.subplot(1, 2, 1)
    mfcc1 = librosa.feature.mfcc(y=y1, sr=sr1)  # Computing MFCC values
    librosa.display.specshow(mfcc1)

    plt.subplot(1, 2, 2)
    mfcc2 = librosa.feature.mfcc(y=y2, sr=sr2)
    librosa.display.specshow(mfcc2)

    # 可以通过dist里的ord参数来调节精度, ord越少精度越高, 但会因为微小的差异就被判断为不一样, 原文是ord=1
    # 如果调节到一个比较大的数, 会比较能容忍差异, 这里尝试调节为5, 容错率大了10倍, 调到10, 没有明显增加
    # 所以暂定为5
    dist, cost, acc_cost, path = dtw(mfcc1.T, mfcc2.T, dist=lambda x, y: norm(x - y, ord=5))
    print("The normalized distance between the two : ", dist)   # 0 for similar audios

    plt.imshow(cost.T, origin='lower', cmap=plt.get_cmap('gray'), interpolation='nearest')
    plt.plot(path[0], path[1], 'w')   # creating plot for DTW

    plt.show()  # To display the plots graphically
