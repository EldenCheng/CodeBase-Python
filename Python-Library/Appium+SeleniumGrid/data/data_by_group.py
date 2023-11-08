import itertools
from data.constant import data_group_number, data_number

"""
如果只使用多进程或者只使用多线程, 数据其实可以通过使用queue来在各个进程与线程之间进行异步处理
但由于Python的GIL锁, 导致单纯多线程的处理速度有限, 而多进程又受CPU核心数的限制, 所以这个Demo
使用了多进程然后在每个进程中又开多线程这样的处理方法, 使用这种处理方法的后果就是进程的queue不能直接
在进程的多线程中使用, 而又不想使用太过复杂的处理方法来在进程与线程间共享使用同一份数据
所以就取巧地在打开多进程之前, 先把数据分开成为不同的组, 再把不同组的数据分配到不同的进程, 然后再把
组里的数据通过线程queue来在线程间共享, 从而实现数据分配
注意: 现在这个简单分配方法, 并不能保证特定的数据组能分配到特定的线程中, 只保证每个线程能分配到不同的数据组
"""

data_group = list()
data_of_every_group = int(data_number / data_group_number)  # 先使用预定数据计算中每一组的data数量

with open("./data/chat_list.txt", "r") as text_file:
    for i in range(1, data_group_number + 1):
        data_list = list()
        # itertools.islice可以读取迭代器中指定范围的数据
        # 注意读取过的数据就会从迭代器中删除
        for line in itertools.islice(text_file, 0, data_of_every_group):  # 每次从文件中读取N行数据
            data_list.append(line)
        data_group.append(data_list)
text_file.close()

