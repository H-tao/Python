```python
from functools import wraps
RETRY_TIMES = 3


def do_retry(retry_times, info=None):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for retry in range(retry_times):
                _success_or_not = func(*args, **kwargs)
                if _success_or_not:  # 执行
                    print('success')
                else:
                    print('fail')
                    continue
                if _success_or_not or retry == retry_times:
                    return _success_or_not
        return wrapper
    return decorate


@do_retry(retry_times=RETRY_TIMES)
def open_modify_config(self):
    return self.click_element_until(Xpather.TEMPLATE_MODIFY)


def click_tool(self, tool_name):
    @do_retry(retry_times=RETRY_TIMES)
    def click():
        _ = self.click_element_until(Xpather.TEMPLATE_TOOL_NODE % tool_name, 2)
        time.sleep(1)
        return _
    return click()
    
```
