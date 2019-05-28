# -*- coding:gbk -*-
'''
示例9: 装饰器带类参数，并分拆公共类到其他py文件中
同时演示了对一个函数应用多个装饰器
'''

from Python.Decorator.ImportDecorator_Define import *


class Example:
    @LockHelper(MyLocker, "传参测试")
    def myfunc(self):
        print("被装饰的方法运行中")

    @LockHelper(MyLocker, "传参测试")
    @LockHelper(LockeRex, "传参测试")
    def myfunc2(self, a, b):
        print(" myfunc2() called.")
        return a + b


if __name__ == "__main__":
    a = Example()
    a.myfunc()
    print(a.myfunc())
    print(MyLocker.get_counter())
    # print(a.myfunc2(1, 2))
    # print(a.myfunc2(3, 4))
