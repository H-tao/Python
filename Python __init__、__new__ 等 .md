## Python cls、\_\_call\_\_、\_\_new\_\_、\_\_init\_\_、\_\_del\_\_、\_\_doc\_\_、\_\_str\_\_、

### self 和 cls

我们先看看 self，self 是类的一个实例对象：

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

再看 cls，讲 cls 之前，我们不得不知道 @classmethod



### 类方法和静态方法

```
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

a1 = Apple()
a1.set_total(200)
a2 = Apple()
a2.set_total(300)
a1.print_total()
a2.print_total()
Apple.print_total()     # 可以直接使用 类名.类方法() 调用

b1 = Banana()
b1.set_total(400)
b2 = Banana()
b1.print_total()
b2.print_total()
Banana.print_total()
```

### \_\_init\_\_





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
