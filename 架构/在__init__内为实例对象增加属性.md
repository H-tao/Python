在初始化函数`__init__()`内为实例对象增加属性：
```python
class SetAttrs:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        if not hasattr(self, 'school'):
            self.school = 'Number One School'

    def __str__(self):
        return str(self.__dict__)


class Student(SetAttrs):
    pass


sa = Student(name='Spade_', score=66, number='20201001')
print(sa)
```
```css
{'name': 'Spade_', 'score': 66, 'number': '20201001', 'school': 'Number One School'}
```
其实任何地方都可以为实例对象增加属性，比如这样，sa就多了一个xiaoming属性：
```python
sa.address = 'beijing'
print(sa)
```
```css
{'name': 'Spade_', 'score': 66, 'number': '20201001', 'school': 'Number One School', 'address': 'beijing'}
```
> 但是并不推荐这种做法，因为在这样增加的属性是不受控制的。换句话来说，你在这个地方为实例对象增加了属性，我在其他地方并不知道有这属性。
