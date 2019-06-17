import time


class StrTest(object):

    def __init__(self):
        self.number = 10
        self.words = "Some words"
        self.current_time = time.strftime("%Y-%m-%d_%H%M%S", time.localtime())

    # 定义__str__方法可以与Java的ToString方法一样, 可以指定当前类的实例是怎样转换成string的
    # __str__方法对应的是str(),一般Python自动转换时默认的都是使用这个方法
    def __str__(self):
        return self.current_time

    # __repr__方法对应的是repr()
    def __repr__(self):
        return self.current_time


if __name__ == "__main__":
    t = StrTest()
    print(t)
    print(str(t))
    print(repr(t))
    print(t.words)
