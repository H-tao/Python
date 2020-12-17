```
_ = re.sub(r'[\\/:*?"<>→]', '.', _)
```

```python
import pandas as pd
import os
import re

if __name__ == '__main__':
    # 读取8,9,18列
    df = pd.read_excel(io='demo.xlsx', header=0, sheet_name="Sheet1", usecols=[7, 8, 17])
    # 筛选出责任部门为PaaS的
    df = df[df['责任部门'].isin(['PaaS'])]
    # 遍历行
    for index, row_series in df.iterrows():
        # 替换Windows文件夹名不能存在的字符为 "."
        software_name = re.sub(r'[\\/:*?"<>→]', '.', row_series['software name'])
        version = re.sub(r'[\\/:*?"<>→]', '.', row_series['Version'])
        # 连接 software name 和 Version
        dir_name = '@'.join([software_name, version])
        print(dir_name)
        # 递归创建文件夹
        os.makedirs(f'paas/{dir_name}')

```
