concurrent.futures模块的主要特色是ThreadPoolExecutor和ProcessPoolExecutor类，这两个类实现的接口能分别在不同的线程或进程中执行可调用的对象。这两个类在内部维护着一个工作线程或进程池，以及要执行的任务队列。 



1. 线程什么时候被创建？
2. 任务是如何被线程处理的？







### 核心工作详解

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

#### executor.submit()的核心

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
    self._adjust_thread_count()		# 调整线程数量
    return f	# 返回future
```

#### Future对象

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

#### WorkItem对象

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

