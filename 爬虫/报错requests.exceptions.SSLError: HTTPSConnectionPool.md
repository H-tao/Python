requests报错：
```css
requests.exceptions.SSLError: HTTPSConnectionPool

urllib3.exceptions.MaxRetryError: HTTPSConnectionPool

ssl.SSLError: ("bad handshake: Error([('SSL routines', 'tls_process_server_certificate', 'certificate verify failed')])",)

OpenSSL.SSL.Error: [('SSL routines', 'tls_process_server_certificate', 'certificate verify failed')]
```
解决办法：
```python
import requests

response = requests.get(_url, headers=self.headers, verify=False)   # 加入verify=False

```
