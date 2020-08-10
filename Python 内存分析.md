```python
class Fruit(object):
    total = 0

    def func1(self): pass

    @classmethod
    def class_func(cls): pass

    @staticmethod
    def static_func(): pass

class Apple(Fruit):
    def __init__(self):
        self.name = "Apple"

class Banana(Fruit):
    def __init__(self):
        self.name = "Banana"

class Cherry(Fruit):
    total = 'Cherry total'
    name = "Cherry Class Name"
    def __init__(self):
        self.name = "Cherry Instance Name"

f1, f2 = Fruit(), Fruit()
a1, a2 = Apple(), Apple()
b1, b2 = Banana(), Banana()
c1, c2 = Cherry(), Cherry()

print(Fruit.class_func, Apple.class_func, Banana.class_func.__str__())   # <bound method Fruit.class_func of <class '__main__.Fruit'>> <bound method Fruit.class_func of <class '__main__.Apple'>> <bound method Fruit.class_func of <class '__main__.Banana'>>
print(id(Fruit.class_func), id(Apple.class_func), id(Banana.class_func)) # 2723822850248 2723822850248 2723822850248
print(Fruit.class_func is Apple.class_func)           # False

print(Fruit.static_func, Apple.static_func, Banana.static_func)
print(Fruit.static_func is Apple.static_func, Banana.static_func)
print(Fruit.func1, Apple.func1, Banana.func1)
print(Fruit.func1 is Apple.func1, Banana.func1)

print(a1.class_func, a2.class_func)                   # <bound method Fruit.class_func of <class '__main__.Apple'>> <bound method Fruit.class_func of <class '__main__.Apple'>>
print(id(a1.class_func), id(a2.class_func))           # 2723822850248 2723822850248
print(a1.class_func is a2.class_func)                 # False

print(a1.func1, a2.func1, b1.func1, b2.func1)   # <bound method Fruit.func1 of <__main__.Apple object at 0x0000027A3FC962C8>> <bound method Fruit.func1 of <__main__.Apple object at 0x0000027A3FC96348>> <bound method Fruit.func1 of <__main__.Banana object at 0x0000027A3FC96308>> <bound method Fruit.func1 of <__main__.Banana object at 0x0000027A3FC963C8>>
print(a1.func1 is a2.func1)     # False

print(a1.static_func, a2.static_func, b1.static_func, b2.static_func)   # <function Fruit.static_func at 0x0000027A3FC659D8> <function Fruit.static_func at 0x0000027A3FC659D8> <function Fruit.static_func at 0x0000027A3FC659D8> <function Fruit.static_func at 0x0000027A3FC659D8>
print(a1.static_func is a2.static_func)     # True

print(Fruit.__dict__)   # {'__module__': '__main__', 'total': 100, 'class_func': <classmethod object at 0x0000027A3FC961C8>, 'set_total': <classmethod object at 0x0000027A3FC96248>, 'func1': <function Fruit.func1 at 0x0000027A3FC65948>, 'static_func': <staticmethod object at 0x0000027A3FC96288>, '__dict__': <attribute '__dict__' of 'Fruit' objects>, '__weakref__': <attribute '__weakref__' of 'Fruit' objects>, '__doc__': None}
print(Apple.__dict__)   # {'__module__': '__main__', '__doc__': None, 'total': 300}
print(Banana.__dict__)  # {'__module__': '__main__', '__doc__': None, 'total': 400}

# print(Fruit.__dict__["func"])   #

print(Cherry.__dict__)  # {'__module__': '__main__', 'total': 'Cherry total', 'name': 'Cherry', '__doc__': None}
```
