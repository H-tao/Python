
```python
"""
有n个线程，向同一个信箱(信箱的大小为k)里传递消息，放入的消息为数字i(i=1...n)，有m个线程从信箱里取数字，取出来将数字*10并打印。
"""
import time
import random
from threading import Thread, Semaphore, Lock
list_len = 5
in_index, out_index = 0, 0
in_lock, out_lock, output_lock = Lock(), Lock(), Lock()
message_list = [0 for x in range(list_len)]
full_semaphore, empty_semaphore = Semaphore(0), Semaphore(list_len)

def producer(name, num: int):
    global in_index, in_lock, output_lock, list_len, message_list, full_semaphore, empty_semaphore
    print(name, id(message_list))
    while True:
        time.sleep(random.randint(1, 5))
        empty_semaphore.acquire()
        in_lock.acquire()
        message_list[in_index] = num
        in_index = (in_index + 1) % list_len
        in_lock.release()
        full_semaphore.release()
        output_lock.acquire()
        print(f'{name}已经加入一个: {num}')
        output_lock.release()

def consumer(name):
    global out_index, out_lock, output_lock, list_len, message_list, full_semaphore, empty_semaphore
    print(name, id(message_list))
    while True:
        time.sleep(random.randint(1, 5))
        full_semaphore.acquire()
        out_lock.acquire()
        num = message_list[out_index] * 10
        out_index = (out_index + 1) % list_len
        out_lock.release()
        empty_semaphore.release()
        output_lock.acquire()
        print(f'{name}已经取得一个: {num}')
        output_lock.release()

if __name__ == '__main__':
    p1, p2, p3 = Thread(target=producer, args=('Producer-1 ', 1, )), Thread(target=producer, args=('Producer-2 ', 2, )), \
                 Thread(target=producer, args=('Producer-3 ', 3,))
    c1, c2 = Thread(target=consumer, args=('Consumer-1 ', )), Thread(target=consumer, args=('Consumer-2 ', ))
    p1.start()
    p2.start()
    p3.start()
    c1.start()
    c2.start()
```
