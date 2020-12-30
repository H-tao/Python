### 构建一个简单的本地Web服务器

这个服务器接收到请求后，对每一个请求先等待3秒，再返回一个 Hello world 和处理时间：

```
pip install flask
```

```javascript
from flask import Flask
import time
from datetime import datetime

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    time.sleep(3)
    return f'<h1>Hello World : {datetime.now()}<h1>'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
```

### 使用request下载

```javascript
import requests

async def request(url):
    response = requests.get(url)
    return response.text

async def spider(url):
    return await request(url)

if __name__ == '__main__':
    sp = spider("http://127.0.0.1:8080/")
    try:
        print(sp.send(None))
    except StopIteration as e:
        print(e.value)
```

```css
<h1>Hello World : 2020-12-21 11:19:55.197145<h1>
```

只有一个，看不到异步的效果，我们使用事件循环开启两个request试试：

```javascript
import asyncio
import requests

async def request(url):
    response = requests.get(url)
    print(response.text)
    return response.text

async def spider(url):
    return await request(url)

if __name__ == '__main__':
    sp1 = spider("http://127.0.0.1:8080/")
    sp2 = spider("http://127.0.0.1:8080/")
    tasks = [sp1, sp2]
    loop = asyncio.get_event_loop()
    # tasks = [loop.create_task(sp1), loop.create_task(sp2)]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
```

```css
<h1>Hello World : 2020-12-21 11:20:54.906349<h1>
<h1>Hello World : 2020-12-21 11:20:57.910104<h1>
```

我们看到，两个请求还是相隔了3秒，这说明不是异步的。

### aiohttp实现异步爬虫

因为requests内部是不支持异步的，要想实现异步，得使用aiohttp库：

```javascript
import asyncio
import time
import aiohttp

async def get_url(session, url):
    async with session.get(url) as resp:  # <4>
        return await resp.read()  # <5>


async def download_many(urls):
    async with aiohttp.ClientSession() as session:  # <8>
        res = await asyncio.gather(                 # <9>
            *[asyncio.create_task(get_url(session, url))
                for url in sorted(urls)])
    for r in res:
        print(r)
    return len(res)


def main():  # <10>
    urls = ['http://127.0.0.1:8080/'] * 5
    start_time = time.time()
    count = asyncio.run(download_many(urls))
    elapsed = time.time() - start_time
    msg = '\n{} urls downloaded in {:.2f}s'
    print(msg.format(count, elapsed))


if __name__ == '__main__':
    main()
```

```css
b'<h1>Hello World : 2020-12-21 11:14:11.098480<h1>'
b'<h1>Hello World : 2020-12-21 11:14:11.098480<h1>'
b'<h1>Hello World : 2020-12-21 11:14:11.098480<h1>'
b'<h1>Hello World : 2020-12-21 11:14:11.098480<h1>'
b'<h1>Hello World : 2020-12-21 11:14:11.097478<h1>'

5 urls downloaded in 3.01s
```

5次的请求处理的间隔几乎相同。

### 使用as_completed

```python
import asyncio
import time
import aiohttp
from functools import wraps


def time_elapsed(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        elapsed = end_time - start_time
        print(f'{res} used time in {elapsed}')
        return res
    return decorator


async def download_one(session, url, semaphore):
    async with semaphore:
        async with session.get(url) as resp:  # <4>
            return await resp.read()  # <5>


async def download_many(urls, coroutine_num):
    results = []
    semaphore = asyncio.Semaphore(coroutine_num)
    async with aiohttp.ClientSession() as session:
        to_do = [download_one(session, url, semaphore)
                 for url in urls]

        to_do_iter = asyncio.as_completed(to_do)
        for future in to_do_iter:
            res = await future
            print(f'many {res}')
            results.append(res)

    return results


@time_elapsed
def main():  # <10>
    coroutine_num = 5
    urls = ['http://127.0.0.1:8080/'] * 20
    results = asyncio.run(download_many(urls, coroutine_num))
    return len(results)


if __name__ == '__main__':
    main()
```

将download_one拆开：

```python
async def get_url(session, url):
    async with session.get(url) as resp:  # <4>
        return await resp.read()  # <5>

async def download_one(session, url, semaphore):
    async with semaphore:
        return await get_url(session, url)
```

