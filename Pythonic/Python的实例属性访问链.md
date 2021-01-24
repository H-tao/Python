### Python的实例属性访问链

1. `__getattribute__() ` ：访问属性必被调用。
2. `property.get()` ：当属性不在实例、基类和祖先类的`__dict__`中时，被调用。
3. `__getattr__` ：当属性不在实例、基类和祖先类的`__dict__`中、`__getattribute__() ` 或 `property.get()` 抛出异常时，被调用。

简单来说，访问链就是：`__getattribute__() ` -> `property.get()` -> `__getattr__`

```python
# 示例1.1
class Student:
    def __getattr__(self, item):
        print('__getattr__')
        if item == 'name':
            return 'John'

    def __getattribute__(self, item):
        print('__getattribute__')
        return super().__getattribute__(item)

john = Student()
print(john.name)
```

```css
__getattribute__
__getattr__
John
```

为了找到 name ，实例先访问了`__getattribute__()`，再访问 `__getattr__` 。

我们看看把 `__getattribute__`、`__getattr__` 和 `property` 结合起来会怎么样：

```python
# 示例1.2
class Student:
    @property
    def name(self):
        print('property.get')
        raise AttributeError	# 抛出异常

    def __getattr__(self, item):
        print('__getattr__')
        if item == 'name':
            return 'John'

    def __getattribute__(self, item):
        print('__getattribute__')
        # raise AttributeError      # 如果抛出异常会直接调用getattr，而不访问property
        return super().__getattribute__(item)

john = Student()
print(john.name)
```

```python
__getattribute__
property.get
__getattr__
John
```

### 在getattribute中捕获异常并手动调用getattr

前面在示例1.2中，其实访问`__getattribute__` 时，因为获取不到 name ，`super().__getattribute__(item)`自动抛出了 AttributeError，所以才访问了`__getattr__`  。现在我们尝试捕获异常并手动调用 getattr ：

```python
# 示例1.3
class Student:
    def __init__(self, name):
        self._name = name

    def __getattr__(self, item):
        print('__getattr__')
        if item == 'score':
            return 99
        if item == 'name':
            return self._name

    def __getattribute__(self, item):
        print('__getattribute__')
        print('item: ', item)
        # return super().__getattribute__(item)
        try:
            return super().__getattribute__(item)
        except AttributeError:      # 捕获AttributeError
            print('AttributeError')
            getattr(Student, item)      # 手动调用 getattr
            # return self.__getattr__(item)       # 这种相当于获取实例的 __getattr__ 再调用 __getattr___(item)
            # getattr(self, item)      # 错误的方式。这种方式相当于调用实例.属性(self.item)，而我们要获取的就是self.name，所以会导致无限递归

john = Student('John')
print(john.name)
```

```css
__getattribute__
item:  name
AttributeError
__getattr__
__getattribute__
item:  _name
John
```
