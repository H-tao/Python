### super()和super(class_name,  self)的选择

今天有人问我 super() 和 super(class_name,  self) 有什么区别。总结来说，Python3新式类推荐使用super()。

```python
"""
关于super():
        super() -> same as super(__class__, <first argument>)
        super(type) -> unbound super object
        super(type, obj) -> bound super object; requires isinstance(obj, type)
        super(type, type2) -> bound super object; requires issubclass(type2, type)
        Typical use to call a cooperative superclass method:
        class C(B):
            def meth(self, arg):
                super().meth(arg)
        This works for class methods too:
        class C(B):
            @classmethod
            def cmeth(cls, arg):
                super().cmeth(arg)

        # (copied from class doc)
"""

class Grand:
    @classmethod
    def say(cls):
        print('Grand')


class Parent(Grand):
    @classmethod
    def say(cls):
        print('Parent')

class Child(Parent):
    @classmethod
    def say(cls):
        print('Child')
        # 以下三者都相当于 super(Child, Child).say()
        super().say()                   # Parent
        super(Child, cls).say()         # Parent
        super(__class__, cls).say()     # Parent

        super(Parent, cls).say()        # Grand，调用Parent的父类
        # super(Grand, cls).say()         # AttributeError!!!
        # super(object, cls).say()        # AttributeError!!!


super(Child, Child).say()       # Parent
super(Parent, Child).say()      # Grand
super(Parent, Parent).say()     # Grand
# super(Child, Parent).say()     # TypeError!!!

Child().say()
```
