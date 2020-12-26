# 使用futures模块处理并发

concurrent.futures模块的主要特色是ThreadPoolExecutor和ProcessPoolExecutor类，这两个类实现的接口能分别在不同的线程或进程中执行可调用的对象。这两个类在内部维护着一个工作线程或进程池，以及要执行的任务队列。ThreadPoolExecutor和ProcessPoolExecutor的API接口一样，本文重点讲解ThreadPoolExecutor的用法。

## 一、用法示例

### 1. 使用 map() 处理多个任务

使用两行代码，就能帮我们调用多线程完成任务：

```python
with futures.ThreadPoolExecutor(max_workers=5) as executor: 	# max_workers 最大线程数
    res = executor.map(fn, params)		# fn 是被调用函数，params 是 fn 的参数
```

例子如下：

```python
from concurrent import futures

def download_source(url):
    print(url)
    return url * 100

urls = range(1, 20)

with futures.ThreadPoolExecutor(max_workers=5) as executor:
    res = executor.map(download_source, urls)

print(list(res))
```

```css
1
2
3
4
...	# 省略了输出
18
19
[100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900]
```

**注意事项：**map() 返回结果的顺序和调用开始的顺序一直，如果第一个调用生成结果用时10秒，而其他调用只用1秒，代码会阻塞10秒以获取第一个结果。在此之后，获取后续结果不会阻塞，因为后续调用已经结束。更可取的方式是，不管提交顺序如何，只要有结果就获取。而使用 Executor.submit 方法和 futures.as_completed 函数可以帮我们完成这种方式。

### 2. 使用 submit() 提交单个任务

map() 可以帮我们快速完成一批任务，但是我们有时候需要的是单个处理，可以使用 submit()：

```python
import time
from concurrent import futures

def sleep_and_print(number):
    time.sleep(1)
    print('I am number', number)
    return number * 100

numbers = range(1, 100)

with futures.ThreadPoolExecutor(max_workers=5) as executor:
    for num in numbers:
        future = executor.submit(sleep_and_print, num)	# 当submit时，executor会创建线程，并将事件加入_work_queue(threading.Queue)，多个线程从_work_queue获取Work并执行。
```

此处 submit() 返回的 future 并不是结果，而是指待完成的操作。future 封装待完成的操作，可以放入队列，完成的状态可以查询，得到结果后可以获取结果（或者异常）。

###3. 使用 as_completed() 逐个获取已完成的任务

>  as_completed() 返回一个包含 *fs* 所指定的 [`Future`](https://docs.python.org/zh-cn/3/library/concurrent.futures.html#concurrent.futures.Future) 实例（可能由不同的 [`Executor`](https://docs.python.org/zh-cn/3/library/concurrent.futures.html#concurrent.futures.Executor) 实例创建）的迭代器，这些实例会在完成时生成 future 对象（包括正常结束或被取消的 future 对象）。 任何由 *fs* 所指定的重复 future 对象将只被返回一次。 任何在 [`as_completed()`](https://docs.python.org/zh-cn/3/library/concurrent.futures.html#concurrent.futures.as_completed) 被调用之前完成的 future 对象将优先被生成。 如果 [`__next__()`](https://docs.python.org/zh-cn/3/library/stdtypes.html#iterator.__next__) 被调用并且在对 [`as_completed()`](https://docs.python.org/zh-cn/3/library/concurrent.futures.html#concurrent.futures.as_completed) 的原始调用 *timeout* 秒之后结果仍不可用，则返回的迭代器将引发 [`concurrent.futures.TimeoutError`](https://docs.python.org/zh-cn/3/library/concurrent.futures.html#concurrent.futures.TimeoutError)。 *timeout* 可以为整数或浮点数。 如果 *timeout* 未指定或为 `None`，则不限制等待时间。 

#### 3.1 获取运行结果

我们尝试获取结果：

```python
with futures.ThreadPoolExecutor(max_workers=3) as executor:
    to_do = []		# 待完成的队列，用于保存所有 future
    for _i in numbers:
        future = executor.submit(sleep_and_print, _i)	# 加入执行
        to_do.append(future)

    results = []	
    for future in futures.as_completed(to_do):	# 等待完成
        res = future.result()	# 接收结果
        results.append(res)
        print("Already Finished", res)
        
    print(results)
```

#### 3.2 获取异常

```python
import time
from concurrent import futures

class DemoException(Exception):		# 自定义异常
    pass

def sleep_and_print(number):
    time.sleep(1)
    print('I am number', number)
    raise DemoException				# 产出异常

numbers = range(1, 10)

with futures.ThreadPoolExecutor(max_workers=3) as executor:
    to_do = []
    for _i in numbers:
        future = executor.submit(sleep_and_print, _i)  
        to_do.append(future)

    exceptions = []
    for future in futures.as_completed(to_do):
        res = future.exception()	# future.exception() 获取异常
        exceptions.append(res)

    print(exceptions)
```

```css
I am numberI am number 1 3

I am number 2
I am number 4
I am number 5
I am number 6
I am numberI am number I am number 7
8 9

[DemoException(), DemoException(), DemoException(), DemoException(), DemoException(), DemoException(), DemoException(), DemoException(), DemoException()]
```

### 4. 使用 Lock 解决(打印混乱)争用问题

上面的代码是有问题的，我们访问同一个打印控制台，打印会造成混乱。`ThreadPoolExecutor` 内部是使用的原生的`threading`去创建线程，所以我们使用 threading.Lock 就可以解决争用问题：

```python
from concurrent import futures
from threading import Lock
import time

g_Lock = Lock()     # 多线程互斥访问 print 打印控制台，需要加锁

def sleep_and_print(number):
    time.sleep(1)
    with g_Lock:	# 尝试获取锁
        print('I am number', number)
    return number * 100

numbers = range(1, 1000)

with futures.ThreadPoolExecutor(max_workers=3) as executor:
    results = executor.map(sleep_and_print, numbers)
```

### 5. 使用 add_done_callback() 回调函数

```python
import time
from concurrent import futures
from threading import Lock

g_Lock = Lock()

def sleep_and_print(number):
    time.sleep(1)
    with g_Lock:
        print('I am number', number)
    return number * 100

def _done(f):		# f 是 future 对象，是唯一参数
    with g_Lock:
        print(f, 'Done')

numbers = range(1, 1000)

with futures.ThreadPoolExecutor(max_workers=3) as executor:
    to_do = []
    for _i in numbers:
        future = executor.submit(sleep_and_print, _i)  # 当submit时，executor会创建线程，并将事件加入_work_queue(threading.Queue)，多个线程从_work_queue获取Work并执行。
        to_do.append(future)

    for future in to_do:
        future.add_done_callback(_done)		# 回调函数
```

```css
I am number 1
<Future at 0x25154d1ae08 state=finished returned int> Done
I am number 2
<Future at 0x25154d6a508 state=finished returned int> Done
I am number 3
<Future at 0x25154d75108 state=finished returned int> Done
I am number 4
<Future at 0x25154d753c8 state=finished returned int> Done
I am number 5
I am number 6
<Future at 0x25154d75748 state=finished returned int> Done
<Future at 0x25154d75588 state=finished returned int> Done
...
```

### 6. 使用 wait() 获取所有 future 的状态

wait() 会返回一个命名2元组，包含两个 set()，一个 set 包含已完成的 future (finished or cancelled) ，另一个包含未完成的 future：

```python
import time
from concurrent import futures
from threading import Lock

g_Lock = Lock()

def sleep_and_print(number):
    time.sleep(1)
    with g_Lock:
        print('I am number', number)
    return number * 100

numbers = range(1, 10)

with futures.ThreadPoolExecutor(max_workers=3) as executor:
    to_do = []
    for _i in numbers:
        future = executor.submit(sleep_and_print, _i)  # 当submit时，executor会创建线程，并将事件加入_work_queue(threading.Queue)，多个线程从_work_queue获取Work并执行。
        to_do.append(future)

    time.sleep(2)
    with g_Lock:
        print(futures.wait(to_do, timeout=1))
```

```css
I am number 2
I am number 1
I am number 3
I am number 5
DoneAndNotDoneFutures(done={<Future at 0x2724b629748 state=finished returned int>, <Future at 0x2724b635488 state=finished returned int>, <Future at 0x2724b5b1ac8 state=finished returned int>, <Future at 0x2724b62cfc8 state=finished returned int>}, not_done={<Future at 0x2724b635648 state=running>, <Future at 0x2724b6352c8 state=running>, <Future at 0x2724b635b08 state=pending>, <Future at 0x2724b635948 state=pending>, <Future at 0x2724b6357c8 state=running>})
I am number 6
I am number 4
I am number 7
I am number 9
I am number 8
```

## 二、核心内容

### 1. Executor 对象详解

concurrent.futures 模块中的 Executor 提供了异步执行调用方法，是 ThreadPoolExecutor 和 ProcessPoolExecutor 的父类。Executor 提供了如下方法： 

- `submit(fn, *args, **kwargs)`：调度可调用对象 *fn*，以 `fn(*args **kwargs)` 方式执行并返回 [`Future`](https://docs.python.org/zh-cn/3/library/concurrent.futures.html#concurrent.futures.Future) 对象代表可调用对象的执行。 
- `map(func, *iterables, timeout=None, chunksize=1)` ：类似于全局函数 map(func, *iterables)， 将 *iterables* 和 func 组成任务立即丢入任务池，生成多线程或多进程从任务池中取任务。func 会被异步执行。
- `shutdown(wait=True)`：关闭 Executor，释放资源。不管 *wait* 的值是什么，整个 Python 程序将等到所有待执行的 future 对象完成执行后才退出。 

### 2. future 对象详解

future 是 concurrent.futures 模块和 asyncio 包的重要组件。

future 封装待完成的操作，可以放入队列，完成的状态可以查询，得到结果（或抛出异常）后可以获取结果（或异常）。Future 提供了如下方法： 

- `future.result(timeout=None)` ：返回可调用对象的结果，或者重新抛出执行可调用的对象时抛出的异常。**result()会阻塞调用方所在的线程，直到有结果可返回**，但是result()可以接收可选的**timeout参数**，如果在指定的时间内future没有运行完毕，会抛出**TimeoutError异常**。

  ```python
  try:
      print(to_do[9].result(timeout=1))
  except futures.TimeoutError:
      print('TimeoutError')
  ```

- `future.add_done_callback(fn)` ：当 future 对象被取消或完成运行时，将会调用 *fn*，而这个 future 对象将作为它唯一的参数。 

- `future.cancel()` ：尝试取消调用。 如果调用正在执行或已结束运行不能被取消则该方法将返回 `False`，否则调用会被取消并且该方法将返回 `True`。 

- `future.done()`：返回布尔值，指明future链接的可调用对象是否已经执行，**不会阻塞**。

- `future.cancelled()`：返回布尔值，指明future链接的可调用对象是否已经成功取消，**不会阻塞**。

- `future.running()`：返回布尔值，指明future链接的可调用对象是否已经正在执行而且不能被取消，**不会阻塞**。

### 3. map() 源码剖析 

我们知道 map() 是这么调用的：

```python
with futures.ThreadPoolExecutor(workers) as executor: 
    res = executor.map(download_source, urls)
```

前面说过，map() 返回结果的顺序和调用开始的顺序一直，如果第一个调用生成结果用时10秒，而其他调用只用1秒，代码会阻塞10秒以获取第一个结果。map() 封装很优秀，忍不住看了看源码，Executor.map() 定义在 Lib.concurrent.futures._base 中：

```python
def map(self, fn, *iterables, timeout=None, chunksize=1):
    ...
    fs = [self.submit(fn, *args) for args in zip(*iterables)]	# 将可迭代对象使用submit()构造生成futures
    def result_iterator():
        ...
        while fs:
            if timeout is None:
            	yield fs.pop().result()		# fs.pop()按顺序返回一个future; 而future.result()会阻塞
            else:
                yield fs.pop().result(end_time - time.monotonic()) 
        ...
    return result_iterator()
```

可以看到，Executor.map() 内部也是使用了 submit() 和 result()，但是它返回一个迭代器，迭代器中包含的是各个 future 的结果，而非 future 本身。

### 4. ThreadPoolExecutor 核心工作源码剖析

