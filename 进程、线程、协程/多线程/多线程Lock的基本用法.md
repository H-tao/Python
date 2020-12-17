## 多个线程向同一个list内添加数字，使用Lock对操作进行互斥
```python
from threading import Thread, Lock
import time

def func(nums, _id, lock: Lock):
    for i in range(3):
        time.sleep(1)
        lock.acquire()                      # 请求锁
        nums.append(_id)
        print(f"Thread-{_id} : ", nums)
        lock.release()                      # 释放锁

if __name__ == '__main__':
    lock = Lock()
    nums = []
    t_list = []
    print("Main Thread :", nums)
    for i in range(5):
        t = Thread(target=func, args=(nums, i, lock,))
        t_list.append(t)
        t.start()

    for t in t_list:
        t.join()
    print("Main Thread :", nums)
```
输出：
```
Main Thread : []
Thread-0 :  [0]
Thread-4 :  [0, 4]
Thread-2 :  [0, 4, 2]
Thread-3 :  [0, 4, 2, 3]
Thread-1 :  [0, 4, 2, 3, 1]
Thread-0 :  [0, 4, 2, 3, 1, 0]
Thread-1 :  [0, 4, 2, 3, 1, 0, 1]
Thread-4 :  [0, 4, 2, 3, 1, 0, 1, 4]
Thread-2 :  [0, 4, 2, 3, 1, 0, 1, 4, 2]
Thread-3 :  [0, 4, 2, 3, 1, 0, 1, 4, 2, 3]
Thread-0 :  [0, 4, 2, 3, 1, 0, 1, 4, 2, 3, 0]
Thread-3 :  [0, 4, 2, 3, 1, 0, 1, 4, 2, 3, 0, 3]
Thread-2 :  [0, 4, 2, 3, 1, 0, 1, 4, 2, 3, 0, 3, 2]
Thread-1 :  [0, 4, 2, 3, 1, 0, 1, 4, 2, 3, 0, 3, 2, 1]
Thread-4 :  [0, 4, 2, 3, 1, 0, 1, 4, 2, 3, 0, 3, 2, 1, 4]
Main Thread : [0, 4, 2, 3, 1, 0, 1, 4, 2, 3, 0, 3, 2, 1, 4]
```
