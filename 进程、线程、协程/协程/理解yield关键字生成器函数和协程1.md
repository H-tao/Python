主旨：

1. 介绍yield关键字的用法、生成器和生成器函数
2. 什么是协程、生成器函数和协程的区别
3. 从yield到yield from，引出异步编程
4. future库的用法
5. 





















## yield、生成器和生成器函数

下面讲一个例子，demo1()里面使用了yield，是一个生成器函数，返回一个生成器。我们可以使用next()方法来迭代生成器，每次迭代next()获取到的就是**yield产生的值，也就是yield右边的值**。

```python
# yield可以理解为暂停按钮，每次执行到yield，保存断点，同时yield还会返回值给调用方
def demo1(value=None):
    print('start')
    yield 1
    yield value
    yield 2
    print('end')

g = demo1("Value")	# 生成器函数也是函数，可以接收传参
print(type(g))   # g是一个生成器
print(next(g))   # 执行yield 1，暂停
print(next(g))   # 执行yield value，暂停
print(next(g))   # 执行yield 2，暂停
print(next(g))   # 找不到yield了，raise StopIteration
```

```javascript
<class 'generator'>
start
1
Value
2
end
Traceback (most recent call last):
  File "D:/Desktop/Projects/效率编程/协程/test.py", line 14, in <module>
    print(next(g))   # 找不到yield了，raise StopIteration
StopIteration
```

总共三次yield，我们是调用方，使用next(g)收到了三个yield返回值，当我们尝试调用第四次时，demo1函数产生了一个`StopIteration`告诉我们找不到yield了，raise StopIteration。

## next()和send()的因缘

先讲讲next()和send()的因缘。

### next() == send(None)

```powershell
>>> def demo2(value=None):
...     print('start')
...     a = yield 1
...     print("demo1 Received: ", a)
...     b = yield value
...     print("demo1 Received: ", b)
...
>>> g = demo2("Value")
>>> next(g)
start
1
>>> g = demo2("Value")
>>> g.send(None)
start
1
>>>
```

为什么说next() == send(None)？我们看看底层代码！

Python底层是由C语言实现的，让我们摘出next()和send()来观察看看！ 

```python
static PyObject *
gen_iternext(PyGenObject *gen)
{
    return gen_send_ex(gen, NULL, 0);  # 传入NULL
}


static PyObject *
gen_send(PyGenObject *gen, PyObject *arg)
{
    return gen_send_ex(gen, arg, 0);  # 传入可变参数
}
```

### send() 给生成器函数传值

我们在上面讲到了yield通过`yield item`可以返回值给调用方，调用方可以通过next()获取到yield的产出值。其实yield还可以接受调用方传来的值，通过`data = yield`，生成器函数内就可以接收调用方传来的值。`data = yield item` 可以产出一个值item给调用方，同时接收调用方（调用方使用send）传来的值，然后暂停执行，作出让步，使调用方继续工作，直到调用方下次继续执行send。

1. `yield item`：产出值item给调用方。
2. `data = yield`：data接收值，下一次send()时，data才会接收到上一次send()的值。
3. `data = yield item`：产出值和接收值，先yield item产出值，下一次send()时，data才会接收到上一次send()的值。所以分为yield item 和 data = yield 两步走。

为了理解产出值和接收值，我们看一个产出值和接收值的例子：

```python
def demo2(value=None):
    print('start')
    a = yield 1
    print("demo1 Received: ", a)
    b = yield value
    print("demo1 Received: ", b)
    c = yield 2
    print("demo1 Received: ", c)
    print('end')

g = demo2("Value")
print(type(g))   # g是一个生成器
print(next(g))   # 执行yield 1，暂停
print(g.send(100))   # 执行yield value，暂停
print(g.send(200))   # 执行yield 2，暂停
print(g.send(300))   # 找不到yield了，raise StopIteration
```

```javascript
<class 'generator'>
start
1
demo1 Received:  100
Value
demo1 Received:  200
2
demo1 Received:  300
end
Traceback (most recent call last):
  File "D:/Desktop/Projects/效率编程/协程/test.py", line 17, in <module>
    print(g.send(300))   # 找不到yield了，raise StopIteration
StopIteration
```

## 使用Pycharm的DEBUG模式理解data = yield item的执行过程

还是上面的那段代码，在14行打上断点：

```python
def demo2(value=None):
    print('start')
    a = yield 1
    print("demo1 Received: ", a)
    b = yield value
    print("demo1 Received: ", b)
    c = yield 2
    print("demo1 Received: ", c)
    print('end')

g = demo2("Value")
print(type(g))   
print(next(g))   # 在这里打上断点
print(g.send(100))   
print(g.send(200))   
print(g.send(300))  
```

在Pycharm中，按`Shift+F9`，进入Debug模式，代码运行到14行，接下来按`F7`就行了。

按`F7` 首次进入demo2函数内。在运行到第一个send()，第二次进入demo2函数内的时候，a才被赋值100。在运行到第二个send()，第三次进入demo2函数内的时候，b才被赋值200。c同理。

## 协程

什么是协程？这是第一个问题。很多博客和书都在讲协程，但是并没有给出协程定义。也有人把协程叫做“微线程”，下面给出书上的原话：

> 协程是指一个过程，这个过程与调用方协作，产出由调用方提供的值。 ——《流程的Python》

区别生成器函数和协程：

1. 包含`yield`关键字的函数就是`生成器函数`。
2. 通过`data = yield`，生成器函数内就可以接收调用方传来的值，接收值的生成器函数，就可以理解为Python的`协程`。



## 个人对yield关键字、协程的理解

普通的函数，都是等待接收方调用，调用一次执行（接收参数、执行函数体、返回值）就结束了。如果有一个函数，在一次调用内，既能够接收你传入的值n次，又能返回值m次给你，在执行过程中，可以暂停等待你传值，直到你需要再次启动，是不是感觉有点牛逼？没错，Python里yield关键字就可以做到这件事。`data = yield item` 可以产出一个值item给调用方，同时接收调用方（调用方使用send）传来的值，然后暂停执行，作出让步，使调用方继续工作，直到调用方下次继续执行send。

总之，我个人理解，`data = yield item` 执行过程可以理解为产出值、暂停、接收值上一次send传来的值，依次反复。

