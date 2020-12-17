 [Python3操作YAML文件](https://www.cnblogs.com/superhin/p/11503756.html)

## 安装处理yaml的模块

```
pip install pyyaml
```

- `yaml.load(stream)` / `yaml.safe_load(stream)`：将输入stream对象加载为字典类型。

  **推荐使用**`yaml.safe_load()`，将加载对象限制为简单的Python对象，如整数或列表 。

  `yaml.load()` 能通过加载yaml文件构建任何类型的python对象，若加载的yaml文件来源不可信，则可能产生注入攻击的风险。 

- `yaml.dump(data)` / `yaml.safe_dump(data)`：将data转为YAML类型。同样，推荐使用 `yaml.safe_dump(data)`

## 一、yaml 转 Python数据类型

假如有一个yaml文件，结构如下：

```yaml
name: 小明
number: 20200235
class: 2020-B

score:
  - English: 88
    Math: 90
family:
  - father:
      - name: 小刚
      - phone: 188
  - mother:
      - name: 小红
      - phone:
```

使用方式：

```python
import yaml

def parse_key(yaml_path):
    with open(yaml_path, mode='r', encoding='utf-8') as f:
        return yaml.safe_load(f)

if __name__ == '__main__':
    print(parse_key('xiaoming_info.yaml'))
```

### yaml 转 字典

```yaml
father:
  - name: 小刚
  - phone: 188
mother:
  - name: 小红
  - phone:
```

```python
{'father': [{'name': '小刚'}, {'phone': 188}], 'mother': [{'name': '小红'}, {'phone': None}]}
```

### yaml 转 列表

```yaml
- name: 小刚
- phone: 188
```

```python
[{'name': '小刚'}, {'phone': 188}]
```

### yaml 转 结构等

```yaml
- father:
    - name: 小刚
    - phone: 188
- mother:
    - name: 小红
    - phone:
```

```python
[{'father': [{'name': '小刚'}, {'phone': 188}]}, {'mother': [{'name': '小红'}, {'phone': None}]}]
```

### 处理yaml中的中文

#### 1. 文件输入

打开文件时指定`encoding='utf-8'` ：

```python
def parse_key(yaml_path):
    with open(yaml_path, mode='r', encoding='utf-8') as f:
        return yaml.safe_load(f)
```

#### 2. 字符串输入

无需指定，

```python
info = \
"""
name: 小明
number: 20200235
class: 2020-B
"""

print(yaml.safe_load(info))
# print(yaml.safe_load(info.encode('utf-8')))
```

## 二、Python 数据类型转yaml

```python
info = {'name': '小明', 'number': 20200235, 'class': '2020-B'}
print(yaml.dump(info))
print(yaml.dump(info, allow_unicode=True))
print(yaml.safe_dump(info, allow_unicode=True))
print(yaml.safe_dump(info, allow_unicode=True, encoding='utf-8',allow_unicode=True))

# a是追加写入，w是覆盖写入
with open('student_info.yaml', 'a', encoding='utf-8') as f:
    # stream可以是文件流
    yaml.dump(info, stream=f, allow_unicode=True, encoding='utf-8')
```

```yaml
class: 2020-B
name: "\u5C0F\u660E"
number: 20200235

class: 2020-B
name: 小明
number: 20200235

class: 2020-B
name: 小明
number: 20200235
```
## 三、yaml分段---

在一个yaml文件中，可以使用---来分段（3个横线），这样可以将多个文档写入一个文件中：

```yaml
father:
  - name: 小刚
  - phone: 188
---
mother:
  - name: 小红
  - phone:
```

safe_load_all()方法，load_all方法会生产一个迭代器，可以用for循环输出： 

```python
import yaml

def parse_key(yaml_path):
    with open(yaml_path, mode='r', encoding='utf-8') as f:
        for g in yaml.safe_load_all(f):
            print(g)

if __name__ == '__main__':
    parse_key('xx.yaml')
```

```
{'father': [{'name': '小刚'}, {'phone': 188}]}
{'mother': [{'name': '小红'}, {'phone': None}]}
```

同样也可以将多个字典类型转为yaml：

```python
info1 = {'father': [{'name': '小刚'}, {'phone': 188}]}
info2 = {'mother': [{'name': '小红'}, {'phone': None}]}

print(yaml.safe_dump_all([info1, info2], allow_unicode=True))

with open('student_info.yaml', 'w', encoding='utf-8') as f:
    yaml.safe_dump_all([info1, info2], stream=f, allow_unicode=True)
```

```
father:
- name: 小刚
- phone: 188
---
mother:
- name: 小红
- phone: null
```

