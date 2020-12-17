```python
from selenium import webdriver

EXECUTABLE_PATH = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
driver = webdriver.Chrome(executable_path=EXECUTABLE_PATH)
driver.get('http://www.baidu.com')

cookies = driver.get_cookies()
cookie = '; '.join(['='.join([c['name'], c['value']]) for c in cookies])
print(cookie)
```
