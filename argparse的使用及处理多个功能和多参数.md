## argparse官方文档

https://docs.python.org/zh-cn/3.9/library/argparse.html

## argparse使用示例

### 功能示例

```python
import argparse

parser = argparse.ArgumentParser(description='manual to this script', prefix_chars='-+/')

# 指定type
parser.add_argument('-p', type=int, default=1, help="The number of page")
parser.add_argument('-d', type=str,  default="default_database", help="The name of MySQL's database!")   # 指定type

# 布尔开关
parser.add_argument('-t', action='store_false', default=True)   # 布尔开关，指定-t时，args.t为False，不指定则为True
parser.add_argument('-f', action='store_true', default=False)   # 布尔开关，指定-f时，args.f为True，不指定则为False

# 前缀使用+，一定要配置prefix_chars
parser.add_argument('-a', action='store_true')
parser.add_argument('+a', action='store_false')

# 互斥选项
group = parser.add_mutually_exclusive_group()
group.add_argument('-q', action='store_true')
group.add_argument('-w', action='store_true')

# 可变参数-nargs='+'，'?':0或者1个参数。'*':0或者多个参数。'+'=1或者多个参数。
parser.add_argument('-k', type=str, nargs='+', default=['python', 'C++'])  # 指定str关键字列表

# 限制选项
parser.add_argument('-c', choices=('a', 'b'))

# 参数分组
group = parser.add_argument_group('authentication')
group.add_argument('--user', action="store")
group.add_argument('--password', action="store")

args = parser.parse_args()
print(args)
# print(args.d, args.k, args.p, args.t, args.f, args.a, args.user, args.password)
```

### 使用add_subparsers处理多个功能使用多个不同参数

```python
import argparse


def handle_read(args):
    print(args)
    print(args.path, args.length, args.key)


def handle_write(args):
    print(args)
    print(args.path, args.encoding)


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(help='commands')

    read_parser = subparsers.add_parser(name='read', help='read file')
    read_parser.add_argument('--path', required=True, help="file path")
    read_parser.add_argument('--length', required=True, help="file length")
    read_parser.add_argument('--key', required=True, help="file key")
    read_parser.set_defaults(func=handle_read)	# 绑定处理函数

    write_parser = subparsers.add_parser(name='write', help='write file')
    write_parser.add_argument('--path', required=True, help="file path")
    write_parser.add_argument('--encoding', required=True, help="file encoding")
    write_parser.set_defaults(func=handle_write)	# 绑定处理函数

    args = parser.parse_args()
    # 执行函数功能
    args.func(args)


if __name__ == '__main__':
    main()
```

使用：

```shell
$ python argparse3.py read -h
usage: argparse3.py read [-h] --path PATH --length LENGTH --key KEY

optional arguments:
  -h, --help       show this help message and exit
  --path PATH      file path
  --length LENGTH  file length
  --key KEY        file key


$ python argparse3.py write -h
usage: argparse3.py write [-h] --path PATH --encoding ENCODING

optional arguments:
  -h, --help           show this help message and exit
  --path PATH          file path
  --encoding ENCODING  file encoding
  
  
$ python argparse3.py read --path C:/desktop --length 10 --key project
Namespace(func=<function handle_read at 0x000001AC47B14EE8>, key='project', length='10', path='C:/desktop')
C:/desktop 10 project


$ python argparse3.py write --path C:/desktop --encoding utf-8
Namespace(encoding='utf-8', func=<function handle_write at 0x000001CB2BDF9438>, path='C:/desktop')
C:/desktop utf-8
```



参考博客：https://www.jianshu.com/p/e2f9de45a981
