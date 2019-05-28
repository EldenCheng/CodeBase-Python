import atexit #允许注册程序退出时调用的函数

# atexit只有一个方法register,用来注册程序退出时要运行的方法,这个有点像unittest里面的tearDown
# 注意的是只有正常完成的程序(应该指的是exit 0)才会触发,而且触发的顺序与注册的顺序是相反的

import atexit


def exit1():
    print('exit1')
    raise Exception('exit1')


def exit2():
    print('exit2')


atexit.register(exit1)
atexit.register(exit2)

# 也可以使用修饰符
@atexit.register
def exit3():
    print('exit3')


if __name__ == '__main__':
    pass

