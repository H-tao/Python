> 描述符是对多个属性运用相同存取逻辑的一种方式。例如，Django ORM 和 SQLAlchemy 等 ORM 中的字段类型是描述符，把数据库记录中字段里的数据与 Python 对象的属性对应 起来。 描述符是实现了特定协议的类，这个协议包括 `__get__`、`__set__` 和 `__delete__` 方 法。property 类实现了完整的描述符协议。通常，可以只实现部分协议。其实，我们在真实的代码中见到的大多数描述符只实现了 `__get__`和 `__set__` 方法，还有很多只实现了其中的一个。 描述符是 Python 的独有特征，不仅在应用层中使用，在语言的基础设施中也有用到。除了特性之外，使用描述符的 Python 功能还有方法及 classmethod 和 staticmethod 装饰器。理解描述符是精通 Python 的关键。  ——《流畅的Python》

### 什么是描述符？

实现了 `__get__`、`__set__` 或 `__delete__` 方法的类是描述符。描述符的用法是，创建 一个实例，作为另一个类的类属性。 

```python
class Grade(object):
    def __get__(self, instance, owner):
        pass    # 暂时忽略这部分实现的代码

    def __set__(self, instance, value):
        pass    # 暂时忽略这部分实现的代码

class Exam(object):
    math_grade = Grade()		# 描述符将 Grade 作为类属性
    writing_grade = Grade()
    science_grade = Grade()
```

Python 访问描述符属性时，会对这种访问操作进行转译。这点很重要，我们先看看这种转译：

为属性赋值时：

```python
exam = Exam()
exam.writing_grade = 40
```

Python 会将代码转译为：

```python
Exam.__dict__['writing_grade'].__set__(exam, 40)
```

获取属性时：

```python
exam.writing_grade
```

Python 会将代码转译为：

```python
Exam.__dict__['writing_grade'].__get__(exam, Exam)
```

之所以会有这样的转译，关键在于 object 类的 `__getattribute__` 方法。简单来说，如果 Exam 实例没有名为 writing_grade 的属性，那么 Python 就会转向 Exam 类，并在该类中查找同名的类属性。这个类属性，如果是实现了 `__get__` 和 `__set__` 方法的对象，那么 Python 就认为此对象遵从描述符协议。

### 理解类属性和实例属性访问的不同

我们说过实例属性的访问顺序是这样的：

> Python 实例属性访问链：`__getattribute__() `-> `property.get()` -> `__getattr__` 
>
> 1. `__getattribute__() `：访问属性必被调用。
> 2. `property.get()` ：当属性不在实例、基类和祖先类的`__dict__`中时，被调用。
> 3. `__getattr__` ：当属性不在实例、基类和祖先类的`__dict__`中、`__getattribute__() `或 `property.get()` 抛出异常时，被调用。

```python
class Student:
    @property
    def name(self):
        print('Student.property.get')
        raise AttributeError	  # 抛出异常会调用__getattr__

    def __getattr__(self, item):
        print('Student.__getattr__')
        if item == 'name':
            return 'John'

    def __getattribute__(self, item):
        print('Student.__getattribute__')
        return super().__getattribute__(item)

john = Student()
print(john.name)
```

```css
Student.__getattribute__
Student.property.get
Student.__getattr__
John
```

而类属性的访问顺序是：

> `__getattribute__() `->  描述符类的 `__get__()`

假如我们创建一个 Apple 类，在 Student 中创建一个 Apple 实例作为类属性：

```python
class Apple(object):
    def __init__(self):
        self.name = 'RedApple'

    def __get__(self, instance, owner):
        print('Apple.__get__')
        return self

    def __getattribute__(self, item):
        print('Apple.__getattribute__')
        return super().__getattribute__(item)

class Student:
    apple = Apple()     # Apple 实例作为类属性，这是重点！！！

    @property
    def name(self):
        print('Student.property.get')
        raise AttributeError

    def __getattr__(self, item):
        print('Student.__getattr__')
        if item == 'name':
            return 'John'

    def __getattribute__(self, item):
        print('Student.__getattribute__')
        return super().__getattribute__(item)

john = Student()
print(john.name)
print('-----------')
print(john.apple)
print('-----------')
print(john.apple.name)
```

```css
Student.__getattribute__
Student.property.get
Student.__getattr__
John
-----------
Student.__getattribute__
Apple.__get__
<__main__.Apple object at 0x000001F41FFE94C8>
-----------
Student.__getattribute__
Apple.__get__
Apple.__getattribute__
RedApple
```

可以看到 apple 作为 Student 的类属性，并不会访问 `Student.__getattr__` ，而直接转向了 `Apple.__get__` 。

### 开始写描述符

明白了描述符的转译方式和类属性的访问方式之后，下面我们先看错误的示例，这是刚刚开始写的时候很容易犯的错误：

```python
class Grade(object):
    def __init__(self):
        self._value = 0

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._value = value

class Exam(object):
    math_grade = Grade()
    writing_grade = Grade()

first_exam = Exam()
first_exam.writing_grade = 40

second_exam = Exam()
first_exam.writing_grade = 50

print(first_exam.writing_grade, second_exam.writing_grade)  # 50 50
```

多个 Exam 实例操作某一属性，导致了错误的结果。产生这种问题的原因是：对于 writing_grade 这个类属性来说，所有的 Exam 实例都要共享同一份 Grade 实例。同一时刻，内存中可能有几千个 Exam 实例，不过只会有两个描述符实例：Exam.math_grade 和 Exam.writing_grade。因此，存储在描述符实例中的数据，其实会变成 Exam 类的类属性，从而由全部 Exam 实例共享。 

为了解决这个问题，我们可以在 Grade 类中用字典来保存每个 Exam 实例的状态：

```python
class Grade(object):
    def __init__(self):
        self._values = {}

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._values[instance] = value

class Exam(object):
    math_grade = Grade()
    writing_grade = Grade()

first_exam = Exam()
first_exam.writing_grade = 40

second_exam = Exam()
second_exam.writing_grade = 50

print(first_exam.writing_grade)     # 40
print(second_exam.writing_grade)    # 50
```

上面这种实现方式很简单，也容易理解，但它会泄露内存。在程序的生命周期内，对于传给`__set__` 方法的每个 Exam 实例来说， `_value`字典都会保存指向该实例的一份引用。这就导致该实例的引用计数无法降为0，从而使垃圾收集器无法将其回收。我们可以使用 weakref 模块的 WeakKeyDictionay  来解决这个问题。WeakKeyDictionary，其**键是弱引用**，被引用的键对象在程序中的其他地方被当作垃圾回收后，对应的值会自动从 WeakKeyDictionary 中删除。如果不清楚弱引用。可以参考 [Python 高级用法 - 弱引用详解](https://blog.csdn.net/spade_/article/details/108114785)。

```python
from weakref import WeakKeyDictionary

class Grade(object):
    def __init__(self):
        self._values = WeakKeyDictionary()		# 仅有这里变化
......
```

#### 理解 self、instance 和 owner 参数

在我们上面的例子中， Grade中的`__get__(self, instance, owner)`方法的 self 就是 Exam 类中的 math_grade、writing_grade 实例；instance 就是 Exam 实例（如 first_exam、second_exam）；owner 就是 Exam 类。

```python
class Grade(object):
    def __init__(self, name):
        self.name = name
        self._values = {}

    def __get__(self, instance, owner):
        print(self.name, instance.name, owner.name)
        if instance is None:
            return self
        return self._values.get(instance, 0)    # 默认为0


class Exam(object):
    name = 'Exam'
    math_grade = Grade('math_grade')
    writing_grade = Grade('writing_grade')

    def __init__(self, name):
        self.name = name


first_exam = Exam('first_exam')
second_exam = Exam('second_exam')
print(first_exam.writing_grade)
print(second_exam.writing_grade)
```

```css
writing_grade first_exam Exam
0
writing_grade second_exam Exam
0
```

> 注意，`__get__` 方法有三个参数：self、instance 和 owner。owner 参数是托管类（如 Exam）的引用，通过描述符从托管类中获取属性时用得到。如果使用 Exam.math_grade 从类中获取托管属性（以 math_grade 为例），描述符的 `__get__` 方法接 收到的 instance 参数值是 None。 

有个小细节，`__get__` 方法中 __if instance is None: return self__ 这段代码：

```python
class Grade(object):
    def __get__(self, instance, owner):
        if instance is None:
            print('instance is None')
            return self

class Exam(object):
    math_grade = Grade()
    writing_grade = Grade()
    
print(Exam.math_grade)
```

```css
instance is None
<__main__.Grade object at 0x000001977EDD3B08>
```

### 使用 getattr  和 setattr 替代字典以改写描述符类

我们之前都是将 first_exam.writing_grade 的值保存在字典中，这不是很方便，我们可以利用 Python 本身的动态属性来改写代码，将 first_exam.writing_grade 的值使用 setattr 和 getattr 来设置和获取，保存在 first_exam 的属性字典 `__dict__中`：

```python
class Grade(object):
    def __init__(self, name):
        self.name = name
        self.internal_name = '_' + name

    def __get__(self, instance, owner):
        print(self.name, instance.name, owner.name)
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')  # 最后一个 '' 是指获取不到实例名为 internal_name 的值时，返回空字符串

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


class Exam(object):
    name = 'Exam'
    math_grade = Grade('math_grade')
    writing_grade = Grade('writing_grade')

    def __init__(self, name):
        self.name = name
```

```python
first_exam = Exam('first_exam')
second_exam = Exam('second_exam')
print(first_exam.__dict__)
print(second_exam.__dict__)
first_exam.writing_grade = 10
first_exam.math_grade = 20
second_exam.writing_grade = 30
print(first_exam.__dict__)
print(second_exam.__dict__)
print(first_exam.writing_grade)
print(second_exam.writing_grade)
```

```css
{'name': 'first_exam'}
{'name': 'second_exam'}
{'name': 'first_exam', '_writing_grade': 10, '_math_grade': 20}
{'name': 'second_exam', '_writing_grade': 30}
writing_grade first_exam Exam
10
writing_grade second_exam Exam
30
```

现在我们就可以不用字典来保存值了。

### 使用元类注解类的属性

看下面代码：

```python
class Exam(object):
    math_grade = Grade('math_grade')
    writing_grade = Grade('writing_grade')
    english_grade = Grade('english_grade')
    chinese_grade = Grade('chinese_grade')
    
    a_grade = Grade('a_grade')
    b_grade = Grade('b_grade')
    ......
```

如果我们存在 N 个 Grade，每次都在右边传个对应的 name，岂不是很难看很麻烦。

我们可以用元类来改写，元类是类的钩子，可以在定义类之后，对类进行改造：

> 如果你不懂元类，可以参考 [[Python] 深入理解元类并区分元类中的init、call、new方法](https://blog.csdn.net/spade_/article/details/113485937)

```python
class Grade(object):
    def __init__(self):     # 不再需要 name 参数
        self.name = None                # 初始为 None
        self.internal_name = None       # 初始为 None

    def __get__(self, instance, owner):
        print(self.name, instance.name, owner.name)
        if instance is None:
            return self
        return getattr(instance, self.internal_name, '')  # 最后一个 '' 是指获取不到实例名为 internal_name 的值时，返回空字符串

    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)


class Meta(type):
    def __init__(cls, name, bases, class_dict):
        super().__init__(name, bases, class_dict)
        # print(class_dict)     # 输出 class_dict
        for key, value in class_dict.items():
            if isinstance(value, Grade):    # 如果 value 是 Grade 的实例对象
                value.name = key   # value.name 相当于 math_grade.name/writing_grade.name
                value.internal_name = '_' + key


class Exam(object, metaclass=Meta):
    name = 'Exam'
    math_grade = Grade()
    writing_grade = Grade()

    def __init__(self, name):
        self.name = name


first_exam = Exam('first_exam')
second_exam = Exam('second_exam')
print(first_exam.__dict__)
print(second_exam.__dict__)
first_exam.writing_grade = 10
first_exam.math_grade = 20
second_exam.writing_grade = 30
print(first_exam.__dict__)
print(second_exam.__dict__)
print(first_exam.writing_grade)
print(second_exam.writing_grade)
```

```css
{'name': 'first_exam'}
{'name': 'second_exam'}
{'name': 'first_exam', '_writing_grade': 10, '_math_grade': 20}
{'name': 'second_exam', '_writing_grade': 30}
writing_grade first_exam Exam
10
writing_grade second_exam Exam
30
```

### 用描述符和元类仿照 Django 实现 ORM 模型

```python
class Field(object):
    def __init__(self, read_only=False):
        self.field_name = None
        self.read_only = read_only

    def __set__(self, instance, value):
        setattr(instance, self.field_name, value)

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.field_name, '')


class CharField(Field):
    def __init__(self, max_length=10, **kwargs):
        super().__init__(**kwargs)
        # max_length 必须为大于0的数
        if max_length is None or max_length < 0:
            raise ValueError('max_length must be a positive number')
        self.max_length = max_length

    def __set__(self, instance, value):
        # 1. read_only 只允许第一次赋值，不允许之后第二次赋值
        if self.read_only and \
                getattr(instance, self.field_name, ''):
            raise RuntimeError('read_only can not be modify')
        # 2. len(value) 不能大于 max_length
        if len(value) > self.max_length:
            raise ValueError("value's len must small than mat_length")
        super().__set__(instance, value)    # 调用父类


class IntegerField(Field):
    def __set__(self, instance, value):
        # value 必须为 int 类型
        if not isinstance(value, int):
            raise ValueError('IntegerField value must be int')
        super().__set__(instance, value)    # 调用父类


class Meta(type):
    def __new__(mcs, name, bases, class_dict):
        for key, value in class_dict.items():
            if isinstance(value, Field):
                value.field_name = '_' + key
        return super().__new__(mcs, name, bases, class_dict)


class Model(object, metaclass=Meta):
    def __init__(self, **kwargs):
        super().__init__()
        for k, v in kwargs.items():
            setattr(self, k, v)


class User(Model):
    name = CharField()
    age = IntegerField()
    sex = CharField(max_length=2)
    number = CharField(read_only=True)      # 只读的number，仅第一次可以写


if __name__ == "__main__":
    user1 = User(name="XiaoMing", age=15, sex="男", number='201010')
    user2 = User(name="XiaoHong", age=26, sex="女")
    print(user1.name, user1.age, user1.sex)
    print(user2.name, user2.age, user2.sex)
    user2.number = '101010'       # 第一次赋值
    # user1.number = '202020'     # 已经初始化过了，第二次赋值报错
    print(user1.__dict__)
    print(user2.__dict__)
    # user2.sex = '我是女'       # 报错
```

```css
140
150
{'_math_grade': 50, '_writing_grade': 140}
{'_writing_grade': 150, '_math_grade': 60}
```
