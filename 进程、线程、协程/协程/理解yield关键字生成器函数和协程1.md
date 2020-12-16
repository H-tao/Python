demo1()里面使用了yield，是一个生成器函数，返回一个生成器。我们可以使用next()方法来迭代生成器，每次迭代获取到的就是**yield产生的值，也就是yield右边的值**。
```python
# yield可以理解为暂停按钮，每次执行到yield，保存断点，同时yield还会返回值给调用方
def demo1(value=None):
    print('start')
    yield 1
    yield value
    yield 2
    print('end')

g = demo1("Value")
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

我们在上面讲到了`yield item`可以返回值给调用方，先讲一讲`data = yield item`

