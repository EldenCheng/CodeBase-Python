"""
开启多线程可以使用两个方法, 第一是建立一个自定义的线程类, 通过继承Thread基类, 再重构基类方法来实现多线程
第二就是直接使用threading.Thread(target=func_name, args=(arg1, arg2, ), daemon=True).start()来创建一个线程
实际上, 两种方法实现的方法都是一样的(建立一个Thread类(或者Thread的继承类), 再start), 只是写在脚本上的形式有分别

详细信息可以参考官方文档: https://docs.python.org/zh-cn/3/library/threading.html
"""

import threading
import time


# 方法一, 建立一个继承Thread的自定义类, 需要重构run方法
# 好处是在建立实例时可以自定义一些实例参数, 比如thread的名字(虽然Thread会有默认的名字, 但有时就需要自定义)
class MyThread (threading.Thread):
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name)
        print_time(self.name, self.counter, 5)
        print("Exiting " + self.name)


# 需要多线程执行的方法
def print_time(thread_name, delay: int = 3, counter: int = 5):
    while counter:
        time.sleep(delay)
        print("%s: %s" % (thread_name, time.ctime(time.time())))
        counter -= 1


if __name__ == "__main__":
    # Create new threads
    thread1 = MyThread(1, "Thread-1", 1)
    thread2 = MyThread(2, "Thread-2", 2)

    # Start new Threads
    thread1.start()
    thread2.start()

    # 方法二, 直接使用threading.Thread来创建多线程
    # 要注意这里的thread3没有自定义构造函数的参数, 所以args需要提供的是print_time的参数
    # 另外, 如果多线程执行的方法只有一个参数的话, 要写成args=(arg, ), 这样python才会认为传进去的是一个元组
    thread3 = threading.Thread(target=print_time, args=("Thread-3", ), daemon=True)
    thread3.start()

    # threading中也有一些方法可以了解当前的多线程状态
    print("当前活跃的线程数为: ", threading.active_count())  # 活跃线程数要加上脚本所在的主线程, 所以一般得出来的结果是多1个
    print("当前仍然运行中的线程列表: ", threading.enumerate())  # 注意仍然会包含主线程在内的

    # 当然可以使用创建线程后返回的Thread类的方法来实现一些操作
    print("线程3的名字是: ", thread3.name)
    print("线程3仍然在活跃吗: ", thread3.is_alive())
    print("线程3是守护线程吗: ", thread3.isDaemon())  # 当没有存活的非守护线程时，整个Python程序才会退出

    thread1.join()
    print("线程1的名字是: ", thread1.name)
    print("线程1仍然在活跃吗: ", thread1.is_alive())
    thread2.join()
    thread3.join()

    print("All threads are done, exiting Main Thread")

