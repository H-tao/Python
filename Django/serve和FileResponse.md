### 在settings.py内配置
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
```

### 在urls.py内配置
```python
from django.urls import path, re_path
from . import views
from django.conf.urls import url
from django.views.static import serve
from MyProject.settings import STATICFILES_DIRS

urlpatterns = [
    ...
    url(r'^(?P<path>.*)$', serve, {'document_root': STATICFILES_DIRS[0]}),
    ...
]
```
