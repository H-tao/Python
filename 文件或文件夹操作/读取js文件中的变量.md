存在一个这样的js文件，我想把arr变量读取出来：
```javascript
<script type="text/javascript">
    # sss
    var arr=[
			{"num":"1001","name":"jack","age":16},
			{"num":"1002","name":"Mary","age":17},
			{"num":"1003","name":"Tom","age":19}
			];

    # sss
    var arr1 = [
			{"num":"1001","name":"jack","age":16},
			{"num":"1002","name":"Mary","age":17},
			{"num":"1003","name":"Tom","age":19}
			];

    # sss
    var arr2 = [
			{"num":"1001","name":"jack","age":16},
			{"num":"1002","name":"Mary","age":17},
			{"num":"1003","name":"Tom","age":19}
			];

    # sss
    var arr3 = [
			{"num":"1001","name":"jack","age":16},
			{"num":"1002","name":"Mary","age":17},
			{"num":"1003","name":"Tom","age":19}
			];
    arr.splice(1, 2,3,4,5);
    alert(arr);
</script>
```
```python
import json
import re


def read_param_of_js(file, param):
    with open(file, mode='r', encoding='utf-8') as f:
        data = f.read()
        res = re.findall(rf'var {param}[ ]*=[ ]*([\s\S]*?);', data)
        return res[0] if res else None


arr = read_param_of_js('test.js', 'arr')
print(json.loads(arr))
```
```css
[{'num': '1001', 'name': 'jack', 'age': 16}, {'num': '1002', 'name': 'Mary', 'age': 17}, {'num': '1003', 'name': 'Tom', 'age': 19}]
```
