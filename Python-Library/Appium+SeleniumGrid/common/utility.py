import concurrent.futures
import multiprocessing
import threading

from queue import Queue
from test_cases.case001 import test_steps


def queue_worker(q: Queue):
    while True:
        item = q.get()
        print(f'Finished {item}\n')
        q.task_done()


def simple_thread(device_group, data_queue: multiprocessing.Queue):

    # 建立一个线程的消息队列, 并使用一个独立线程来统一处理各个线程的消息
    # 主要是为了将各线程的运行情况, 响应时间等等写入一个统一的log文件中
    thread_message_queue = Queue()
    threading.Thread(target=queue_worker, args=(thread_message_queue,), daemon=True).start()

    # 多线程入口
    thread_number = len(device_group)
    thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=thread_number)
    for d in device_group:
        data_list = data_queue.get()  # 分配data group
        data_queue.task_done()
        thread_pool.submit(test_steps, data_list, d['sender_caps'], d['receiver_caps'], thread_message_queue)

    # wait for all tasks to complete
    thread_pool.shutdown(wait=True)
    thread_message_queue.join()

