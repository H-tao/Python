```python
from driver import Driver
from Config.settings import PS
import time
from CodeCD.xpath_ import Xpather
from functools import wraps
from utils import read_file_by_line_skip
from selenium.webdriver import ActionChains


class CoreCD_Driver(Driver):
    def __init__(self, show_windows=True):
        super().__init__(show_windows=show_windows)

    def login(self):
        """登录CoreCD"""
        self.open_url("https://corecd.inhuawei.com/")
        self.maxsize_window()
        self.send_keys('//*[@id="uid"]', "swx944363")
        self.send_keys('//*[@id="password"]', PS)
        self.click_element('//*[@name="Submit"]')
        time.sleep(2)

    def get_current_url(self):
        return self.browser.current_url

    def open_template_page(self):
        """打开 模板定义 页"""
        self._open_page("https://corecd.inhuawei.com/#/home/templateDefine")

    def open_pipeline_page(self):
        """打开 流水线实例 页"""
        self._open_page("https://corecd.inhuawei.com/#/home/pipeline")

    def _open_page(self, url):
        self.open_url(url=url)
        time.sleep(2)
        self.refresh()

    def refresh(self):
        self.browser.refresh()   # 刷新
        time.sleep(2)

    def next_template_page(self):
        """ 下一页模板 """
        return self._next_page()

    def next_pipeline_page(self):
        """ 下一页流水线 """
        return self._next_page()

    def prev_template_page(self):
        """ 上一页模板 """
        return self._prev_page()

    def prev_pipeline_page(self):
        """ 上一页流水线 """
        return self._prev_page()

    def search_template(self, keyword=None):
        """ 搜索模板 """
        self._search(keyword)

    def search_pipeline(self, keyword=None):
        """ 搜索流水线 """
        self._search(keyword)

    def open_first_template(self):
        """ 打开搜索出的第一条记录 """
        is_not_available = self.is_visible('//*[@colspan="11"]', 1)
        if is_not_available:
            print("查无此模板")
            return False
        self.click_element_until(Xpather.TEMPLATE_FIRST)
        self.switch_to_new(close_current=False)
        return True

    def open_first_pipeline(self):
        """ 打开搜索出的第一条记录 """
        is_not_available = self.is_visible('//*[@colspan="9"]', 1)
        if is_not_available:
            print("查无此流水线")
            return False
        self.click_element_until(Xpather.PIPELINE_FIRST)
        self.switch_to_new(close_current=False)
        return True

    def traverse_pipelines(self, codequality_or_mr="cq"):
        """
        遍历流水线的装饰器，跳过 # 注释掉的流水线
        :param codequality_or_mr: "cq" 或 "mr" : "cq"遍历CodeQuality流水线；"mr"遍历MR流水线
        :return:
        """
        def decorate(func):
            @wraps(func)
            def wrapper(*agrs, **kwargs):
                if codequality_or_mr == "cq":
                    names = read_file_by_line_skip(file="Pipelines/codequality_pipelines.txt", startwith='#')
                else:
                    names = read_file_by_line_skip(file="Pipelines/mr_pipelines.txt", startwith='#')
                for name in names:
                    print(name)
                    url = f'https://corecd.inhuawei.com/#/home/pipelineFactory?type=CI&autoFlag=false&templateName={name}'
                    print(url)
                    self.open_url_in_new_window(url)
                    time.sleep(2)
                    func(*agrs, **kwargs)   # 执行
                    time.sleep(2)
            return wrapper
        return decorate

    def check_value(self, xpath_str, check=True):
        """
        勾选或取消勾选 selected 框
        :param xpath_str: 元素的Xpath
        :param check: 是否勾选，True 为勾选，False为取消勾选
        :return:
        """
        # 是否有该检查项
        is_visible = self.is_visible(xpath_str)
        if not is_visible:
            print("没有该检查项")
            return

        # 检查是否已经勾选
        element = self.find_element_by_xpath(xpath_str)
        try:
            checked = element.get_attribute('checked')
        except AttributeError:
            checked = False

        if checked & check:
            print("已经勾选且需要勾选/没有勾选且不需要勾选")
            return
        else:
            print("没有勾选且需要勾选/勾选且不需要勾选")
            self.click_element_until(xpath_str)

    def click_locate_xy(self, x, y, left_click=True):
        """
        点击页面 (x,y) 坐标点
        :param x:
        :param y:
        :param left_click: True为鼠标左键点击，否则为右键点击
        :return:
        """
        if left_click:
            ActionChains(self.browser).move_by_offset(x, y).click().perform()
        else:
            ActionChains(self.browser).move_by_offset(x, y).context_click().perform()
        ActionChains(self.browser).move_by_offset(-x, -y).perform()  # 将鼠标位置恢复到移动前

    def click_select(self, x):
        # 点击 select
        pass

    def _next_page(self):
        return self.click_element_until(Xpather.NEXT_PAGE)

    def _prev_page(self):
        return self.click_element_until(Xpather.PREV_PAGE)

    def _search(self, keyword=None):
        self.send_new_keys(Xpather.FILTER, keyword)


if __name__ == '__main__':
    my_driver = CoreCD_Driver()

    # Login
    my_driver.login()

    """模板页测试"""
    # 打开模板页
    my_driver.open_template_page()

    # 搜索关键字
    my_driver.search_template(keyword="CTtTTTTT")
    my_driver.open_first_template()
    my_driver.search_template(keyword="CodeQuality")
    my_driver.open_first_template()

    """流水线页测试"""
    # 打开流水线页
    my_driver.open_pipeline_page()

    # 搜索关键字
    my_driver.search_pipeline(keyword="AAAAAA")
    my_driver.open_first_pipeline()

    my_driver.search_pipeline(keyword="mr")
    my_driver.open_first_pipeline()

    while my_driver.next_template_page():
        print("下一页")



```
