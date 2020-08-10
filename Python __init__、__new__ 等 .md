# Python self、cls、\_\_call\_\_、\_\_new\_\_、\_\_init\_\_、\_\_del\_\_、\_\_doc\_\_、\_\_str\_\_、

刷各种Python书籍的时候，都会看到很多类里有各种 **\_\_xxx\_\_** 函数，这些函数，涉及到了很多知识点，故想做一个汇总。
https://docs.python.org/3/reference/datamodel.html#object.__init__

## 1. self 和 cls 的区别

一句话，`cls` 代表类，`self` 代表实例对象。

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

实际上**_\_init\_\_**并不是真正意义上的构造方法，**_\_init\_\_**方法所做的工作是在类的对象创建好之后进行变量的初始化。**_\_new\_\_**方法才会真正创建实例，是类的构造方法。一个可调用的对象加括号，就是触发这个对象所在的类中的**\_\_call\_\_**方法的执行。

### 1. \_\_call\_\_

此方法会在实例作为一个函数被“调用”时被调用；如果定义了此方法，则 `x(arg1, arg2, ...)` 就相当于 `x.__call__(arg1, arg2, ...)` 的快捷方式。

> 不仅Python函数是真正的对象，任何Python对象都可以表现得像函数。为此，只需实现实例方法\_\_call\_\_。——《流畅的Python》

```python
class A:
    def __init__(self):
        self.__name = "A"   # 私有变量

    def __call__(self, *args, **kwargs):
        print(f"{self.__get_name()} {args} {kwargs}")

    def __get_name(self):   # 私有函数
        return self.__name

a = A()
a() 			# A () {}
a.__call__()    # A () {}
print(callable(a))  # True
```
注意：在元类中，**\_\_call\_\_**的首个参数为 `cls`。看不懂以下代码没关系，可以先跳过。

```python
class A(type):
    def __call__(cls, *args, **kwargs):
        print("metaclass A __call__")
        print(f"{cls} {args} {kwargs}")

class B(metaclass=A):
    def __init__(self):
        self.__name = "B"
        
b = B()

# metaclass A __call__
# <class '__main__.B'> () {}
```

### 2. _\_new\_\_

调用类时会运行类的**_\_new\_\_**方法创建一个实例，然后运行**_\_init\_\_**方法，初始化实例，最后把实例返回给调用方。

> 一般情况下不需要覆盖**_\_new\_\_**方法。

```python
class A:
    def __new__(cls, *args, **kwargs):
        #__new__是一个类方法，在对象创建的时候调用
        print("调用 __new__")
        # super 父类是 object
        return super().__new__(cls)   # 或者 super(A, cls).__new__(cls)


    def __init__(self):
        #__init__是一个实例方法，在对象创建后调用，对实例属性做初始化
        print("调用 __init")
        self.name = "A"


a = A()   # 调用 __new__    调用 __init
print(a.name)     # A
```

**_\_new\_\_**使用情况：

1. 当类继承（如str、int、unicode、tuple或者forzenset等）不可变类型且默认的**_\_new\_\_**()方法不能满足需求的时候。

2. 用来实现工厂模式或者单例模式或者进行元类编程（元类编程中常常需要使用**_\_new\_\_**()来控制对象创建。

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
```

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

- 通过显式地调用**gc.collect()**进行垃圾回收。
- 在创建新的对象为其分配内存的时候，检查threshold阈值，当对象的数量超过threshold的时候便自动进行垃圾回收。

## 4. \_\_str\_\_、\_\_repr\_\_

我们直接打印对象或者使用**str()**、和**repr()**打印对象时，分别会调用**\_\_str\_\_()、\_\_repr\_\_()**两个函数。

### 4.1 \_\_str\_\_

打印对象时，会调用对象的 **\_\_str\_\_()** 方法，默认会打印类名和对象的地址名。

```python
class A: pass

class B:
    def __str__(self):
        print('B 的 __str__ 方法被调用了')
        return f"{super().__str__()}"	# 默认 super 为 object 

class C:
    def __str__(self):
        return 'C 的 __str__ 方法被调用了'

class D(C): pass    # __str__ 会被继承


a, b, c, d = A(), B(), C(), D()
print(a)		 # <__main__.A object at 0x000001FDC04B1788> 
print(str(a))    # <__main__.A object at 0x000001FDC04B1788>
print(b)		 # B 的 __str__ 方法被调用了     <__main__.B object at 0x000001FDCF53EC48>
print(str(b))    # B 的 __str__ 方法被调用了     <__main__.B object at 0x000001FDCF53EC48>
print(c)		 # C 的 __str__ 方法被调用了
print(str(c))    # C 的 __str__ 方法被调用了
print(d)		 # C 的 __str__ 方法被调用了
print(str(d))    # C 的 __str__ 方法被调用了
```
### 4.2 \_\_repr\_\_

当不存在 \_\_str\_\_() 时，会转而调用 \_\_repr\_\_() 。

```python
class A:
    def __repr__(self):
        print(super().__repr__())
        return 'A 的 __repr__ 方法被调用了'

class B(A): pass    # __repr__ 会被继承


a, b = A(), B()
print(a)    # <__main__.A object at 0x000002A31AC50408>     A 的 __repr__ 方法被调用了
print(str(a))
print(repr(a))
print(b)    # <__main__.B object at 0x000002A31AC4ED48>     A 的 __repr__ 方法被调用了
print(str(b))
print(repr(b))
```

### 4.3 两者区别
1）两者之间的目标不同：**str()**主要面向用户，其目的是可读性，返回形式为用户友好性和可读性都较强的字符串类型；而**repr()**面向的是Python解释器，或者说开发人员，其目的是准确性，其返回值表示Python解释器内部的含义，常作为编程人员debug用途。

2）在解释器中直接输入a时默认调用repr()函数，而print(a)则调用str()函数。

3）repr()的返回值一般可以用eval()函数来还原对象，通常来说有如下等式。

```python
obj == eval(repr(obj))
```

4）这两个方法分别调用内建的\_\_str\_\_()和\_\_repr\_\_()方法，一般来说在类中都应该定义\_\_repr_\_\_()方法，而__\_\_str\_\_()方法则为可选，当可读性比准确性更为重要的时候应该考虑定义\_\_str\_\_()方法。如果类中没有定义__\_\_str\_\___()方法，则默认会使用__\_\_repr\_\_()方法的结果来返回对象的字符串表示形式。用户实现\_\_repr\_\_()方法的时候最好保证其返回值可以用eval()方法使对象重新还原。

## 5. _\_class\_\_

<https://luobuda.github.io/2015/01/16/python-class/> 

<http://brionas.github.io/2014/09/15/python-type-class/> 

```
class A(object): pass

a = A()
print(a.__class__, type(a))	# <class '__main__.A'> <class '__main__.A'>
print(A.__class__, type(A))	# <class 'type'> <class 'type'>
```


```
class A(object): pass

a = A()
print(a.__class__, type(a))
print(A.__class__, type(A))

class B(type): pass

class C(metaclass=B): pass

a, c = A(), C()
print(B.__class__, type(B))
print(object.__class__, type(object))
print(c.__class__, type(c))
print(C.__class__, type(C))
print(dir(a))
print(A.__dict__)
print(isinstance(C, (type, object)))
print(issubclass(B, type))
print(isinstance(C, object))
print(isinstance(B, object), issubclass(B, object))
print(isinstance(A, type))
print(isinstance(int, object))
print(isinstance(object, type), issubclass(object, type))
```



```
class A(object):
    def __call__(self, *args, **kwargs):
        print("A __call__")
    pass


class B(type):
    def __call__(cls, *args, **kwargs):         # TODO 此处是 cls
        print("B __call__")


print(A())
print(B())
print(A.__str__)
print(A.__dict__)
print(A.__hash__)
print(A.__dir__)
print(A.__module__)
```

## 6. _\_doc\_\_



### \_\_dir\_\_





### \_\_eq\_\_

编写高质量的代码 建议16 分清 == 与 is 





### \_\_dict\_\_





### \_\_hash\_\_





### \_\_module\_\_



### dir()





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

