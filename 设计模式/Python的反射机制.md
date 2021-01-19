### hasattr

判断对象中是否有这个方法或变量。

```python
class Person(object):
    def __init__(self, name):
        self.name = name

    def talk(self):
        print(f'{self.name} is talking!')

p = Person("John")
print(hasattr(p, "talk"))  # True。因为存在talk方法
print(hasattr(p, "name"))  # True。因为存在name变量
print(hasattr(p, "abc"))  # False。因为不存在abc方法或变量
```

### getattr

获取对象中的方法或变量的内存地址。

```python
class Person(object):
    def __init__(self, name):
        self.name = name

    def talk(self):
        print(f'{self.name} is talking!')


p = Person("John")

n = getattr(p, "name")  # 获取name变量的内存地址
print(n)  # 此时打印的是:laowang

f = getattr(p, "talk")  # 获取talk方法的内存地址
f()  # 调用talk方法

# 我们发现getattr有三个参数，那么第三个参数是做什么用的呢?
s = getattr(p, "abc", "Not Found!")
print(s)  # 打印结果：not find。因为abc在对象p中找不到，本应该报错，属性找不到，但因为修改了找不到就输出not find
```
```css
John
John is talking!
Not Found!
```

### setattr

为对象添加变量或方法。

```python
def talk_func(self):
    print(f'{self.name} is talking!')

class Person(object):
    def __init__(self, name):
        self.name = name

p = Person("John")
setattr(p, "talk", talk_func)  # 将abc函数添加到对象中p中，并命名为talk
p.talk(p)  # 调用talk方法，因为这是额外添加的方法，需手动传入对象

setattr(p, "age", 30)  # 添加一个变量age,赋值为30
print(p.age)  # 打印结果:30
```

### delattr

删除对象中的变量，注意：**不能用于删除方法**。

```python
class Person(object):
    def __init__(self, name):
        self.name = name

    def talk(self):
        print(f'{self.name} is talking!')

p = Person("John")

delattr(p, "name")  # 删除name变量
print(p.name)  # 此时将报错
```

### 反射机制

#### common.py

```python
def home():
    print('home')

def login():
    print('login')

def logout():
    print('logout')
```

#### 普通方法

```python
import common

def main():
    _in = input('Please input url: ').strip()
    if _in == 'login':
        common.login()
    elif _in == 'logout':
        common.logout()
    elif _in == 'home':
        common.home()
    else:
        print('404')

if __name__ == '__main__':
    main()
```

#### 使用hasttr和getattr完成反射

```python
import common

def main():
    _in = input('Please input url: ').strip()
    if hasattr(common, _in):
        func = getattr(common, _in)
        func()
    else:
        print('404')

if __name__ == '__main__':
    main()
```

#### 动态导入模块

```python
def run():
    _in = input("请输入您想访问页面的url：  ").strip()
    modules, func = _in.split("/")
    obj = __import__(modules)
    if hasattr(obj, func):
        func = getattr(obj, func)
        func()
    else:
        print("404")


if __name__ == '__main__':
    run()
```

### 参考博客

https://www.cnblogs.com/kongk/p/8645202.html
