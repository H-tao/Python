## 独立与非独立的内存空间

> 同一进程的线程共享本进程的地址空间和资源，而进程之间的地址空间和资源相互独立。 

我们看一个简单的例子，使用多个线程/进程向同一个`list`内添加值。

多线程的代码这样写：

```python
from threading import Thread, Lock
import time

def func(nums, i, lock: Lock):
    lock.acquire()                          # 打印控制台是共享资源，需要请求锁
    print(f"Thread -{i} : ", id(nums))
    lock.release()                          # 释放锁
    for x in range(3):
        time.sleep(1)
        lock.acquire()                      # nums也是共享资源，需要请求锁
        nums.append(i)
        print(f"Thread -{i} : ", nums)
        lock.release()                      # 释放锁

if __name__ == '__main__':
    lock = Lock()
    nums = []
    print("Main Thread :", id(nums))
    t_list = []
    for i in range(3):
        t = Thread(target=func, args=(nums, i, lock, ))
        t_list.append(t)
        t.start()
    for t in t_list:
        t.join()
    print("Main Thread :", nums)
```

输出的结果是我们想象中的结果，多个线程写入的是同一个`list`：

```
Main Thread : 2112122344008
Thread -0 :  2112122344008
Thread -1 :  2112122344008
Thread -2 :  2112122344008
Thread -0 :  [0]
Thread -1 :  [0, 1]
Thread -2 :  [0, 1, 2]
Thread -1 :  [0, 1, 2, 1]
Thread -0 :  [0, 1, 2, 1, 0]
Thread -2 :  [0, 1, 2, 1, 0, 2]
Thread -0 :  [0, 1, 2, 1, 0, 2, 0]
Thread -1 :  [0, 1, 2, 1, 0, 2, 0, 1]
Thread -2 :  [0, 1, 2, 1, 0, 2, 0, 1, 2]
Main Thread : [0, 1, 2, 1, 0, 2, 0, 1, 2]
```

那么我们换成多进程呢？代码稍微修改一下：

```python
from multiprocessing import Process, Lock
import time

def func(nums, i, lock: Lock):
    lock.acquire()                          # 打印控制台是共享资源，需要请求锁
    print(f"Process -{i} : ", id(nums))
    lock.release()                          # 释放锁
    for x in range(3):
        time.sleep(1)
        lock.acquire()                      # nums也是共享资源，需要请求锁
        nums.append(i)
        print(f"Process -{i} : ", nums)
        lock.release()                      # 释放锁

if __name__ == '__main__':
    lock = Lock()
    nums = []							# 一个普通的list变量
    print("Main Process :", id(nums))
    p_list = []
    for i in range(3):
        p = Process(target=func, args=(nums, i, lock, ))
        p_list.append(p)
        p.start()
    for p in p_list:
        p.join()
    print("Main Process :", nums)
```

结果输出，和多线程是不同的，和我们想象中的效果不一样啊：

```
Main Process : 2153732646280
Process -0 :  2598231611336
Process -1 :  2290033891400
Process -2 :  2314883635464
Process -0 :  [0]
Process -1 :  [1]
Process -2 :  [2]
Process -0 :  [0, 0]
Process -1 :  [1, 1]
Process -2 :  [2, 2]
Process -0 :  [0, 0, 0]
Process -1 :  [1, 1, 1]
Process -2 :  [2, 2, 2]
Main Process : []
```

每个进程都具有独立的内存空间。我们使用创建子进程的时候，子进程Process替我们深度复制了传入的参数，生成了自己的进程空间。因此不同进程操作的`list` 并不是同一个`list`，而是各个子进程复制出来的`list`。如何在多进程中共享数据呢？这我们就要使用Python的中的管理器了。

## 管理器——不同进程中共享数据

管理器提供了一种创建共享数据的方法，从而可以在不同进程中共享，甚至可以通过网络跨机器共享数据。管理器维护一个用于管理 *共享对象* 的服务。其他进程可以通过代理访问这些共享对象。 

```python
from multiprocessing import Process, Lock, Manager
import time

def func(nums, i, lock: Lock):
    lock.acquire()                          # 打印控制台是共享资源，需要请求锁
    print(f"Process -{i} : ", id(nums))
    lock.release()                          # 释放锁
    for x in range(3):
        time.sleep(1)
        lock.acquire()                      # nums也是共享资源，需要请求锁
        nums.append(i)
        print(f"Process -{i} : ", nums)
        lock.release()                      # 释放锁

if __name__ == '__main__':
    lock = Lock()
    nums = Manager().list([])               # 多个进程需要使用manager来传递共享变量
    print("Main Process :", id(nums))
    p_list = []
    for i in range(3):
        p = Process(target=func, args=(nums, i, lock, ))
        p_list.append(p)
        p.start()
    for p in p_list:
        p.join()
    print("Main Process :", nums)
```

输出结果，即便各个进程打印出来`list`的id不同，但是仍然是同一数据，这就是管理器的作用：

```
Main Process : 2511697914568
Process -2 :  2023818640072
Process -1 :  1574718126600
Process -0 :  2238624938312
Process -2 :  [2]
Process -1 :  [2, 1]
Process -0 :  [2, 1, 0]
Process -2 :  [2, 1, 0, 2]
Process -1 :  [2, 1, 0, 2, 1]
Process -0 :  [2, 1, 0, 2, 1, 0]
Process -2 :  [2, 1, 0, 2, 1, 0, 2]
Process -1 :  [2, 1, 0, 2, 1, 0, 2, 1]
Process -0 :  [2, 1, 0, 2, 1, 0, 2, 1, 0]
Main Process : [2, 1, 0, 2, 1, 0, 2, 1, 0]
```

