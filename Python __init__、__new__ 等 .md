# Python self、cls、\_\_call\_\_、\_\_new\_\_、\_\_init\_\_、\_\_del\_\_、\_\_doc\_\_、\_\_str\_\_、

刷各种Python书籍的时候，都会看到很多类里有各种 **\_\_xxx\_\_** 函数，这些函数，涉及到了很多知识点，故想做一个汇总。
https://docs.python.org/3/reference/datamodel.html#object.__init__

## 1. self 和 cls 的区别

### 1.1 self 关键字

`self`是类的每一个实例对象本身，相当于 C++ 的 this 指针。

> self 表示的就是实例对象本身，即类的对象在内存中的地址。	——《编写高质量的代码：改善Python程序的91个建议》

```python
class A:
    def get_self(self):
        return self

a1 = A()
print(a1.get_self())
a2 = a1.get_self()
print(a1 is a2)   # True    说明 a1 和 a2 是同一个实例对象

a3 = A()
print(a3 is a1)   # False   说明 a3 是一个新的实例对象
```

理解了 self 关键字是什么，再看看类内的变量吧，这对我们了解 `cls` 关键字有帮助。

### 1.2 类的变量

它们分为**类的公有变量、保护变量、私有变量**和**实例的公有变量、保护变量、私有变量**。

> ***Python 没有真正的私有。***

很多书上都是这么说的，**但是新版的 Python 已经不能在外部访问 `__xxx ` 私有变量了。**

```python
class A:
    class_public = "class public"           # 类的公有变量
    _class_protected = "class protected"    # 类的保护变量
    __class_private = "class private"       # 类的私有变量
    name = "class A"
    def __init__(self):
        name = 'Local A'            # 局部变量
        self.name = "self A"
        self.instance_public = "instance public"        # 实例的公有变量
        self._instance_protected = "instance protected" # 实例的保护变量
        self.__instance_private = "instance private"    # 实例的私有变量
        print(name)     # Local A	优先访问局部变量

a = A()
# 实例的私有变量，每个类的实例拥有自己的私有变量，各个实例的私有变量互不影响。
print(a.name)                   # self A        同名的 实例私有变量 覆盖了 类的公有变量
print(a.class_public)           # class public
print(a._class_protected)       # class protected   （Pycharm 提示: Access to a protected member _instance_protected of a class）
# print(a.__class_private)        # AttributeError: 'A' object has no attribute '__class_private'
print(a.instance_public)        # instance public
print(a._instance_protected)    # instance protected    （Pycharm 提示: Access to a protected member _instance_protected of a class）
# print(a.__instance_private)     # AttributeError: 'A' object has no attribute '__instance_private'

# 类内，函数外定义的变量，都是类的变量，所有类内函数需要通过 cls 关键字访问类的变量，外部可直接 类名.公有变量名 访问类的公有变量
print(A.name)                   # class A
print(A.class_public)           # class public
print(A._class_protected)       # class protected  （Pycharm 提示: Access to a protected member _class_protected of a class）
# print(A.__class_private)        # AttributeError: type object 'A' has no attribute '__class_private'

A.name = "Changed class A"		# 修改公有变量
print(A.name)
A._class_protected = "Changed class protected"	# 修改保护变量
print(A._class_protected)
```

想要了解更多变量的作用域，推荐文章：[[Python\] 变量名的四个作用域及 nonlocal 关键字](https://blog.csdn.net/Spade_/article/details/107702841)

我们只知道了外部是怎么修改类的公有变量的，那么**类内怎么修改类的公有变量呢？**这就涉及到了 `cls` 关键字了。 

### 1.3 cls 关键字

想要知道 `cls`， 得先了解类方法 `@classmethod` 和静态方法 `@staticmethod` 。

#### 1.3.1 staticmethod和classmethod

Python中的静态方法（staticmethod）和类方法（classmethod）都依赖于装饰器（decorator）来实现。定义方法和调用方法如下：

```python
class A(object):
    def func(self, *args, **kwargs): pass	# self 关键字
    
    @staticmethod
    def func1(*args, **kwargs):	pass		# 不需要 self 和 cls 关键字
    
    @classmethod
    def func2(cls, *args, **kwargs): pass	# 不能缺少 cls 关键字
```

静态方法和类方法都可以**通过类名.方法名（如A.f()）或者实例.方法名（A().f()）的形式来访问**。其中静态方法没有常规方法的特殊行为，如绑定、非绑定、隐式参数等规则，而类方法的调用使用类本身作为其隐含参数，但调用本身并不需要显示提供该参数。

```python
a = A()
a.func()
# A.func()	# 报错 不能访问实例的函数

a.func1()	# 类名.方法名 访问 staticmethod
A.func1()	# 实例.方法名 访问 staticmethod

a.func2()	# 类名.方法名 访问 classmethod		
A.func2()	# 实例.方法名 访问 classmethod		注意：cls 是作为隐含参数传入的
```

类方法 `@classmethod` 用来做什么呢？下面我们看一个例子：

```python
class Fruit(object):
    total = 0
    @classmethod
    def print_total(cls):
        print(cls.total)
        # print(id(Fruit.total))
        # print(id(cls.total))

    @classmethod
    def set_total(cls, value):
        print(f"调用类方法 {cls} {value}")
        cls.total = value

class Apple(Fruit): pass
class Banana(Fruit): pass

Fruit.print_total()		# 0		注意：此处是0，我们会发现后面Apple、Banana修改total不会影响此值
a1 = Apple()
a1.set_total(200)		# 调用类方法 <class '__main__.Apple'> 200
a2 = Apple()			
a2.set_total(300)		# 调用类方法 <class '__main__.Apple'> 300
a1.print_total()		# 300
a2.print_total()		# 300
Apple.print_total()     # 300

b1 = Banana()
b1.set_total(400)		# 调用类方法 <class '__main__.Banana'> 400
b2 = Banana()
b1.print_total()		# 400
b2.print_total()		# 400
Banana.print_total()	# 400

Fruit.print_total()		# 0
Fruit.set_total(100)	# 调用类方法 <class '__main__.Fruit'> 100
Fruit.print_total()		# 100
```

不管你创建多少个 Apple 或 Banana 的类实例对象，这些实例对象都是共用一个 `cls.total` （注意函数内变量前不加 `cls` 关键字的话，则是局部变量）。所以类内是怎么修改类的公有变量的呢？显而易见，**通过 类方法 `@classmethod` 关键字 定义的函数来修改类的公有变量。**

## 2.\_\_call\_\_、\_\_new\_\_、\_\_init\_\_ 

不知道你面试的时候，有没有人问你这三个的区别呢？

https://docs.python.org/3/reference/datamodel.html#object.__init__

### 1. \_\_call\_\_





```python
class A:
    def __del__(self):
        # 当对象被销毁时，会自动调用这个方法
        print('__del__ 方法被调用了')

a = A()
del a
```



```
class A:
    def __del__(self):
        # 当对象被销毁时，会自动调用这个方法
        print('__del__ 方法被调用了')

    def __str__(self):
        # 当对象被销毁时，会自动调用这个方法
        print('__str__ 方法被调用了')
        return "__str__"

class B: pass

a = A()
print(a)
print(A)
del a

b = B()
print(B)
print(b)

```

```
class A(object):
    def __call__(self, *args, **kwargs):
        print("A __call__")
    pass


class B(type):
    def __call__(cls, *args, **kwargs):         # TODO 为什么此处是 cls ？？？
        print("B __call__")


print(A())
print(B())
print(A.__str__)
print(A.__dict__)
print(A.__hash__)
print(A.__dir__)
print(A.__module__)
```

```
class A: pass

a = A()
print(A)
print(a)

class B:
    def __str__(self):
        # 当对象被销毁时，会自动调用这个方法
        print('__str__ 方法被调用了')
        return f"{self.__class__} __str__"

b = B()
print(B)
print(b)

# __str__ 会被继承
class C(B): pass

c = C()
print(C)
print(c)
```

### \_\_dir\_\_





### \_\_eq\_\_

编写高质量的代码 建议16 分清 == 与 is 





### \_\_dict\_\_





### \_\_hash\_\_





### \_\_module\_\_





### ...





参考博客：

<https://www.cnblogs.com/zhouyixian/p/11129347.html> 

<https://blog.csdn.net/mall_lucy/article/details/104489036/> 

<https://www.cnblogs.com/coder2012/p/4309999.html> 



参考书籍：

编写高质量的代码：改善Python程序的91个建议

流畅的Python



## 元类

<https://www.cnblogs.com/tkqasn/p/6524879.html> 

<https://blog.csdn.net/a2011480169/article/details/87891753> 

```
class MyMetaClass(type):
    def __call__(cls, *args, **kwargs):
        print('--自动触发元类当中的__call__方法---')
        #调用__new__产生一个空对象obj
        obj = cls.__new__(cls)
        print(obj)
        print(obj.__dict__)   #此时名称空间为空.
        #调用__init__初始化这个对象.
        cls.__init__(obj,*args,**kwargs)
        #返回初始化的对象
        print(obj.__dict__)

        return obj



class Person(object, metaclass=MyMetaClass):  # 这一行: Person = MyMetaClass('Person',(object,),{...})

    country = 'China'

    def __init__(self, name, age):
        print('-----Person--init-----')
        self.name = name
        self.age = age

    def tell_info(self):
        print('%s 的年龄是:%s' % (self.name, self.age))

    def __new__(cls, *args, **kwargs):
        print('---------new--------')
        return super().__new__(cls)


print(callable(Person))
person = Person('wtt',25)   #Person这个类之所以可以被调用,肯定是因为造出Person的类：MyMetaClass当中含有__call__方法.
print(person)
```
