### 文件IO
#### Excel

##### 1. pandas.read_excel

```python
pandas.read_excel(io,sheet_name=0,header=0,names=None,index_col=None,usecols=None,squeeze=False,dtype=None,engine=None,converters=None,true_values=None,false_values=None,skiprows=None,nrows=None,na_values=None,keep_default_na=True,verbose=False,parse_dates=False,date_parser=None,thousands=None,comment=None,skip_footer=0,skipfooter=0,convert_float=True,mangle_dupe_cols=True,**kwds)
```

**常用参数：**

- io：文件路径

  io = r'C:\Users\ss\Desktop\ppp.xlsx'

- sheetname：表名，

  sheetname = None		# 读取全部表，得到 OrderDict：key为表名，value为 DataFrame

  sheetname = 1 / "Sheet1"			# 读取单个表，返回 DataFrame

  sheetname = [0, 1] /  ["Sheet1", "Sheet2"]   	# 读取多表，返回一个OrderDict	

- header：指定列名行

- names：设置列名，必须是list类型，且长度和列数一致

  names = ["Name", "Number", "Score"]

- usecols：使用的行

  usecols = range(1, 3) 		# 使用 [1, 3) 行，不包括第 3 行

  usecols = [4, 7]			# 使用 4和7 行

- skiprows：指定跳过的行数（不读取的行数）

  shiprows = 4				# 跳过前 4 行，会把首行列名也跳过

  skiprows = [1, 2, 4]		# 跳过 1,2,4 行

  skiprows = range(1, 10)	# 跳过 [1,10) 行，不包括第10行，可以留下首行列名

- skipfooter：指定省略尾部的行数，必须为整数

  skipfooter = 4 			# 跳过尾部 4 行

- index_col：指定列为索引列，索引从 0 开始

  index_col = 1				

  index_col = "名称"		

```bash
# 读取多个表
import pandas as pd
order_dict = pd.read_excel(r'C:\Users\sss\Desktop\test.xlsx',header=0, usecols=[2, 3] names=["Name", "Number"], sheet_name=["Sheet1", "Sheet2"], skiprows=range(1, 10), skipfooter=4)
for sheet_name, df in order_dict.items():
    print(sheet_name)
    print(df)
```

##### 2. DataFrame.to_excel

```python
DataFrame.to_excel(excel_writer,sheet_name="Sheet1",na_rep="",float_format=None,columns=None,header=True,index=True,index_label=None,startrow=0,startcol=0,engine=None,merge_cells=True,encoding=None,inf_rep="inf",verbose=True,freeze_panes=None)
```

**常用参数：**

- excel_writer：文件路径，不存在会自动生成

- sheet_name="Sheet1"：指定写的表

- columns=None：指定输出某些列

  columns = ["Name", "Number"]	

- header=True：是否保存头行列名

- index=True：是否保存索引列

- startcol=0：起始行

- merge_cells=True：是否合并单元格

- encoding=None：指定编码，常用 utf-8

- float_format=None：浮点数保存的格式，默认保存为字符串

  float_format='%.2f'		# 保存为浮点数，保留2位小数

- engine=None：保存格式，指定`io.excel.xlsx.writer、` `io.excel.xls.writer`、`io.excel.xlsm.writer`.

```python
# 简单示例
df.to_excel(r'C:\Users\sss\Desktop\test.xlsx', columns=["Name", "Number"], encoding="utf8")
```

