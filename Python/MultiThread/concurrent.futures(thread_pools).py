"""
从Python3.2开始, Python官方提供了一个更高级别的多线程处理模块concurrent.futures
这个模块大约包括两部分: ThreadPoolExecutor, ProcessPoolExecutor分别对应线程池与进程池
详细信息可以查看官方文档 https://docs.python.org/zh-cn/3/library/concurrent.futures.html
"""

import concurrent.futures
import urllib.request

URLS = ['http://www.baidu.com/',
        'http://www.163.com/',
        'http://www.jd.com/',
        'http://www.taobao.com/',
        'http://www.sina.com/']


# Retrieve a single page and report the URL and contents
def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()


if __name__ == '__main__':

    # create a thread pool with x threads
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=5)

    # Start the load operations and mark each future with its URL
    # future_to_url = dict()
    future_list = list()
    # future_to_url = {pool.submit(load_url, url, 60): url for url in URLS}
    for url in URLS:
        # future_to_url[pool.submit(load_url, url, 60)] = url
        future_list.append(pool.submit(load_url, url, 60))

    # Future实例(线程句柄)有一些方法可以对正在进行的线程进行一些查询或者操作
    if future_list[0].done():
        print("如果线程已完成, 则返回线程运行的结果: ", future_list[0].result())
    else:
        print(f"线程正在运行吗: ", future_list[0].running())
        print("尝试取消")
        future_list[0].cancel()
        print("线程取消成功吗: ", future_list[0].cancelled())

    '''
    concurrent.futures.as_completed方法会返回一个已完成或者出现异常的线程的集合(即已停止运行的线程)
    返回的集体是Future实例(线程句柄)的迭代器, 如果需要做后续操作, 可以将它转换成列表之类的
    需要提供一个Future实例(线程句柄)的集合作为参数, 这里说的Future实例(线程句柄)的集合可以任何迭代器, 比如列表, 字典等
    '''
    # 返回的迭代器, 只能通过__next__()方法, 或者使用for each来遍历
    completed_futures = concurrent.futures.as_completed(future_list)

    # 在其实需求的话, 可以先转换成列表之类的可操作的类型, 当然要注意转换后原迭代器就空了
    # cf_list = list(completed_futures)

    for future in completed_futures:
        # url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            # print('%r generated an exception: %s' % (url, exc))
            print('generated an exception: %s' % exc)
        else:
            # print('%r page is %d bytes' % (url, len(data)))
            print('page is %d bytes' % (len(data)))

    # 关闭线程池, wait参数的作用是主进程是否等等待所有线程完结后才执行关闭,
    # cancel-futures参数是指定是否去尝试强制关闭还在运行中的线程来实现尽快shutdown
    # 实际上起到thread.join()的阻塞作用
    pool.shutdown(wait=True, cancel_futures=False)

