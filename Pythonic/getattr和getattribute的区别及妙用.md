### Python的属性访问链



### getattr不抛出异常会导致的问题

访问未定义的属性时，如果`__getattr__()` 方法中不抛出`AttributeError` 异常或者显示返回一个值，则会返回None，此时可能影响到程序的实际运行预期。 比如 `__hasattr__()` 获取到的一直是 True： 

```python
class Student:
    def __init__(self, name):
        self.name = name

    def __getattr__(self, item):
        if item == 'score':
            return 99
        else:
            return None


john = Student('John')
print(john.score)	# 99

if hasattr(john, 'number'):     # 即便没有定义number，我们还是获取到了True
    print(True)		# True

print(john.number)	# None
```

### 无限递归示例

```python
class Demo:
    def __init__(self):
        self.my_dict = {}

    def __getattr__(self, item):
        print('__getattr__')
        return self.my_dict[item]	# .my_dict会继续调用 getattr 以获取 .my_dict

    def __setattr__(self, key, value):
        print('__setattr__')
        self.my_dict[key] = value

d = Demo()
d.name = 'John'
```

### super()和super(class_name,  self)的选择

今天有人问我 super() 和 super(class_name,  self) 有什么区别。总结来说，Python3新式类推荐使用super()。

```python
"""
关于super():
        super() -> same as super(__class__, <first argument>)
        super(type) -> unbound super object
        super(type, obj) -> bound super object; requires isinstance(obj, type)
        super(type, type2) -> bound super object; requires issubclass(type2, type)
        Typical use to call a cooperative superclass method:
        class C(B):
            def meth(self, arg):
                super().meth(arg)
        This works for class methods too:
        class C(B):
            @classmethod
            def cmeth(cls, arg):
                super().cmeth(arg)

        # (copied from class doc)
"""

class Grand:
    @classmethod
    def say(cls):
        print('Grand')


class Parent(Grand):
    @classmethod
    def say(cls):
        print('Parent')

class Child(Parent):
    @classmethod
    def say(cls):
        print('Child')
        # 以下三者都相当于 super(Child, Child).say()
        super().say()                   # Parent
        super(Child, cls).say()         # Parent
        super(__class__, cls).say()     # Parent

        super(Parent, cls).say()        # Grand，调用Parent的父类
        # super(Grand, cls).say()         # AttributeError!!!
        # super(object, cls).say()        # AttributeError!!!


super(Child, Child).say()       # Parent
super(Parent, Child).say()      # Grand
super(Parent, Parent).say()     # Grand
# super(Child, Parent).say()     # TypeError!!!

Child().say()
```

### getattr的妙用——动态访问 JSON 数据

JavaScript中支持以点号`.`访 JSON 数据，比如 `feed['Schedule']['events'][40]['name']` 可以使用 feed.Schedule.events[40].name 获取。使用 getattr 我们在 Python 中也可以这样动态访问 JSON 数据：

```python
class JsonDict(dict):
    """general json object that allows attributes to be bound to and also behaves like a dict"""

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(r"'JsonDict' object has no attribute '%s'" % attr)

    def __setattr__(self, attr, value):
        self[attr] = value

d = JsonDict()
d.name = 'John'
d['score'] = 99
print(d)
```

《流畅的Python》中作者实现了一个  FrozenJSON 类，可以递归自动处理嵌套的映射和列表。感兴趣的参考书的第19章。

### getattr的妙用——自动串接路径

```python
class _Url:
    def __init__(self, base_url):
        self._base_url = base_url

    def __getattr__(self, attr):
        if attr == 'get':		# 递归出口
            return self._base_url
        if attr == 'post':		# 递归出口
            return self._base_url
        _base_url = '%s/%s' % (self._base_url, attr)
        return _Url(_base_url)

url = _Url('www.csdn.com')
print(url.blog.user.info.get)
```

```python
www.csdn.com/blog/user/info
```

代码参考：https://github.com/michaelliao/sinaweibopy/blob/master/weibo.py#L307
