import multiprocessing
import time
from multiprocessing import Process

from data.constant import result_csv_path
from data.data_by_group import data_group
from data.mobile_by_group import devices_group1, devices_group2, devices_group3
from common.utility import thread_creator, save_to_csv

if __name__ == '__main__':

    """
    本示例是展示使用多进程 + 多线程同时控制多台设备进行信息收发操作, 同时统计收发的成功率, 响应时间等等信息
    本示例使用的App是Simple Bluetooth Chat, 运行本示例前需要先把两台手机上的Simple Bluetooth Chat
    连接好, 保证可以相互发送消息
    """

    # 把所有数据组逐一放到进程队列中, 这样就可以多个进程共享同一个数据来源
    # 再在进程中把数据组从进程队列中提取出, 分配给不同的线程, 就可以实现每个线程获得独立的数据组
    data_queue = multiprocessing.Queue()
    for dg in data_group:
        data_queue.put(dg)

    """
    各个线程的运行结果应该汇聚在一起, 尝试让各个线程共享使用一个queue去保存结果
    但Python中好像进程Queue与线程Queue不能混用, 即进程Queue只能用于多进程, 不
    能用于进程里面的多线程, 而线程Queue只能用于同一个进程里的各个线程, 不能用于
    其它进程
    所以这里使用一个csv文件来汇总各个线程的运行结果, 现在只是简单做一次碰撞回避
    如果有很多线程需要同时写入到这个文件时, 可能要使用线程锁来实现竞争使用
    """
    csv_tile = ["Time", "Action", "Result", "Response Time(s)"]
    save_to_csv(result_csv_path, csv_tile, True)

    """
    由于Python有GIL, 所以只使用多线程, 性能方面不够, 但多进程又受CPU核心数限制, 数量不够
    所以这里采用多进程, 然后在每一个进程中开多线程的方法, 希望可以控制更多设备的同时
    能尽量利用更多的CPU核心来提高性能
    这里不使用线程池Pool的原因是这里传到多线程入口方法中的参数都是数组, 而Pool.map方法会
    根据参数数组元素的数量来开进程, 在这里比较不方便, 所以下面使用了手工逐一开启进程的方式来
    开启多进程
    """
    p1 = Process(target=thread_creator, args=(devices_group2, data_queue))
    p2 = Process(target=thread_creator, args=(devices_group3, data_queue))
    p1.start()
    # time.sleep(600)  TODO As not all the VU will be started at the same time, maybe we can start the process not at the same time
    p2.start()
    p1.join()
    p2.join()




