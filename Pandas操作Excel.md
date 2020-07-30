## Python 操作 Excel

Python 操作 Excel 可以通过两个方式，一种是使用 `openpyxl` 模块，另一种是使用 `Pandas` 模块。

### 1. Pandas DataFrame


```python
# -*- coding:utf-8 -*-
import os
import pandas as pd
import numpy as np

DIR_PATH = 'C:/Users/swx944363/Desktop/每日总结/2020-07-14/'
SHAPAN_PATH = os.path.join(DIR_PATH, 'PaaS沙盘(1).xlsx')
GOCENTER_PATH = os.path.join(DIR_PATH, '中心仓go信息(2020-07-09).csv')
OPENSOURCE_PATH = os.path.join(DIR_PATH, 'opensource_all_20200622204325.xls')
OUTPUT_PATH = os.path.join(DIR_PATH, '输出.xlsx')

if __name__ == '__main__':
    shapan_excel = pd.read_excel(SHAPAN_PATH, sheet_name='FusionStage+POM')
    gocenter_excel = pd.read_csv(GOCENTER_PATH, sep=',', encoding='ANSI')
    opensource_excel = pd.read_excel(OPENSOURCE_PATH, sheet_name='st')
    output_excel = pd.read_excel(OUTPUT_PATH, sheet_name='Sheet1')

    # 解决 Pandas 输出省略的问题
    pd.set_option('display.max_columns', 1000)
    pd.set_option('display.width', 1000)
    pd.set_option('display.max_colwidth', 1000)

    # print(shapan_excel.head())
    # print(gocenter_excel.head())
    # print(opensource_excel.head())
    # print(output_excel.head())
    # print(type(shapan_excel), type(gocenter_excel), type(opensource_excel), type(output_excel))

    # 获取 沙盘 的所有软件信息
    shapan_soft_name_df = shapan_excel.iloc[1:, 3]  # 获取 沙盘 的 "软件名称" 列
    # print(shapan_soft_df, type(shapan_soft_df))
    shapan_soft_name_list = list(shapan_soft_name_df)
    print(shapan_soft_name_df.shape, shapan_soft_name_list)

    shapan_soft_version_df = shapan_excel.iloc[1:, 4]  # 获取 沙盘 的 "版本号" 列
    shapan_soft_version_list = list(shapan_soft_version_df)
    print(shapan_soft_version_df.shape, shapan_soft_version_list)


    # 获取 中心仓 的所有软件信息
    gocenter_soft_name_df = gocenter_excel.iloc[:, 4]  # 获取 中心仓 的 "软件名称" 列
    gocenter_soft_name_list = list(gocenter_soft_name_df)
    print(gocenter_soft_name_df.shape, gocenter_soft_name_list)

    gocenter_soft_version_df = gocenter_excel.iloc[:, 5]  # 获取 中心仓 的 "版本号" 列
    gocenter_soft_version_list = list(gocenter_soft_version_df)
    print(gocenter_soft_version_df.shape, gocenter_soft_version_list)

    gocenter_soft_url_df = gocenter_excel.iloc[:, 7]  # 获取 中心仓 的 "group_id" 列
    gocenter_soft_url_list = list(gocenter_soft_url_df)
    print(gocenter_soft_url_df.shape, gocenter_soft_url_list)


    # 获取 opensource 的所有软件信息
    opensource_soft_df = opensource_excel.iloc[:, [0, 2, 4]]
    opensource_soft_name_list = list(opensource_soft_df.iloc[:, 1])  # 获取 opensource 的 "软件名称" 列
    opensource_soft_version_list = list(opensource_soft_df.iloc[:, 2])  # 获取 opensource 的 "版本号" 列
    opensource_soft_url_list = list(opensource_soft_df.iloc[:, 0])  # 获取 opensource 的 "软件URL" 列
    print(len(opensource_soft_name_list), opensource_soft_name_list)
    print(len(opensource_soft_version_list), opensource_soft_version_list)
    print(len(opensource_soft_url_list), opensource_soft_url_list)


    # 0. 取三个表的基本信息
    shapan_soft_df = shapan_excel.iloc[1:, 2:6]              # 软件编码 软件名称 版本号 license
    gocenter_soft_df = gocenter_excel.iloc[:, [0, 4, 5, 7]]        # 软件编码 软件名称 版本号 group_id
    opensource_soft_df = opensource_excel.iloc[:, [0, 2, 3, 4]]    # 软件名称 版本号 软件URL 软件编码
    # shapan_soft_df = shapan_soft_df.drop_duplicates()     # 去重
    # gocenter_soft_df = gocenter_soft_df.drop_duplicates()     # 去重

    print(shapan_soft_df.shape, len(shapan_soft_df["软件名称（必填）"].unique()))   # 查看软件名称不重复的项
    print(gocenter_soft_df.shape, len(gocenter_soft_df["软件名称"].unique()))
    print(opensource_soft_df.shape, len(opensource_soft_df["软件名称"].unique()))
    print(shapan_soft_df.head(10))
    print(gocenter_soft_df.head(5))
    print(opensource_soft_df.head(5))


    # 1. 合并 沙盘 和 中心仓
    one_merge = pd.merge(left=shapan_soft_df, right=gocenter_soft_df, how="left", left_on="软件名称（必填）", right_on="软件名称")
    one_merge = one_merge.drop(columns=["软件名称", "软件版本编码"])
    one_merge = one_merge[one_merge.apply(lambda x: x[2] == x[4] if x[4] is not np.NaN else True, axis=1)]
    one_merge = one_merge.drop_duplicates(["软件名称（必填）"])
    print(one_merge.shape)
    print(one_merge.head(40))
    print(one_merge.columns)

    # 2. 合并 三者
    two_merge = pd.merge(left=one_merge, right=opensource_soft_df, how="left", left_on="软件名称（必填）", right_on="软件名称")
    two_merge = two_merge.drop(columns=["软件名称", "软件编码"])
    print(two_merge.shape)
    print(two_merge.head(20))
    # print(two_merge["软件名称（必填）"].unique())
    print(two_merge["软件名称（必填）"].value_counts())
    # two_merge = two_merge.drop_duplicates(["软件名称（必填）"])


    # 3. 筛选过滤
    # 软件编码（必填）   软件名称（必填）   版本号（必填）  license（必填） 软件版本号    group_id     软件URL     版本
    #       0               1                  2               3            4           5           6           7
    # 1. 中心仓 或 opensource 找不到 沙箱的软件信息
    # 2. 沙箱 和 中心仓 版本都一致，但
    #   (1) 中心仓版本 和 opensource 版本不一致
    #   (2) 中心仓的URL路径 和 opensource 的URL路径不一致 且 路径不是 gitlab.huawei.com 开头
    f = lambda x: (x[4] is np.NaN or x[5] is np.NaN) or (x[2] == x[4] and x[4] == x[7] and x[5] != x[6])
    is_same = two_merge.apply(f, axis=1)         # 对比每一行的 软件 版本是否一致
    print(is_same)
    res = two_merge[is_same]
    print(res.head(20))
    print(res.shape)

    drop_dup = res.drop_duplicates(["软件名称（必填）"])    # 去重
    print(drop_dup.head(20))
    print(drop_dup.shape)


    # 4. 输出文件，csv 文件需保存为 ANSI 编码格式
    drop_dup.to_csv(os.path.join(DIR_PATH, 'output.csv'), encoding='ANSI')
```
### 2. openpyxl

```python
import openpyxl

# 1. 打开一个excel文档, class 'openpyxl.workbook.workbook.Workbook'实例化出来的对象
wb = openpyxl.load_workbook('C:/Users/swx944363/Desktop/每日总结/2020-07-14/输出.xlsx')

# 获取当前工作薄里所有的工作表， 和正在使用的表;
print(wb, type(wb))
print(wb.sheetnames)
print(wb.active)


# 2. 选择要操作的工作表， 返回工作表对象
sheet = wb['Sheet1']
# 获取工作表的名称
print(sheet.title)


# 3. 返回指定行指定列的单元格信息
print(sheet.cell(row=4, column=4).value)

cell1 = sheet['C4']     # 第 C 列 第 4 行
print(cell1)
print(cell1.row, cell1.column, cell1.value)


# 4. 获取工作表中行和列的最大值
print(sheet.max_column)
print(sheet.max_row)
sheet.title = '学生信息'
print(sheet.title)


# 5. 访问单元格的所有信息
print(sheet.rows)  # 返回一个生成器， 包含文件的每一行内容， 可以通过便利访问.
# 循环遍历每一行
for row in sheet.rows:
    # 循环遍历每一个单元格
    for cell in row:
        # 获取单元格的内容
        print(cell.value, end=',')
    print()

import openpyxl


def read_column(sheet_name, column):
    pass


if __name__ == '__main__':

    # 1. 打开一个excel文档, class 'openpyxl.workbook.workbook.Workbook'实例化出来的对象
    wb = openpyxl.load_workbook('C:/Users/swx944363/Desktop/每日总结/2020-07-14/PaaS沙盘(1).xlsx')

    sheet = wb['FusionStage+POM']
    cell_range = sheet['C4':'K13']
    # print(cell_range)

    # print(tuple(cell_range))
    #u
    # for row in sheet.iter_rows('C4:K13'):
    #     for cell in row:
    #         print(cell)

    col_shapan = [4, 5]     # 第四列为软件名称，第五列版本号，第三列软件编码


    # for i in range(1, 11):
    #     for j in range(1, 13):
    #         value = sheet.cell(row=i, column=j).value
    #         if value is not None:
    #             print(value, end="\t\t\t")
    #         else:
    #             print("", end="\t\t\t\t")
    #     print("")

    sheet.columns()

```

