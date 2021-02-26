import re
from functools import wraps
from Log.logging import logger


def do_retry(retry_times, info=None):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if info is not None:
                logger.info(f'正在开始{info}...')
            for retry in range(1, retry_times+1):
                result = func(*args, **kwargs)
                if result:  # 执行
                    if info is not None:
                        logger.info(f'{info}成功!')
                    return result
                elif not result:
                    if info is not None:
                        logger.info(f'{info}失败!重试第{retry}次...')
                    if retry == retry_times:
                        return result
                    continue
        return wrapper
    return decorate


def read_file_by_line(file):
    with open(file, mode='r', encoding='utf8') as f:
        while True:
            one_line = f.readline().strip()
            if not one_line:
                return
            yield one_line


def read_file_by_line_skip(file, startwith='#'):
    with open(file, mode='r', encoding='utf8') as f:
        while True:
            one_line = f.readline().strip()
            while one_line.startswith(startwith):
                one_line = f.readline().strip()
            if not one_line:
                return
            yield one_line


def read_file_by_total(file):
    with open(file, mode='r', encoding='utf8') as f:
        return f.read()


# 统一大写转小写，"-" 转 "_"
def make_format(name):
    if name:
        return re.sub(r'-', r"_", name.lower())
    else:
        return name


if __name__ == '__main__':
    # lines = read_file_by_total("Jenkins/jobs.txt")
    # # for line in lines:
    # #     print(line)
    lines = read_file_by_line_skip('../TXT/MR流水线.txt', startwith='#')
    for index, line in enumerate(lines):
        print(index + 1, line)
    import os
    print(os.path.split(os.path.realpath(__file__))[0])
