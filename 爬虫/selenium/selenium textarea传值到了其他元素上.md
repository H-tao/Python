## 0. 前情提要

Python使用selenium操作textarea时，由于`send_keys()`要写入有多行值的脚本，脚本里面包含换行`\n`、`\t`等，所以遇到了一个很奇怪的bug，`send_keys()`把值写到了其他元素input上，让我有点懵逼。后面也试了调用js脚本设置textarea的value值，但是没办法把值写入后端的数据库。最后发现由于是脚本内`\n\t`导致`send_keys()`把值传入了其他的元素的input框内。只要把`\n\t`中的`\t`用四个空格替换，就不会出现这个问题了。

## 1. 问题代码

我要写入textarea的是下面一段脚本a.sh，里面包含了`\n\t`：

```shell
#!/bin/sh
set -x

if [ ! -f "test.txt" ];then
	echo "The file is not exist!"
fi
```

写入值的Python脚本：

```python
with open('a.sh', 'r', encoding='utf-8') as f:
    text = f.read()
    element = driver.find_element_by_xpath('\\textarea[@id="editNode"])')
    element.send_keys(text)
```

## 2. 解决办法：替换\t

```python
text = re.sub('\t', '    ', text)
```

## 3. 另辟蹊径：selenium使用js操作textarea元素替换value

**仅适用于前端读取textarea值是在value中的**，因为有的textarea是从json读值然后显示出来的，值不存在于value中，这种办法没办法写入数据。

我写了一个函数替换元素的value：

```python
def set_element_value(driver, xpath, value):
    """ Xpath中使用双引号，则拼接js时要使用单引号包裹双引号，否则会出现missing)after argument list """
    js = f'var ele = document.evaluate(\'{xpath}\', document).iterateNext(); ele.value = arguments[0];'
    driver.execute_script(js, value)
```

使用方法：

```python
my_driver.set_element_value(xpath=Xpather.TEXTAREA, value=text)
```

