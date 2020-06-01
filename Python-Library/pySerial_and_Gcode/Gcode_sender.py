import time

import serial
from time import sleep


def recv(serial):
    while True:
        data = serial.read_all()
        if data == '':
            continue
        else:
            break
        sleep(0.02)
    return data


if __name__ == '__main__':
    serial = serial.Serial('COM3', 115200, timeout=0.5)  #/dev/ttyUSB0
    if serial.isOpen():
        print("open success")
    else:
        print("open failed")
    time.sleep(5)
    while True:
        data =recv(serial)
        if data != b'':
            print("receive : ", data)
            time.sleep(1)
        input_string = input("Please input command('q' for quit): ")
        if input_string.lower() != 'q':
            input_string = bytes(input_string + '\n', encoding='ascii')
            serial.write(input_string)
            time.sleep(2)
        else:
            break

    serial.close()
