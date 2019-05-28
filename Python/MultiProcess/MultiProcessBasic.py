from multiprocessing import Process
import os
from Python.MultiProcess.Data import Test

# 子进程要执行的代码
def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))
    print(Test.get_dict())
    Test.set_dict("Hardy" + name)
    print(Test.get_dict())


if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p1 = Process(target=run_proc, args=('test1',))
    p2 = Process(target=run_proc, args=('test2',))
    print('Child process will start.')
    p1.start()
    p1.join()
    p2.start()
    p2.join()
    print('Child process end.')
    print(Test.get_dict())