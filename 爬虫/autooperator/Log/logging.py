"""
我们的目的是借助单例模式，只生成一个logger。
当日志文件已经存在时，默认以追加方式写入。
"""
import logging
import os
import time
import sys


class SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=SingletonType):
    def __new__(cls, log_file=None, file_output=True, standard_output=True):
        """
        1. Logger的__new__只在创建第一个实例的时候被调用。
        2. 我们要返回的不是Logger类实例，而是使用内置logging模块创建的实例。
        """
        # 日志文件的路径
        if log_file is None:
            # 文件的当前目录
            current_path = os.path.dirname(os.path.realpath(__file__))
            current_time = time.strftime("%Y-%m-%d-%H%M%S", time.localtime())
            log_file = os.path.join(current_path, 'log_output', f'{current_time}.txt')
            os.makedirs(os.path.dirname(log_file), exist_ok=True)

        cls.logger = logging.getLogger(__name__)
        formater = logging.Formatter('%(asctime)s  [%(filename)s %(lineno)s] : %(message)s')
        # 如果既不使用标准输出，也不使用日志文件输出，则选择标准输出
        if not file_output and not standard_output:
            standard_output = True
        if standard_output:
            # 标准输出
            standard_out = logging.StreamHandler(sys.stdout)
            standard_out.setFormatter(formater)
            cls.logger.addHandler(standard_out)    # 添加标准输出
        if file_output:
            # 日志文件输出
            file_out = logging.FileHandler(log_file, encoding='utf-8')
            file_out.setFormatter(formater)
            cls.logger.addHandler(file_out)    # 添加文件输出
            cls.logger.setLevel(logging.INFO)
        return cls.logger


logger = Logger(standard_output=True, file_output=True)

if __name__ == '__main__':
    # logger = Logger("Logger1")  # 只第一个名称有效
    # logger2 = Logger("Logger2")
    # logger3 = Logger("Logger3")
    # logger.info("This is a info")
    # print(logger is logger2, logger2 is logger3)
    print(not False and not False)
