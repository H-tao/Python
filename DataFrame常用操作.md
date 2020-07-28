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

##### 
