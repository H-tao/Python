"""
写一个装饰器函数：如果被装饰的函数有参数名为 'name'，这个参数由装饰器函数传入被装饰函数，否则不作处理。
"""

from functools import wraps


def get_func(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        func_args = func.__code__.co_varnames   # 获取被装饰函数的参数名
        # func_defaults = func. __defaults__    # 被装饰函数参数的默认值
        if 'name' in func_args:
            print(True)
            res = func('name', *args, **kwargs)   # 注意， kwargs 后面不能继续传递参数了
        else:
            print(False)
            res = func(*args, **kwargs)
        return res
    return decorator


@get_func
def func1(name, number=None, score='99'):
    print('Func1', name, number, score)


@get_func
def func2(number=None):
    print('Func2', number)


func1(2, '3')   # name 参数由 get_func帮我们传递了
func2(1)    #
