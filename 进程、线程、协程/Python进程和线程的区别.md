## 独立与非独立的内存空间

> 同一进程的线程共享本进程的地址空间和资源，而进程之间的地址空间和资源相互独立。 

我们看一个简单的例子，使用多个线程/进程向同一个`list`内添加值。

多线程的代码这样写：

```python
from threading import Thread, Lock

def func(nums, i, lock: Lock):
    lock.acquire()                          # 打印控制台是共享资源，需要请求锁
    print(f"Thread -{i} : ", id(nums))
    lock.release()                          # 释放锁
    for i in range(3):
        lock.acquire()                      # 我们认为nums也是共享资源，需要请求锁
        nums.append(i)
        print(f"Thread -{i} : ", nums)
        lock.release()                      # 释放锁

if __name__ == '__main__':
    lock = Lock()
    nums = []
    print("Main Thread :", id(nums))
    for i in range(3):
        p = Thread(target=func, args=(nums, i, lock, ))
        p.start()
        p.join()
    print("Main Thread :", nums)
```

输出的结果是我们想象中的结果，多个线程写入的是同一个`list`：

```
Main Thread : 3039846224456
Thread -0 :  3039846224456
Thread -0 :  [0]
Thread -1 :  [0, 1]
Thread -2 :  [0, 1, 2]
Thread -1 :  3039846224456
Thread -0 :  [0, 1, 2, 0]
Thread -1 :  [0, 1, 2, 0, 1]
Thread -2 :  [0, 1, 2, 0, 1, 2]
Thread -2 :  3039846224456
Thread -0 :  [0, 1, 2, 0, 1, 2, 0]
Thread -1 :  [0, 1, 2, 0, 1, 2, 0, 1]
Thread -2 :  [0, 1, 2, 0, 1, 2, 0, 1, 2]
Main Thread : [0, 1, 2, 0, 1, 2, 0, 1, 2]
```

那么我们换成多进程呢？代码稍微修改一下：

```python
from multiprocessing import Process, Lock

def func(nums, i, lock: Lock):
    lock.acquire()                          # 打印控制台是共享资源，需要请求锁
    print(f"Process -{i} : ", id(nums))
    lock.release()                          # 释放锁
    for i in range(3):
        lock.acquire()                      # 我们认为nums也是共享资源，需要请求锁
        nums.append(i)
        print(f"Process -{i} : ", nums)
        lock.release()                      # 释放锁

if __name__ == '__main__':
    lock = Lock()
    nums = []
    print("Main Process :", id(nums))
    for i in range(3):
        p = Process(target=func, args=(nums, i, lock, ))
        p.start()
        p.join()
    print("Main Process :", nums)
```

结果输出，和多线程是不同的，和我们想象中的效果不一样啊：

```
Main Process : 2074467994184
Process -0 :  2278560477128
Process -0 :  [0]
Process -1 :  [0, 1]
Process -2 :  [0, 1, 2]
Process -1 :  2077940821960
Process -0 :  [0]
Process -1 :  [0, 1]
Process -2 :  [0, 1, 2]
Process -2 :  2538612830152
Process -0 :  [0]
Process -1 :  [0, 1]
Process -2 :  [0, 1, 2]
Main Process : []
```

每个进程都具有独立的内存空间。我们使用创建子进程的时候，子进程Process替我们深度复制了传入的参数，生成了自己的进程空间。因此不同进程操作的`list` 并不是同一个`list`，而是各个子进程复制出来的`list`。
