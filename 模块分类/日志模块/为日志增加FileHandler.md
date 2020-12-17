```python
formatter = logging.Formatter('[%(asctime)s][%(filename)s, %(lineno)s] %(message)s', datefmt='%m-%d %H:%M:%S')

def set_logfile(logger, logfile):
    # 日志文件输出
    file_out = logging.FileHandler(logfile, encoding='utf-8')
    file_out.setFormatter(formatter)
    logger.addHandler(file_out)    # 添加文件输出
    logger.setLevel(logging.DEBUG)
```
