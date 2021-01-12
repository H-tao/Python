```python
"""
lambda 表达式的坑:参考CookBook 7.7 在匿名函数中绑定变量的值
lambda 表达式中用到的 x 是一个自由变量，在运行时才进行绑定而不是定义的时候绑定。
"""
funcs = [lambda x: x+n for n in range(5)]
for f in funcs:
    print(f(0))

funcs = [lambda x, n=n: x+n for n in range(5)]
for f in funcs:
    print(f(0))
```

```python
"""
为什么要使用闭包？
当编写代码中遇到需要附加额外的状态给函数时，可以使用闭包。
嵌套函数或者闭包：
简单来说，闭包就是一个函数，但是它还保存着额外的变量环境，使得这些变量可以在函数中使用。
闭包的核心特性就是它可以记住定义闭包时的环境，使得这些变量可以在函数中使用。
"""

class Add:
    def __init__(self):
        self.tmp = 1
    def add(self, x):
        return x + self.tmp

def func1(tmp):
    def func2(x):
        return x + tmp
    return func2

my_func = func1(1)
print(my_func(2))
```

```python
"""
闭包和format_map
"""
print('n={name}&&s={score}'.format_map({"name": "XiaoHong", "score": "WWWW"}))

def outer_func(x):
    def inter_func(**kwargs):
        return x.format_map(kwargs)
    return inter_func

func = outer_func('n={name}&&s={score}')
print(func(name="XiaoHong", score="WWWW"))
```
