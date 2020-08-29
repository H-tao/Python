```python
from selenium.common.exceptions import TimeoutException, NoSuchElementException, InvalidElementStateException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui
from selenium import webdriver

SHOW_WINDOWS = True     # 是否有界面爬取
EXECUTABLE_PATH = 'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'    # chromedriver 执行路径

class Driver:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        if not SHOW_WINDOWS:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')  # 上面三行代码就是为了将Chrome不弹出界面，实现无界面爬取

        # 添加代理IP 如快代理：https://www.kuaidaili.com/ops/
        # chrome_options.add_argument("--proxy-server=http://27.154.34.146:39320")  # 代理地址

        self.browser = webdriver.Chrome(
            executable_path=EXECUTABLE_PATH,    # 驱动安装路径
            options=chrome_options,
        )

    def open_url(self, url):
        """ 打开一个页面 """
        try:
            self.browser.get(url)
            print("Open url %s success!" % url)
            return True
        except Exception as e:
            print(e)
            return False

    def find_element_by_xpath(self, xpath):
        """ 通过 xpath 定位一个元素 """
        try:
            element = self.browser.find_element_by_xpath(xpath)
        except NoSuchElementException as e:
            print(e)
            return None
        else:
            return element

    def is_visible(self, locator, timeout=10):
        """ 一直等待某个元素出现，默认超时10秒 """
        try:
            ui.WebDriverWait(self.browser, timeout).until(EC.visibility_of_element_located((By.XPATH, locator)))
            return True
        except TimeoutException:
            return False

    def is_not_visible(self, locator, timeout=10):
        """ 一直等待某个元素消失，默认超时10秒 """
        try:
            ui.WebDriverWait(self.browser, timeout).until_not(EC.visibility_of_element_located((By.XPATH, locator)))
            return True
        except TimeoutException:
            return False

    def is_clickable(self, locator, timeout=10):
        """ 一直等待某元素可点击，默认超时10秒 """
        try:
            ui.WebDriverWait(self.browser, timeout).until(EC.element_to_be_clickable((By.XPATH, locator)))
            return True
        except TimeoutException:
            return False

    def click_element(self, xpath):
        """ 定位 xpath 点击一个元素 """
        element = self.find_element_by_xpath(xpath)
        if element is not None:
            self.element_click(element)  # 点击元素
            return True
        else:
            return False

    def click_element_until(self, xpath, timeout=2):
        if not self.is_visible(xpath, timeout):  # 等待元素出现
            return False
        else:
            return self.click_element(xpath)

    @staticmethod
    def element_click(element):
        """ 通过一个元素点击 """
        try:
            element.click()
            return True
        except Exception as e:  # 输出报错原因
            print(e)
            return False

    def send_keys(self, xpath, keys):
        """  """
        self.is_visible(xpath)
        try:
            element = self.find_element_by_xpath(xpath)
            element.send_keys(keys)
            return True
        except NoSuchElementException as e:
            print(e)
            return False

    def send_new_keys(self, xpath, keys):
        self.is_visible(xpath)
        element = self.find_element_by_xpath(xpath)
        try:
            element.clear()
            element.send_keys(keys)
            return True
        except InvalidElementStateException as e:
            print(e)
            return False

    def switch_to_main(self, close_current=True):
        driver_ = self.browser
        if close_current:
            driver_.close()  # 关闭当前窗口
        driver_.switch_to.window(driver_.window_handles[0])  # 切换主窗口

    def switch_to_new(self, close_current=True):
        driver_ = self.browser
        if close_current:
            driver_.close()  # 关闭当前窗口
        driver_.switch_to.window(driver_.window_handles[-1])  # 切换主窗口

    def quit(self):
        self.browser.quit()

    # def status_code(self):
    #     self.browser.get()

    def open_url_in_new_window(self, url, close_current=False):
        js = f'window.open("{url}");'
        self.browser.execute_script(js)
        self.switch_to_new(close_current=close_current)

    def maxsize_window(self):
        self.browser.maximize_window()


if __name__ == '__main__':
    my_driver = Driver()
    my_driver.open_url("http://www.baidu.com")
    my_driver.send_new_keys('//*[@id="kw"]', 111)

```
