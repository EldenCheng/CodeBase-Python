import time
import threading

def device1():
    for i in range(10):
        print('device1')
        #time.sleep(1)

def device2():
    for i in range(10):
        print('device2')
        #time.sleep(0.5)

threads = []

t1 = threading.Thread(target=device1)
threads.append(t1)

t2 = threading.Thread(target=device2)
threads.append(t2)

if __name__ == '__main__':
    for t in threads:
        print('start', t)
        t.start()

    for t in threads:
        print('join', t)
        t.join()

    print('all end')