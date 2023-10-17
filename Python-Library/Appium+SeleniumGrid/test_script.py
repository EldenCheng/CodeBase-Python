import concurrent.futures

from code.mobiles import *
from test_cases.case001 import test_steps


if __name__ == '__main__':

    # selenium hub的地址， 如果hub在本机， 可以指定http://localhost:4444
    hub_url = "http://192.168.16.50:4444"

    '''
    当使用selenium hub与selenium node组织多台设备测试时
    因为真正传送到appium server的启动desired_capabilities已经在node中定义
    脚本里的desired_capabilities只是方便hub找到对应的node而已
    所以在脚本里指定的desired_capabilities可以只使用一部分
    '''
    '''
    如果脚本中指定的desired_capabilities比较模糊, hub会找到多个对应的node的话，
    至少在python中的表现就是每完整运行一次脚本（从开始运行到完整退出）, hub会按顺序每次转发
    命令到其中一个node, 而不是将命令转发到所有满足条件的node, 就像走马灯一样
    比如指定像下面的desired_capabilities, 每跑一次脚本, 就会连接下一个Android设备
    '''
    capabilities1 = dict(
        platformName='Android',
    )
    '''
    如果脚本中指定的desired_capabilities是唯一的, 那么hub会找到这个唯一的node
    '''
    capabilities2 = dict(
        deviceName='Galaxy S9+',
    )

    '''
    指定desired_capabilities后, 就可以连接设备进行测试了
    一次只跑一台设备的话可以直接运行
    '''
    test_steps(hub_url, options_s9plus, "Galaxy S9+")

    '''
    但如果需要同时在多台设备上跑, 就需要使用多进程或者多线程
    但一般电脑核心有限, 多进程的话能开的进程有限, 如果线程数超出核心数, 
    有可能需要等部分进程跑完脚本, 剩下的进程才会开始跑
    而python13之前的多线程由于GIL的缘故也不是真实的多线程(好像说JPython没有GIL), 但线程的数量基本不受核心数量限制
    不过线程数过多的话, 每个线程运行速度就会很慢
    这个需要按实际情况决定是使用多进程还是多线程
    下面的示例使用多线程操作
    '''

    # Multi thread
    # create a thread pool with x threads
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=10)

    # submit tasks to the pool
    pool.submit(test_steps, hub_url, options_s9plus, "s9plus")
    pool.submit(test_steps, hub_url, options_s10, "s10")
    pool.submit(test_steps, hub_url, options_s205g, "s205g")
    pool.submit(test_steps, hub_url, options_s22, "s22")
    pool.submit(test_steps, hub_url, options_note10, "note10")
    pool.submit(test_steps, hub_url, options_note20, "note20")
    pool.submit(test_steps, hub_url, options_s20fe, "s20fe")
    pool.submit(test_steps, hub_url, options_tabs2, "tabs2")
    pool.submit(test_steps, hub_url, options_tabs7plus, "tabs7plus")
    pool.submit(test_steps, hub_url, options_note9, "note9")

    # wait for all tasks to complete
    pool.shutdown(wait=True)


