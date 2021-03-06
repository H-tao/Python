
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui
from selenium.webdriver import ActionChains
from selenium import webdriver
from Config.settings import EXECUTABLE_PATH
import time
import requests
import warnings
import json
from Log.logging import logger


class Driver:
    def __init__(self, show_windows=True):
        chrome_options = webdriver.ChromeOptions()
        if not show_windows:
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--disable-gpu')  # 上面三行代码就是为了将Chrome不弹出界面，实现无界面爬取
        else:
            chrome_options = None
        self.browser = webdriver.Chrome(
            # 驱动安装路径
            executable_path=EXECUTABLE_PATH,
            options=chrome_options,
        )

    def open_url(self, url):
        try:
            self.browser.get(url)
            print("Open url %s success!" % url)
        except Exception as e:
            print(e)

    def refresh(self):
        self.browser.refresh()   # 刷新
        time.sleep(2)

    def quit(self):
        self.browser.quit()

    def get_current_url(self):
        return self.browser.current_url

    def get_cookie(self):
        return '; '.join(['='.join([c['name'], c['value']]) for c in self.browser.get_cookies()])

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
            return True
        except Exception as e:  # 输出报错原因
            print(element.id, e)
            return False

    def click_element(self, xpath):
        element = self.find_element_by_xpath(xpath)
        if element is not None:
            self.element_click(element)  # 点击元素
            return True
        else:
            return False

    def click_element_until(self, xpath, timeout=10):
        if not self.is_visible(xpath, timeout):  # 等待元素出现
            return False
        else:
            return self.click_element(xpath)

    def click_elements(self, xpath):
        elements = self.browser.find_elements_by_xpath(xpath)
        if not elements:
            return False
        else:
            for element in elements:
                self.element_click(element)  # 点击元素
                time.sleep(0.2)
            return True

    def send_keys(self, xpath, keys):
        self.is_visible(xpath)
        try:
            element = self.browser.find_element_by_xpath(xpath)
            element.send_keys(keys)
            return True
        except NoSuchElementException as e:
            print(e)
            return False

    def send_new_keys(self, xpath, keys):
        self.is_visible(xpath)
        try:
            element = self.browser.find_element_by_xpath(xpath)
            time.sleep(0.05)
            try:
                element.clear()
            except ElementNotInteractableException:
                return False
            time.sleep(0.05)
            element.send_keys(keys)
            return True
        except NoSuchElementException as e:
            print(e)
            return False

    def clear_key(self, xpath):
        self.is_visible(xpath)
        try:
            element = self.browser.find_element_by_xpath(xpath)
            time.sleep(0.05)
            try:
                element.clear()
            except ElementNotInteractableException:
                return False
            else:
                return True
        except NoSuchElementException as e:
            print(e)
            return False

    def send_keys_all(self, xpath, keys):
        self.is_visible(xpath)
        try:
            elements = self.browser.find_elements_by_xpath(xpath)
            for element in elements:
                element.send_keys(keys)
            return True
        except NoSuchElementException as e:
            print(e)
            return False

    def send_new_keys_all(self, xpath, keys):
        self.is_visible(xpath)
        try:
            elements = self.browser.find_elements_by_xpath(xpath)
            time.sleep(0.05)
            try:
                for element in elements:
                    element.clear()
            except ElementNotInteractableException:
                return False
            time.sleep(0.05)
            for element in elements:
                element.send_keys(keys)
            return True
        except NoSuchElementException as e:
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

    def find_element_by_xpath(self, xpath):
        try:
            element = self.browser.find_element_by_xpath(xpath)
        except NoSuchElementException as e:
            print(e)
            return None
        else:
            return element

    @staticmethod
    def find_sub_element_by_xpath(element, xpath):
        try:
            sub_element = element.find_element_by_xpath(xpath)
        except NoSuchElementException as e:
            print(e)
            return None
        else:
            return sub_element

    # def status_code(self):
    #     self.browser._get()

    def set_element_value(self, xpath, value):
        """ Xpath中使用双引号，则拼接js时要使用单引号包裹双引号 """
        js = f'var ele = document.evaluate(\'{xpath}\', document).iterateNext(); ele.value = arguments[0];'
        self.browser.execute_script(js, value)
        
    def open_url_in_new_window(self, url, close_current=False):
        js = f'window.open("{url}");'
        self.browser.execute_script(js)
        self.switch_to_new(close_current=close_current)

    def maxsize_window(self):
        self.browser.maximize_window()

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
        """ 点击页面 (x,y) 坐标点。left_click: True为鼠标左键点击，否则为右键点击 """
        if left_click:
            ActionChains(self.browser).move_by_offset(x, y).click().perform()
        else:
            ActionChains(self.browser).move_by_offset(x, y).context_click().perform()
        ActionChains(self.browser).move_by_offset(-x, -y).perform()  # 将鼠标位置恢复到移动前

    def right_click_element(self, xpath):
        element = self.find_element_by_xpath(xpath)
        if element is None:
            return False
        ActionChains(self.browser).context_click(on_element=element).perform()
        return True

    def move_element_by_offset(self, xpath, x, y):
        """ 将一个元素按偏移移动 """
        element = self.find_element_by_xpath(xpath)
        ac = ActionChains(self.browser).drag_and_drop_by_offset(element, x, y)
        ac.perform()

    def move_element_to_another_element_by_offset(self, ele_xpath, to_ele_xpath, x=0, y=0):
        """ 将一个元素移动另一个元素的偏移(x,y)的位置 """
        ele = self.find_element_by_xpath(ele_xpath)
        time.sleep(0.5)
        to_ele = self.find_element_by_xpath(to_ele_xpath)
        ac = ActionChains(self.browser).click_and_hold(ele).move_to_element_with_offset(to_ele, x, y).release()
        ac.perform()


class WLogin:
    """
    CloudDragon、CoreCD、gitlab等平台都是通过 W3 进行登录的。
    """
    def __init__(self, uid, password):
        if not all([uid, password]):
            raise Exception('W3登录账号密码不能为空')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            'Referer': 'https://login.huawei.com/',
            'Origin': 'https://login.huawei.com',
        }
        self.post_url = 'https://login.huawei.com/login/login.do'
        self.visit_url = 'https://corecd.inhuawei.com/passthrough/core_pipeline/v1/pipeline/%s/last_record'
        self.pipelinerun_url = 'https://corecd.inhuawei.com/#/home/pipelinerun?templateId=%s'
        self.template_id = ''
        self.session = requests.Session()
        self.uid = uid
        self.password = password
        self.login_w()

    def login_w(self):
        warnings.filterwarnings('ignore')
        post_data = {
            'actionFlag': 'loginAuthenticate',
            'lang': 'en',
            'loginMethod': 'login',
            'loginPageType': 'mix',
            'version': 'V4.3.7',
            'deviceFingerInfo': 'd1848278c1f752cbc2c02c03bc58a214',
            'spesVersion': 'v2',
            'keyCheck': 'yy',
            'uid': self.uid,
            'password': self.password,
        }
        response = self.session.post(self.post_url, data=post_data, headers=self.headers)
        if response.status_code == 200:
            print(response)
        else:
            raise Exception("登录失败，请检查账号密码是否错误")

    def _get(self, _url):
        logger.info(_url)
        response = self.session.get(_url, headers=self.headers, verify=False)
        if response.status_code == 200:
            res = json.loads(response.text)
            return res
        else:
            logger.info(f'访问失败: {_url}')
            return None

    def get_corecd_cookie(self):
        _url = 'https://corecd.inhuawei.com/passthrough/api/v1/codecheck-info'  # 首页url
        self._get(_url)
        _cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
        _cookie = '; '.join(['='.join([k, v]) for k, v in _cookies.items()])
        return _cookie


if __name__ == '__main__':
    # driver = webdriver.Chrome()
    # driver.maximize_window()
    # driver.find_element_by_name("Submit")
    USERNAME = ''
    PASSWORD = ''

    cdl = WLogin(USERNAME, PASSWORD)
    template_name = 'paaslite_canal_codequality_21_1_0'

    cookie = cdl.get_corecd_cookie()
    from CodeCD.corecd_driver import InfoGetter
    getter = InfoGetter(cookie)
    template_id = getter.get_template_id(template_name)
    record = getter.get_last_record(template_id)
    print(template_id)
    print(record)
