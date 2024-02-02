import concurrent.futures
import csv
import multiprocessing
import threading
import time
from pathlib import Path

from queue import Queue
from random import random, randint

from data.constant import result_csv_path
from test_cases.case001 import test_steps


def thread_queue_processor(q: Queue):
    """
    处理从线程中放入的数据与信息
    """
    while True:
        item = q.get()
        # print(f'{item}\n')
        try:
            save_to_csv(result_csv_path, item)  # 尝试写入结果csv
        except (IOError, PermissionError) as msg:
            time.sleep(randint(5, 10))  # 写入失败就回避一段时间
            try:
                save_to_csv(result_csv_path, item)
            except (IOError, PermissionError) as msg:
                time.sleep(randint(5, 10))  # 写入失败就回避一段时间
                try:
                    save_to_csv(result_csv_path, item)
                except (IOError, PermissionError) as msg:  # 三次写入都失败, 放弃
                    print("Aborted to save: ", item)
        q.task_done()


def thread_creator(device_group, data_queue: multiprocessing.Queue):

    # 建立一个线程的消息队列, 并使用一个独立线程来统一处理各个线程的消息
    # 主要是为了将各线程的运行情况, 响应时间等等写入一个统一的log文件中
    thread_message_queue = Queue()
    threading.Thread(target=thread_queue_processor, args=(thread_message_queue,), daemon=True).start()

    # 多线程入口
    thread_number = len(device_group)
    thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=thread_number)
    for d in device_group:
        data_list = data_queue.get()  # 分配data group
        thread_pool.submit(test_steps, data_list, d['sender_caps'], d['receiver_caps'], thread_message_queue)

    # wait for all tasks to complete
    thread_pool.shutdown(wait=True)
    thread_message_queue.join()


def save_to_csv(csv_path, row, create=False):
    if not create or (create and not Path(csv_path).is_file()):
        with open(csv_path, 'a+', encoding='utf-8', newline='') as f:
            writer_obj = csv.writer(f)
            writer_obj.writerow(row)
        f.close()





