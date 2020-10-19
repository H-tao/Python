```python
import os, openpyxl

class ExcelHandler:
    def __init__(self, excel_path):
        self.excel_path = excel_path
        self.wb = openpyxl.load_workbook(excel_path)

    def save_hyperlink(self, sheet_name, column, row, url):
        print(sheet_name, column, row, url)
        try:
            sheet = self.wb[sheet_name]
            try:
                sheet.cell(row=row, column=column).hyperlink = url
            except ValueError:
                print("存储失败，请检查数据项对应的表格行列是否正确")
        except KeyError:
            print("未在表格内找到对应的存储Sheet，请检查表格")

    def save_to_cell(self, sheet_name, column, row, value):
        print(sheet_name, column, row, value)
        try:
            sheet = self.wb[sheet_name]
            try:
                sheet.cell(row=row, column=column, value=value)
            except ValueError:
                print("存储失败，请检查数据项对应的表格行列是否正确")
        except KeyError:
            print("未在表格内找到对应的存储Sheet，请检查表格")

    def save_to_excel(self, output_path):
        try:
            self.wb.save(output_path)
        except PermissionError as error:
            print(error)
            print("======== [权限错误，存储失败，请检测是否关闭文件!!!] =========")
        except OSError as error:
            print(error)
            print("======== [存储失败，请检查文件格式!!!] =========")
        else:
            print("======== [所有数据存储至EXCEL表格已完成] =========")
            print(os.path.abspath(output_path))
            
```

```python

if __name__ == '__main__':
    in_file = 'input/xxx表.xlsx'
    ex = ExcelHandler(in_file)
    ex.save_to_cell('Sheet1', 2, 5, '百度一下')
    ex.save_hyperlink('Sheet1', 2, 5, 'http://www.baidu.com')
```



