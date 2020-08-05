class A():       #定义一个类 A
    a     = 100  #公有变量
    _b    = 200  #公有变量
    __c   = 300  #私有变量
    __d__ = 400  #公有变量

    @classmethod
    def printf(cls):
        print(cls.__c)

    def print_c(self):
        print(self.__c)
a = A()     #实例化一个对象a，当然可以取另外一个名字b
print(a.a,a._b,a.__d__)   #打印四个变量的值
a.__c = 1
a.printf()
a.print_c()
# print(A.__dict__)
# class A():       #定义一个类 A
#     a     = 100  #公有变量
#     _b    = 200  #公有变量
#     __c   = 300  #私有变量
#     __d__ = 400  #公有变量
#     def __init__(self,a,b,c,d):   #通过构造函数给公有变量或者私有变量重新赋值
#         print('构造前:',self.a,self._b,self.__c,self.__d__)
#         self.a = a
#         self._b = b
#         self.__c = c
#         self.__d__ = d
#         print('构造后:',self.a,self._b,self.__c,self.__d__)
#     def print_c(self):  #通过成员函数访问私有变量
#         return self.__c
# a = A(1000,2000,3000,4000)          #通过传值构造对象
