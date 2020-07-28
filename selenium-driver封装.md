```python
class Driver:
    def __init__(self):
        self.executable_path = EXECUTABLE_PATH
        self.browser = webdriver.Chrome(
            # 驱动安装路径
            executable_path=self.executable_path,
        )

    def open_url(self, url):
        try:
            self.browser.get(url)
            print("Open url %s success!" % url)
        except Exception as e:
            print(e)

# 一直等待某个元素出现，默认超时10秒
def is_visible(self, locator, timeout=10):
    try:
        ui.WebDriverWait(self.browser, timeout).until(EC.visibility_of_element_located((By.XPATH, locator)))
        return True
    except TimeoutException:
        return False

# 一直等待某个元素消失，默认超时10秒
def is_not_visible(self, locator, timeout=10):
    try:
        ui.WebDriverWait(self.browser, timeout).until_not(EC.visibility_of_element_located((By.XPATH, locator)))
        return True
    except TimeoutException:
        return False

# 一直等待某元素可点击，默认超时10秒
def is_clickable(self, locator, timeout=10):
    try:
        ui.WebDriverWait(self.browser, timeout).until(EC.element_to_be_clickable((By.XPATH, locator)))
        return True
    except TimeoutException:
        return False

@staticmethod
def element_click(element):
    try:
        element.click()
    except Exception as e:  # 输出报错原因
        print(element.id, e)

def click_element(self, xpath):
    self.is_visible(xpath)  # 等待元素出现
    element = self.browser.find_element_by_xpath(xpath)  # 定位元素
    self.is_clickable(xpath)  # 等待元素可点击
    self.element_click(element)  # 点击元素

def quit(self):
    self.browser.quit()
```
