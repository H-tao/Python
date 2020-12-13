## 开始

concurrent.futures模块的主要特色是ThreadPoolExecutor和ProcessPoolExecutor类，这两个类实现的接口能分别在不同的线程或进程中执行可调用的对象。这两个类在内部维护着一个工作线程或进程池，以及要执行的任务队列。不过，这个接口抽象的层级很高。

```python
from concurrent import futures

def download_source(url):
    pass

urls = ['https://www.python.org/ftp/python/3.7.5/Python-3.7.5.tgz',
        'https://www.python.org/ftp/python/3.7.6/Python-3.7.6.tgz',
        'https://www.python.org/ftp/python/3.8.0/Python-3.8.0.tgz']

with futures.ThreadPoolExecutor(max_workers=3) as executor:
    to_do = []
    for url in urls:
        future = executor.submit(download_source, url)
        to_do.append(future)

    results = []
    for future in futures.as_completed(to_do):
        res = future.result()
        results.append(res)
```

future是concurrent.futures模块和asyncio包的重要组件。

future封装待完成的操作，可以放入队列，完成的状态可以查询，得到结果（或抛出异常）后可以获取结果（或异常）。

- `future.done()`：返回布尔值，指明future链接的可调用对象是否已经执行，**不会阻塞**。
- `future.result(timeout=None)` ：返回可调用对象的结果，或者重新抛出执行可调用的对象时抛出的异常。**result()会阻塞调用方所在的线程，直到有结果可返回**，但是result()可以接收可选的**timeout参数**，如果在指定的时间内future没有运行完毕，会抛出**TimeoutError异常**。
- 

```python
with futures.ThreadPoolExecutor(workers) as executor: 
    res = executor.map(download_source, urls)
    
print(len(list(res)))
```

Executor.map()定义在Lib.concurrent.futures._base中：

```python
def map(self, fn, *iterables, timeout=None, chunksize=1):
    ...
    fs = [self.submit(fn, *args) for args in zip(*iterables)]	# 将可迭代对象使用submit()构造成futures
    def result_iterator():
        ...
        while fs:
            if ...:
            	yield fs.pop().result()
            else:
                yield fs.pop().result(end_time - time.monotonic())
        ...
    return result_iterator()
```

可以看到，Executor.map()返回一个迭代器，迭代器中包含的是各个future的结果，而非future本身。map()接收的参数就不再一一说明了。

