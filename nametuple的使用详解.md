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
```
import csv
from collections import namedtuple

def read_file(file):
    with open(file, mode='r', encoding='utf8') as f:
        while True:
            one_line = f.readline().strip()
            if not one_line:
                return
            yield one_line


lines = read_file("student_info.csv")
csv_reader = csv.reader(lines)
header = next(csv_reader)[:4]
# llt = namedtuple("llt", header)
llt = namedtuple("Student", "Name Date English Math Chinese Money")
for index, row in enumerate(csv_reader):
    _ = llt._make(row[:4])
    print(row[:4])      # 输出前 4 列
    print(_.Name, _.Date, _.English, _.Math, _.Chinese, _.Chinese)
    if index == 5:      # 输出前 5 行
        break

# with open("student_info.csv", mode="r") as f:
#     lines = f.readlines()
#     csv_reader = csv.reader(lines)
#     print(csv_reader)
#     i = 0
#     for row in csv_reader:
#         print(row)
#         if i == 5:
#             break
#         i += 1

# Name,Date,English,Math,Chinese,Money,Other_1,Other_2,Other_3
# XiaoMing,2020-07-20T01:07:00Z,42,93,0.45,3077,5739,0.54,1
# XiaoHu,2020-07-20T01:07:31Z,320,852,0.38,18874,37143,0.51,1
# XiaoWang,2020-07-20T01:07:48Z,38,118,0.32,3581,34875,0.1,1
# XiaoYe,2020-07-20T01:12:48Z,312,477,0.65,3210,4935,0.65,1
# XiaoAn,2020-07-20T01:14:04Z,163,263,0.62,2152,4117,0.52,1
# XiaoChen,2020-07-20T01:17:30Z,8,10,0.8,423,777,0.54,0.98
# XiaoPeng,2020-07-20T01:17:44Z,5,9,0.56,1053,1398,0.75,1
# XiaoHong,2020-07-20T01:19:33Z,392,797,0.49,8969,15366,0.58,1
# XiaoNing,2020-07-20T01:20:59Z,24,41,0.59,1387,2677,0.52,1
# XiaoJing,2020-07-20T01:23:22Z,16,53,0.3,696,1378,0.51,1
# XiaoChong,2020-07-20T01:23:45Z,76,111,0.68,2127,2713,0.78,1
# XiaoMing,2020-07-20T01:24:01Z,52,135,0.39,3251,6695,0.49,0.99
```
