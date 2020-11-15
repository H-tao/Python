## 题目
有n个进程共享同一个list，每个进程pi(i~[1,n])每隔一段时间就向中添加数字i。当所有进程都添加完毕时，在主进程将list的内容输出。
```python
from multiprocessing import Process, Lock, Manager
import time
import random


def func(nums, p_id, lock: Lock):
    lock.acquire()                          # 打印控制台是共享资源，需要请求锁
    print(f"Process-{p_id} : ", id(nums))
    lock.release()                          # 释放锁
    for x in range(5):
        time.sleep(random.uniform(1, 3))    # 随机睡眠1-3秒
        lock.acquire()                      # nums也是共享资源，需要请求锁
        nums.append(p_id)
        print(f"Process-{p_id} : ", nums)
        lock.release()                      # 释放锁

if __name__ == '__main__':
    lock = Lock()
    nums = Manager().list([])               # 多个进程需要使用manager来传递共享变量
    p_list = []
    print("Main Process :", id(nums))
    for i in range(3):
        p = Process(target=func, args=(nums, i+1, lock, ))
        p.start()
        p_list.append(p)
    for p in p_list:
        p.join()
    print("Main Process :", nums)
```
输出:
```
Main Process : 2655621961480
Process-1 :  1857747821000
Process-2 :  2438204105032
Process-3 :  2555502964232
Process-3 :  [3]
Process-3 :  [3, 3]
Process-2 :  [3, 3, 2]
Process-1 :  [3, 3, 2, 1]
Process-3 :  [3, 3, 2, 1, 3]
Process-2 :  [3, 3, 2, 1, 3, 2]
Process-3 :  [3, 3, 2, 1, 3, 2, 3]
Process-1 :  [3, 3, 2, 1, 3, 2, 3, 1]
Process-2 :  [3, 3, 2, 1, 3, 2, 3, 1, 2]
Process-1 :  [3, 3, 2, 1, 3, 2, 3, 1, 2, 1]
Process-3 :  [3, 3, 2, 1, 3, 2, 3, 1, 2, 1, 3]
Process-2 :  [3, 3, 2, 1, 3, 2, 3, 1, 2, 1, 3, 2]
Process-1 :  [3, 3, 2, 1, 3, 2, 3, 1, 2, 1, 3, 2, 1]
Process-2 :  [3, 3, 2, 1, 3, 2, 3, 1, 2, 1, 3, 2, 1, 2]
Process-1 :  [3, 3, 2, 1, 3, 2, 3, 1, 2, 1, 3, 2, 1, 2, 1]
Main Process : [3, 3, 2, 1, 3, 2, 3, 1, 2, 1, 3, 2, 1, 2, 1]
```
