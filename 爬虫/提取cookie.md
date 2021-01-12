提取登录响应的Cookie

### 1. post请求登录之后的Cookie，通过`response.cookies`获取：

```python
response = requests.post(self.post_url, data=data, headers=self.headers)

cookies = response.cookies
cookies = requests.utils.dict_from_cookiejar(response.cookies)
self.headers['Cookie'] = '; '.join(['='.join([k, v]) for k, v in cookies.items()])

response = requests.get(self.visit_url, headers=self.headers, verify=False)
print(response.text)
```

### 2. session 登录后的Cookie，通过`session.cookies`获取：

```python
_cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
_cookie = '; '.join(['='.join([k, v]) for k, v in _cookies.items()])
```

如果页面有登录跳转，需要访问跳转之后的页面以获取cookie：

```python
def __get(self, _url):
    response = self.session.get(_url, headers=self.headers, verify=False)
    if response.status_code == 200:
        res = json.loads(response.text)
        return res
    else:
        return None

def get_xxx_cookie(self):
    _url = 'https://xxx.com/passthrough/api/v1/codecheck-info'  # 首页url
    self.__get(_url)
    _cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
    _cookie = '; '.join(['='.join([k, v]) for k, v in _cookies.items()])
    return _cookie
```

