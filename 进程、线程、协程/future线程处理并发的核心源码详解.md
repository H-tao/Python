### ThreadPoolExecutor 核心工作详解

1. ThreadPoolExecutor内部是如何工作的？
2. 什么是future对象？
3. 线程什么时候被创建？
4. 任务是如何被线程处理的？
5. 结束之后如何销毁的

#### 1. ThreadPoolExecutor 

我们所有的工作都是在`ThreadPoolExecutor`完成的：

```python
with futures.ThreadPoolExecutor(max_workers=2) as executor:
    ...
```

executor中定义了几个关键的变量。

```python
class ThreadPoolExecutor(_base.Executor):
    def __init__(self, max_workers=None, thread_name_prefix='', ...):
        self._max_workers = max_workers		# 最大线程数
        self._work_queue = queue.SimpleQueue()	# 任务池Queue，所有线程从该Queue中取任务然后执行
        self._threads = set()	# 线程池
```

#### 2. executor.submit() 的核心

future对象是我们通过调用submit()时返回的。

```python
future = executor.submit(sleep_and_print, _i)	# submit
```

看看submit() 做了哪些事情：

```python
# def submit(*args, **kwargs)对参数进行了处理，实际上相当于这样：
def submit(self, fn, *args, **kwargs):	
    ...
    # 下面是核心代码
    f = _base.Future()		# 创建一个Future()对象
    w = _WorkItem(f, fn, args, kwargs)	# 创建一个_WorkItem，传入可调用的fn和fn的所有参数

    self._work_queue.put(w)		# 将_WorkItem加入_work_queue
    self._adjust_thread_count()		# 调整线程数量，线程就是在这个函数中被创建的
    return f	# 返回future
```

#### 3. Future 对象

future对象初始化时，定义了几个实例变量。

```python
class Future(object):
    """代表一个异步计算的结果"""

    def __init__(self):
        """Initializes the future. Should not be called by clients."""
        self._condition = threading.Condition()
        self._state = PENDING		# 状态。
        self._result = None			# 结果。处理调用方传入的fn的结果，_result = fn(*args, **kwargs)
        self._exception = None		# 异常值。处理fn时，若fn抛出异常，则设置改异常值。
        self._done_callbacks = []	# 回调函数数组。用于处理add_done_callback传入的可调用对象。
```

future有五种状态：

```css
_FUTURE_STATES = [
    PENDING,
    RUNNING,
    CANCELLED,
    CANCELLED_AND_NOTIFIED,
    FINISHED
]
```

#### 4. WorkItem 对象

WorkItem和future是一对一的，submit()会为每一个future都创建一个WorkItem。WorkItem记录待处理的任务fn及其参数，线程会从work_queue中取出WorkItem，调用它的run()方法。WorkItem只定义了一个run()方法：

```python
class _WorkItem(object):
    def __init__(self, future, fn, args, kwargs):
        self.future = future	# future
        self.fn = fn			# fn
        self.args = args		# fn的参数
        self.kwargs = kwargs	# fn的参数

    def run(self):
        if not self.future.set_running_or_notify_cancel():
            return

        try:
            result = self.fn(*self.args, **self.kwargs)		# 调用fn
        except BaseException as exc:
            self.future.set_exception(exc)		# 如果fn有报错，设置错误类型给future
            # Break a reference cycle with the exception 'exc'
            self = None
        else:
            self.future.set_result(result)		# 将fn的返回值，设置给future
```

####5. executor._adjust_thread_count 函数

```python
def _adjust_thread_count(self):
    def weakref_cb(_, q=self._work_queue):	# 这个函数貌似没什么用，后文分析
        ...
        
    num_threads = len(self._threads)	# _threads是已经创建的线程集合(set)
    if num_threads < self._max_workers:		# 如果已创建的线程数小于最大线程数
        thread_name = '%s_%d' % (self._thread_name_prefix or self,
                                 num_threads)		# 线程名=线程名前缀+线程序号
        t = threading.Thread(name=thread_name, target=_worker,
                             args=(weakref.ref(self, weakref_cb),
                                   self._work_queue,
                                   ...))		# 创建线程，主要的两个参数是weakref.ref(self, weakref_cb), self._work_queue。前者是当前executor的弱引用，后者是executor的任务池
        t.daemon = True		# 守护线程。主线程退出时，守护线程会自动退出
        t.start()		# 启动线程
        self._threads.add(t)	# 加入已创建的线程集合
        _threads_queues[t] = self._work_queue	# _threads_queues是一个全局的弱引用WeakKeyDictionary，记录所有executor的任务池，以便退出时进行清理操作
```

```python
 t = threading.Thread(name=thread_name, target=_worker,)
```

这个 target 指向的 _worker 函数很关键，它会执行一个 while True 循环，从 work_queue 中不断获取 work_item， 然后执行 work_item 的 run() 方法：

```python
def _worker(..., work_queue, ...):
    try:
        while True:
            work_item = work_queue.get(block=True)  # 从 work_queue 中取一个 _WorkItem
            if work_item is not None:
                work_item.run()     # 调用 _WorkItem.run()
                # del 删除对象的引用，会将 x 的引用计数减一，当引用计数为0时，调用 x.__del__() 销毁实例。
                del work_item
                continue
            ...
    except BaseException:
        _base.LOGGER.critical('Exception in worker', exc_info=True)
```

这里没有贴出线程退出 While True 的循环，是不想代码过于复杂了。如果感兴趣，可以自己查看源码。

如果你对 weakref.ref(self, weakref_cb) 不理解，下面我讲关键代码提炼出来，模拟该弱引用：

不知道什么是弱引用，请先参考文章：[[Python] 高级用法 - 弱引用详解](https://blog.csdn.net/spade_/article/details/108114785)

```python
import weakref


def _worker(executor_reference):
    print('Enter function: _worker')
    print(executor_reference)
    executor = executor_reference()
    print(executor)
    if executor is not None:
        executor.say_hello()


def run():
    a = A('DemoA')

    def weakref_cb(_):
        print('Enter function: weakref_cb')

    print((weakref.ref(a, weakref_cb)))
    print(weakref.ref(a))

    _worker((weakref.ref(a, weakref_cb)))   # 两行代码效果相同
    _worker(weakref.ref(a))                 # 两行代码效果相同


class A:
    def __init__(self, name):
        self.name = name

    def say_hello(self):
        print(f"Hello, I am {self.name}.")


if __name__ == '__main__':
    run()
```

weakref_cb 并没有被执行：

```shell
<weakref at 0x0000027068011958; to 'A' at 0x000002707F073848>
<weakref at 0x0000027068011958; to 'A' at 0x000002707F073848>
Enter function: _worker
<weakref at 0x0000027068011958; to 'A' at 0x000002707F073848>
<__main__.A object at 0x000002707F073848>
Hello, I am DemoA.
Enter function: _worker
<weakref at 0x0000027068011958; to 'A' at 0x000002707F073848>
<__main__.A object at 0x000002707F073848>
Hello, I am DemoA.
```

#### 6. executor 如何退出

使用 `with` 关键字，在结束时会调用`__exit__`方法，这个方法调用了 shutdown() 方法。 shutdown() 会做两件事：第一，给 work_queue 传入一个 None 值，线程执行时，获取到 None 就会退出 While True 循环； 第二，如果 wait 为 True，将剩余所有未执行完的线程，调用它们的 join() 方法，让主线程等待它们完成：

```python
class Executor(object):
    ...
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown(wait=True)
        return False
    
class ThreadPoolExecutor(_base.Executor):
    ...
    def shutdown(self, wait=True):
        with self._shutdown_lock:
            self._shutdown = True
            self._work_queue.put(None)
        if wait:
            for t in self._threads:
                t.join()
```

