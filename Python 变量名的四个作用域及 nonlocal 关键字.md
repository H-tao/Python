## Python 变量名的四个作用域及 nonlocal 关键字

### 变量访问顺序

Python访问一个变量时，其查找顺序遵循变量解析机制LEGB法则，依次搜索：局部作用域、嵌套作用域、全局作用域、以及内置作用域。

- L：local，局部作用域，即函数中定义的变量；
- E：enclosing，嵌套的父级函数的局部作用域，即包含此函数的上级函数的局部作用域，但不是全局的；
- G：global，全局变量，就是模块级别定义的变量；
- B：built-in，系统固定模块里面的变量，比如int, bytearray等。 搜索变量的优先级顺序依次是：作用域局部>外层作用域>当前模块中的全局>python内置作用域，也就是LEGB。

### 局部作用域：

```python
def fun():
    def inner():
        var = 'b'
        print(var)

    inner()
    print(var)	# 报错了，var 只在 inner 局部作用域内生效

fun()
```

### 嵌套作用域：

```python
var = 'a'
def fun():
    var = 'b'
    def inner():
        print(var)	# b，此时去嵌套作用域搜索到了 var

    inner()
    print(var)	# b

fun()
print(var)	# a
```

### 全局作用域

我们来看以下代码：

```python
var = 'a'

def fun():
    def inner():
        var = 'c'
        print(var)	# c  搜索局部作用域
        
    inner()
    print(var)	# a  即便你没有定义 var，Python还是找到了它，因为去搜索了全局作用域
    
fun()
print(var)	# a
```

如果我们试图修改全局的 var 会怎么样呢？

```python
var = 'a'

def fun():
    var = 'b'	# 这样相当于定义了一个新的变量，不会去搜索全局作用域

    def inner():
        var = 'c'
        print(var)	# c

    inner()
    print(var)	# b	

fun()
print(var)	# a，没有修改成功
```

如果你要修改全局变量，你需要加上`global`关键字：

```python
var = 'a'

def fun():
    global var	# 使用 global
    var = 'b'

    def inner():
        var = 'c'
        print(var)	# c

    inner()
    print(var)	# b

fun()
print(var)	# b 全局变量被修改了
```

### 内置作用域

Python 内置的模块 `__builtin__`，我们平时使用的内置函数就来自于它。

```python
print(abs)	# <built-in function abs>
print(max)	# <built-in function max>
```

### nonlocal 的使用

先看一段代码：

```python
def fun():
    var = 'b'	# 如果我想在 inner 里修改 var，怎么办呢？

    def inner():
        var = 'c'
        print(var)	# c	局部作用域

    inner()
    print(var)	# b 没变化

fun()
```

这样不行啊，如果使用 global 呢？

```python
def fun():
    var = 'b'

    def inner():
        global var
        var = 'c'
        print(var)	# c

    inner()
    print(var)	# b 没变化


fun()
```

还是不行，这就让人有些头疼了。不过别担心，使用 nonlocal 就好了啊。

```python
def fun():
    var = 'b'

    def inner():
        nonlocal var
        var = 'c'
        print(var)	# c

    inner()
    print(var)	# c 变了，它变了！

fun()
```





