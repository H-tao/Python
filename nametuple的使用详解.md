平时偶尔会看到namedtuple，但不知道这玩意儿到底有什么用，特此学习一下。

namedtuple 是一个类工厂，它接受一个类型名称和一个属性列表，并从中创建一个类。明晰类工厂这一点，即使用 namedtuple 创建的是一个类。namedtuple 结合了字典和元组的优点：

1. 访问性能优势，namedtuple 是基于元组的，通过索引访问元素非常快。
2. 存储性能优势，namedtuple 是不可变的，底层的数组存储被精确地分配所需的大小，内存效率胜过字典。
3. 生成的类可以被子类化，继承之后可以添加更多的操作。

所以：

1. 可读性重要的情况，可以优先使用属性访问。
2. 性能关键的情况，元素可以通过索引访问。

```python
from collections import namedtuple

# 定义一个Student类
Student = namedtuple('Student', 'name number score')

# Student是一个类，可以被继承
class NamedStudent(Student): pass

# 创建一个Student的nametuple对象
xm = Student(name='XiaoMing', number=1007, score='A')
xh = Student(**{'name': 'XiaoHong', 'number': 1008, 'score': 'B'})  # 通过字典 ** 解包方式创建
xg = Student._make(['XiaoGang', 1009, 'C'])     # 通过list创建

# 获取属性
print(xm)           # Student(name='XiaoMing', number=1007, score='A')
# 使用索引访问，元组的方式
print(xm[0], xh[1], xh[2])          # XiaoMing 1008 B
# 使用属性访问，字典的方式
print(xm.name, xg.number, xh.score)     # XiaoMing 1009 B

# 取代其中一个值，会返回一个新的Student实例，xg不变
new_xg = xg._replace(number=1010)
print(new_xg, new_xg is xg)    # Student(name='XiaoGang', number=1010, score='C') False

# 转为字典
d = xm._asdict()
print(d)    # OrderedDict([('name', 'XiaoMing'), ('number', 1007), ('score', 'A')])
```
所以说这玩意儿到底有什么用呢？

具名元组在存储[`csv`](https://docs.python.org/3.8/library/csv.html#module-csv)或者[`sqlite3`](https://docs.python.org/3.8/library/sqlite3.html#module-sqlite3)返回数据的时候特别有用

```
EmployeeRecord = namedtuple('EmployeeRecord', 'name, age, title, department, paygrade')

import csv
for emp in map(EmployeeRecord._make, csv.reader(open("employees.csv", "rb"))):
    print(emp.name, emp.title)

import sqlite3
conn = sqlite3.connect('/companydata')
cursor = conn.cursor()
cursor.execute('SELECT name, age, title, department, paygrade FROM employees')
for emp in map(EmployeeRecord._make, cursor.fetchall()):
    print(emp.name, emp.title)
    
https://www.cnblogs.com/linwenbin/p/11282492.html
```
