import rpyc
import time

if __name__ == '__main__':
    conn = rpyc.connect('192.168.9.192', 9999)
    result = conn.root.relay_control("01", "ON")  # 开启useb_relay 01
    print(result)
    time.sleep(10)
    result = conn.root.relay_control("01", "OFF")  # 关闭useb_relay 01
    print(result)
    conn.close()
