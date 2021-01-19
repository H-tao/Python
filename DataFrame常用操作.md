##### Series用法

https://blog.csdn.net/cymy001/article/details/78268721

##### 解决 Pandas 输出省略的问题

```python
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)
```
##### 设置某一列为索引列，加快查找

```python
df.index = df["Name"]				# 设置列为索引
df = df.drop(columns = "Name")		# 删除列
```

##### 读取某一列并转 list

```python
name_list = list(df["Name"])		# 按名称取"Name"列
or	
name_list = list(df.iloc[:, 2])		# 按索引取
```

##### 新增一列

```python
pipeline_df["名称"] = name_list		# name_list 的长度必须和 df 的列长度一致
pipeline_df["FormatName"] = [make_format(x) for x in pipeline_df["名称"]]
pipeline_df["语言"] = ["Python"] * len(name_list)

# 统一大写转小写，"-" 转 "_"
def make_format(name):
    if name:
        return re.sub(r'-', r"_", name.lower())
    else:
        return name
```

##### 按多列排序

```python
# 根据"Name"列降序，"Name"相同的，根据"Score"升序，返回一个新 DataFrame
new_df = pipeline_df.sort_values(by=["Name", "Score"], ascending=[False, True])
```

##### 获取特定值的单元格

```python
# 使用示例：获取 "XiaoMing" 的 "Score"
pipeline_df.index = pipeline_df["Name"]		# 将"Name"列设置为索引
pipeline_df = pipeline_df.drop(columns="Name")	# 删除"Name"列
print(pipeline_df.loc["XiaoMing", :]["Score"])
```

##### 修改特定值单元格的值

```python
# 修改df "Name" 值为 "Python" 的行 的 "Score" 为 56
change_name(df, "Name", "Python", "Score", 56)

def change_name(df, column_name, column_value, change_column_name, new_value):
    index = np.where(df[column_name] == column_value)[0]
    if index.size > 0:
        df.at[index[0], change_column_name] = new_value      
```

##### 获取某个单元格的行或列的位置序号

```python
column = get_cols(sheet_name=sheet_name, project_name=project_name)
row = get_rows(sheet_name=sheet_name, project_name=project_name)

def get_cols(sheet_name, project_name):
    """
    获取表格第一列的某个单元格的列位置序号
    :param sheet_name: EXCEL的 Sheet
    :param project_name: 工程名
    :return: 成功返回列号，否则返回-1
    """
    df = pd.read_excel(FINAL_OUTPUT_EXCEL_PATH, sheet_name=sheet_name)
    # 建立序号列，索引为第 1 行的值
    cols = pd.DataFrame(data=np.arange(1, len(df.columns) + 1), index=df.iloc[0, :].values)
    try:
        col = cols.at[project_name, 0]
        return col
    except KeyError:
        return -1
    
def get_rows(sheet_name, project_name):
    """
    获取表格第一行的某个单元格的行位置序号
    """
    df = pd.read_excel(FINAL_OUTPUT_EXCEL_PATH, sheet_name=sheet_name)
    # 建立序号列，索引为第 1 行的值
    rows = pd.DataFrame(data=np.arange(1, len(df.columns) + 1), index=df.iloc[:, 0].values)
    try:
        rpw = rows.at[project_name, 0]
        return row
    except KeyError:
        return -1
```

##### 留下最新的一条数据（去重）

```python
# 根据 Date 列 降序排序，再根据 Module Point 列去重, subset 可以指定多列去重
df = df.sort_values(by="Date", ascending=False)
# Module 和 Point 列都相同的行会被删除，且保留的是相同的最后一条数据
df = df.drop_duplicates(subset=["Module"，"Point"], keep="last")
```

##### 遍历 DataFrame 的行列

```python
# 遍历列，column_name 为列名
for column_name, col_series in df.iteritems():
    print(column_name)
    print(col_series)
    one, two = col_series[col_series.index == 1], col_series[col_series.index == 2]	# 访问数据
    
# 遍历行，index 为行的索引（索引不一定是 0 - n 的序号）
for index, row_series in df.iterrows():
    print(index)
    print(row_series)
    name, score = row_series["Name"], row_series["Score"]	# 访问数据
```

##### 筛选特定值的所有行

```python
df = df[df["Name"].isin(["XiaoMing","XiaoHong"])]
```

##### 统计空值数

```python
# 计算data每一行有多少个缺失值的值，即按行统计缺失值
rows_null = df.isnull().sum(axis=1) 

# 下面则是按列统计缺失值
col_null = df.isnull().sum(axis=0)

#统计整个df的缺失值
all_null = df.isnull().sum().sum()

# 统计某一列的缺失值
idx_null = df['列名'].isnull().sum(axis=0)
```

##### 判断NaN

```python
import pandas
if pandas.np.isnan(x):
    print(True)

import numpy
if numpy.isnan(x):
    print(True)
    
import math
if math.isnan(x):
    print(True)
```

##### 合并两个表

```python
import pandas as pd

EXCEL_PATH = 'x1.xlsx'

ex1_ = pd.read_excel(EXCEL_PATH, sheet_name='Sheet2')
ex2_ = pd.read_excel(EXCEL_PATH, sheet_name='Sheet3')

one_merge = pd.merge(left=ex1_, right=ex2_, how="outer", on=['name', 'name'])
one_merge.drop_duplicates(['name'], inplace=True)
print(one_merge)
one_merge.to_excel('输出.xlsx', index=False)
```
