from rpyc import Service
from rpyc.utils.server import ThreadedServer


class TestService(Service):

    # 对于服务端来说， 只有以"exposed_"打头的方法才能被客户端调用，所以要提供给客户端的方法都得加"exposed_"
    def exposed_sum(self, num1: int, num2: int) -> int:
        '''
        实现num1、num2相加
        :param num1:
        :param num2:
        :return:
        '''
        return num1 + num2


if __name__ == '__main__':
    s = ThreadedServer(TestService, port=9999, auto_register=False)
    s.start()