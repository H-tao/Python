## 3. \_\_del\_\_

### 3.1 \_\_del\_\_使用方法

**\_\_del\_\_**方法为“析构方法”，用于实现对象被销毁时所需的操作。常用于释放对象所占用的资源，如文件资源、网络连接、数据库连接等。

```python
class A:
    def __del__(self):
        # 当对象被销毁时，会自动调用这个方法
        print('__del__ 方法被调用了')

a = A()
del a

# __del__ 方法被调用了
```

什么时候对象会被销毁呢？这取决于 Python 的垃圾回收机制。我们先看看这句话：

> `del x` 并不直接调用 `x.__del__()` 。前者会将 `x` 的引用计数减一，而后者仅会在 `x` 的引用计数变为零时被调用。

这个是怎么回事呢？我们看看下面这个代码：

```python
import time
class A:
    def __del__(self):
        # 当对象被销毁时，会自动调用这个方法
        print('__del__ 方法被调用了')

a1 = A()
a2 = a1
del a1
for x in range(5):
    print("waiting...")
    time.sleep(1)
del a2


# waiting...
# waiting...
# waiting...
# waiting...
# waiting...
# __del__ 方法被调用了
```

输出5个 waiting... ，且 a1、a2 都被`del`了，`__del__` 方法才被调用，而且只被调用了一次。

### 3.2 垃圾回收机制

Python 使用**引用计数器（Reference counting）**的方法来管理内存中的对象，即针对每一个对象维护一个引用计数值来表示该对象当前有多少个引用。当其他对象引用该对象时，其引用计数会增加1，而删除一个对当前对象的引用，其引用计数会减1。只有当引用计数的值为0的时候该对象才会被垃圾收集器回收，因为它表示这个对象不再被其他对象引用，是个不可达对象。

**缺点：**无法解决循环引用的问题，即两个对象相互引用。因为两个对象的引用计数器都不为0，该对象并不会被垃圾收集器回收，而无限循环导致一直在申请内存而没有释放，所以最后出现了内存耗光的情况。例如：

```python
class Leak:
    def __init__(self):
        print(f"object {id(self)} created")

while True:
    A = Leak()
    B = Leak()
    A.b = B     # 循环引用
    B.a = A     # 循环引用
    A = None
    B = None
```

两种方式可以触发垃圾回收：

- 通过显式地调用**gc.collect()**进行垃圾回收。详情参考[gc 模块](https://docs.python.org/zh-cn/3/library/gc.html#module-gc)。
- 在创建新的对象为其分配内存的时候，检查threshold阈值，当对象的数量超过threshold的时候便自动进行垃圾回收。

