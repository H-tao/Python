angular原生的项目需要跑在webstorm上。angular与Django前后端不分离时，需要将angular的代码集成待Django中，搜了搜，网上居然没有一篇相关的教程，全是简单讲了讲angularJS和Django的，也不全面，这就很离谱！！！
参考JAVA跟Angular前后端不分离的教程，趁着这次简单搞了一次Django集成Angular前端代码，写个简单的教程记录一下。

## 1. angular项目编译
不懂编译angular的前端小白，请自行百度。
angular项目编译之后，生成的dist文件夹目录结构大致如下：
```
- dist
  - index.html
  - x1.js
  - x2.js
  - ...
  ...  
```

## 2.将dist文件夹重命名为static移入Django项目
移入之后，Django项目的目录结构大致如下：
```
- Project
  - __init__.py
  - settings.py
  - urls.py
  - wsgi.py
- static
  - index.html
  - x1.js
  - x2.js
  - ...
  ...  
- templates
- user
  - migartions
    - ...
  - __init__.py
  - admin.py
  - apps.py
  - models.py
```
## 3. 修改项目的settings配置
为了直接使用angular编译出来的前端代码不做过多的修改，我们打开项目的settings.py文件，修改templates目录的配置，找到:
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [os.path.join(BASE_DIR, 'templates')]   
        'DIRS': [os.path.join(BASE_DIR, 'static')]    # 将templates修改为static，这样Django就会去static目录下找模板(.html)文件了
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
除了这样，我们还要修改静态文件的配置：
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
```
## 4. 修改index.html
```html
<base href="/static/">
```
