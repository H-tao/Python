> Requests 是用Python语言编写，基于 urllib，采用 Apache2 Licensed 开源协议的 HTTP 库。它比 urllib 更加方便，可以节约我们大量的工作，完全满足 HTTP 测试需求。Requests 的哲学是以 PEP 20 的习语为中心开发的，所以它比 urllib 更加 Pythoner。

```python
import requests
requests.get(..., stream=False)
```

- 当把get函数的stream参数设置成False时，它会立即开始下载文件并放到内存中，如果文件过大，有可能导致内存不足。
- 当把get函数的stream参数设置成True时，它不会立即开始下载，当你使用iter_content或iter_lines遍历内容或访问内容属性时才开始下载。需要注意一点：文件没有下载之前，它也需要保持连接。

iter_content：一块一块的遍历要下载的内容

iter_lines：一行一行的遍历要下载的内容

使用上面两个函数下载大文件可以防止占用过多的内存，因为每次只下载小部分数据。

### 分块下载保存：

```python
def download_source(url, output_path, chunk_size=512):
    response = requests.get(url=url, stream=True)
    with open(output_path, mode='wb') as f:
        for chunk in response.iter_content(chunk_size):
            f.write(chunk)
            
download_source('www.xxxx.com/aaa/temp.xlsx', 'temp.xlsx')
download_source('www.xxxx.com/aaa/temp.csv', 'temp.csv')
download_source('www.xxxx.com/aaa/temp.zip', 'temp.zip')
```

以上就是基本的使用。分为get()和保存数据流两个部分。

我们get的时候，需要传入其他的get参数，比如请求头等，所以可以使用自己的get方法。

保存数据也分为流保存和一次保存等。所以可以这样做：

### 两种get方法：

requests.get()

```python
def get(url, stream=False)
	headers = {'User-Agent': 'xxx', 'Cookie': 'xxx'}
    response = requests.get(url=url, headers=headers, stream=stream)
    return response
```
session.get()
```python
def get(url, stream=False)
    session = session = requests.Session()
    response = session.get(url=url, stream=True)
    return response
```

### 保存数据的方法：

一次下载保存：

```python
def download_source(url, output_path):
    response = get(url, stream=False)
    with open(output_path, mode='wb') as f:
        f.write(response.content)
```
分块下载保存：
```python
def download_source(url, output_path, chunk_size=512):
    response = get(url, stream=True)
    with open(output_path, mode='wb') as f:
        for chunk in response.iter_content(chunk_size):
            f.write(chunk)
```

此处做了简单的延伸，其他方法自行延伸即可。
