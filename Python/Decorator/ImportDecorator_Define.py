class MyLocker:
    counter = 0

    def __init__(self):
        print("mylocker.__init__() called.")

    @staticmethod
    def acquire():
        print("MyLocker.acquire() 调用")
        MyLocker.counter = MyLocker.counter + 1

    @staticmethod
    def unlock():
        print("MyLocker.unlock() 调用")
        MyLocker.counter = MyLocker.counter + 1

    @staticmethod
    def get_counter():
        return MyLocker.counter


class LockeRex(MyLocker):
    @staticmethod
    def acquire():
        print("lockerex.acquire() called.")

    @staticmethod
    def unlock():
        print("  lockerex.unlock() called.")


def LockHelper(cls, para):
    """
    cls 必须实现acquire和release静态方法
    :param cls:
    :return:
    """

    def _deco(func):
        def wrapper(*args, **kwargs):
            print("传入的参数是 ", para)
            print(",传入的 %s 方法前, wrapper执行中" % func.__name__)
            cls.acquire()
            try:
                return func(*args, **kwargs)
            finally:
                cls.unlock()
        return wrapper
    return _deco


