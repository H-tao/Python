## 1. angular项目编译生成dist文件夹
angular项目编译之后，生成的dist文件夹目录结构如下：
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
