### 在settings.py内配置
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
```

### 在urls.py内配置
```python
from django.conf.urls import url
from django.views.static import serve
from MyProject.settings import STATICFILES_DIRS

urlpatterns = [
    ...
    url(r'^(?P<path>.*)$', serve, {'document_root': STATICFILES_DIRS[0]}),
    ...
]
```

### `^(?P<path>.*)`是如何调用视图函数的

在Python正则表达式中，命名正则表达式组的语法是`(?P<name>pattern)`，其中name是组的名称，pattern是一些要匹配的模式。 

#### 1. 指明组名称

命名正则表达式组：

```python
from django.urls import re_path

re_path(r'^student/(?P<name>.*)/(?P<number>\d{6})$', views.handle_student_info, name='student'),
```


通过路由`http://127.0.0.1/student/xiaoming/123456`发送请求，则会调用试图函数`handle_student_info(request, name='xiaoming', number='123456')`
```python
def handle_student_info(request, name, number):
    return HttpResponse(f'{name} {number}')
```
#### 2. 不指明组名称

命名正则表达式组：

```python
re_path(r'^student/(.*)/(\d{6})$', views.handle_student_info, name='student'),
```

通过路由`http://127.0.0.1/student/xiaoming/123456`发送请求，则同样会调用试图函数`handle_student_info(request, name='xiaoming', number='123456')`

### serve 视图函数的定义

通过`Ctrl+鼠标左键`，跳转到Django `serve`的定义，可以看到：

```python
def serve(request, path, document_root=None, show_indexes=False):
    ...
    response = FileResponse(fullpath.open('rb'), content_type=content_type)
    ...
    return response
```

`serve` 接收一个path和document_root参数，返回的是一个FileResponse，这就解释了我们访问静态文件为什么可以使用serve。

我们想要构造一个对应的路由，自然是可以使用指明组名称的正则表达式组`r'^(?P<path>.*)$'`

