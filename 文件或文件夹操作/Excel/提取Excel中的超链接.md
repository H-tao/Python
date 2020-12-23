第2-40行，第2列的内容如下：
```css
=HYPERLINK("https://www.github.com/xxxxx/32","#32")
=HYPERLINK("https://www.github.com/xxxxxx/452","#452")
=HYPERLINK("https://www.github.com/xxxxxxx/761","#761")
=HYPERLINK("https://www.github.com/xxxxxxxx/318","#318")
=HYPERLINK("https://www.github.com/xxxxxxxxx/316","#316")
=HYPERLINK("https://www.github.com/xxxxxxxxx/572","#572")
...
```
我想将url提取出来：
```css
https://www.github.com/xxxxx/32
https://www.github.com/xxxxxx/452
https://www.github.com/xxxxxxx/761
https://www.github.com/xxxxxxxx/318
https://www.github.com/xxxxxxxxx/316
https://www.github.com/xxxxxxxxx/572
```
使用openpyxl：
```javascript
import openpyxl
import re

PATH = 'aa.xlsx'
column = range(2, 3)    # 第 [2, 3)列，不包括第3列
rows = range(2, 44)     # 第 [2, 44)行，不包括第44行
wb = openpyxl.load_workbook(PATH)
sheet = wb["Sheet1"]

for c in column:
    for r in rows:
        # print(sheet.cell(r, c).value)
        print(re.findall(r'=HYPERLINK\("(.*?)"', str(sheet.cell(r, c).value))[0])
        # print(sheet.cell(r, c).hyperlink)
```
