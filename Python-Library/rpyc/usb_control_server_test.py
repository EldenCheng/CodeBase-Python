from rpyc import Service
from rpyc.utils.server import ThreadedServer
import os


class USBRelayService(Service):

    def exposed_relay_control(self, replay: str = "01", on_off: str = "ON") -> int:
        os.chdir("D:/Elden/USBRelay/USBRelay外部使用开发库/TestApp")  # enter the path of CommandApp_USBRelay.exe
        result = -1  # 如果是-1的话基本代表参数使用不当, 没有调用下面的逻辑
        if on_off.lower() == "on":
            # open relay 0x
            # return value : 0 -- success; 1 -- error; 2 -- index is outnumber the number of the usb relay device
            result = os.system("CommandApp_USBRelay  BITFT open {0}".format(replay))
        if on_off.lower() == "off":
            result = os.system("CommandApp_USBRelay  BITFT close {0}".format(replay))  # close relay 01
        return result


if __name__ == '__main__':
    # 先在terminal运行这个服务, 然后使用rpc client来访问这个服务
    s = ThreadedServer(USBRelayService, port=9999, auto_register=False)
    s.start()
