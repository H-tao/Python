```python
"""
有n个进程，向同一个信箱(信箱的大小为k)里传递消息，放入的消息为数字i(i=1...n)，有m个进程从信箱里取数字，取出来将数字*10并打印。
"""
import time
import random
from multiprocessing import Process, Semaphore, Lock, Manager
from itertools import chain

PRODUCER_NUM = 4
CONSUMER_NUM = 3

def producer(name, num, in_lock, print_lock, arr, full, empty, _global):
    for x in range(5):
        time.sleep(random.randint(1, 5))
        empty.acquire()
        in_lock.acquire()
        arr[_global.in_index] = num
        _global.in_index = (_global.in_index + 1) % _global.arr_len
        in_lock.release()
        full.release()
        print_lock.acquire()
        print(f'{name}已经加入一个: {num} {_global.in_index}')
        print_lock.release()

def consumer(name, out_lock, print_lock, arr, full, empty, _global):
    for x in range(5):
        time.sleep(random.randint(1, 5))
        full.acquire()
        out_lock.acquire()
        num = arr[_global.out_index] * 10
        _global.out_index = (_global.out_index + 1) % _global.arr_len
        out_lock.release()
        empty.release()
        print_lock.acquire()
        print(f'{name}已经取得一个: {num} {_global.out_index}')
        print_lock.release()


if __name__ == '__main__':
    # with Manager() as manager:
    manager = Manager()
    _global = manager.Namespace()
    _global.in_index = 0        # 写入的索引
    _global.out_index = 0       # 读取的索引
    _global.arr_len = 5         # 队列长
    in_lock = Lock()            # 写入锁
    out_lock = Lock()           # 读取锁
    print_lock = Lock()         # 打印控制台锁
    full = Semaphore(0)                 # 空信号量
    empty = Semaphore(_global.arr_len)  # 满信号量
    arr = manager.list([0 for x in range(_global.arr_len)])     # 普通的list不能被多个进程共享，manager.list()可以

    p_list = [Process(target=producer, args=(f'Producer-{i} ', i, in_lock, print_lock, arr, full, empty, _global)) for i in range(1, PRODUCER_NUM)]
    c_list = [Process(target=consumer, args=(f'Consumer-{i} ', out_lock, print_lock, arr, full, empty, _global)) for i in range(1, CONSUMER_NUM)]
    for c in chain(p_list, c_list):
        c.start()
    for c in chain(p_list, c_list):
        c.join()
    print("End")
```
输出结果:
```
Producer-1 已经加入一个: 1 1
Producer-3 已经加入一个: 3 2
Producer-1 已经加入一个: 1 3
Consumer-1 已经取得一个: 10 1
Producer-2 已经加入一个: 2 4
Consumer-2 已经取得一个: 30 2
Consumer-1 已经取得一个: 10 3
Producer-1 已经加入一个: 1 0
Producer-2 已经加入一个: 2 1
Producer-3 已经加入一个: 3 2
Consumer-2 已经取得一个: 20 4
Producer-1 已经加入一个: 1 3
Consumer-1 已经取得一个: 10 0
Producer-2 已经加入一个: 2 4
Producer-1 已经加入一个: 1 0
Consumer-2 已经取得一个: 20 1
Consumer-2 已经取得一个: 30 2
Producer-3 已经加入一个: 3 1
Consumer-1 已经取得一个: 10 3
Producer-2 已经加入一个: 2 2
Producer-3 已经加入一个: 3 3
Consumer-2 已经取得一个: 20 4
Consumer-1 已经取得一个: 10 0
Producer-2 已经加入一个: 2 4
Producer-3 已经加入一个: 3 0
End
```
