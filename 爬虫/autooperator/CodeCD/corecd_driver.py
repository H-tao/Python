from abc import abstractmethod

from Common.driver import Driver
from Config.settings import THRESHOLD_SET
from CodeCD.xpath_ import Xpather
from functools import wraps
from Common.utils import read_file_by_line_skip, do_retry
from Log.logging import logger
import requests
import warnings
import json
import time

RETRY_TIMES = 2  # 失败重试次数


class CoreCD_Driver(Driver):
    def __init__(self, show_windows=True):
        super().__init__(show_windows=show_windows)
        self.getter = InfoGetter(cookie=None)

    def login(self):
        """登录CoreCD，请在SPES开启W3免密登录"""
        self.open_url("https://corecd.inhuawei.com/")
        self.maxsize_window()
        # self.send_keys('//*[@id="uid"]', USERNAME)
        # self.send_keys('//*[@id="password"]', PS)
        # self.click_element('//*[@name="Submit"]')
        time.sleep(3)
        self.getter.set_cookie(self.get_cookie())

    def open_template_page(self):
        """打开 模板定义 页"""
        self._open_page("https://corecd.inhuawei.com/#/home/templateDefine")

    def open_pipeline_page(self):
        """打开 流水线实例 页"""
        self._open_page("https://corecd.inhuawei.com/#/home/pipeline")

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

    def open_template_by_name(self, template_name, std_out=True, retry_times=RETRY_TIMES):
        @do_retry(retry_times=retry_times, info='打开模板')
        def _open():
            url = f'https://corecd.inhuawei.com/#/home/pipelineFactory?templateName={template_name}'
            if std_out:
                logger.info(url)
            self.open_url_in_new_window(url)
            open_success = self.is_visible('//*[text()="已获取Template信息!"]', timeout=15)
            if not open_success:
                self.switch_to_main(close_current=True)
                return False
            return True
        return _open()

    def open_first_template(self):
        """ 打开搜索出的第一条记录 """
        is_not_available = self.is_visible('//*[@colspan="11"]', 1)
        if is_not_available:
            logger.info("不存在筛选出来的模板")
            return False
        self.click_element_until(Xpather.FIRST_TEMPLATE_A)
        self.switch_to_new(close_current=False)
        logger.info("打开筛选出来的模板成功!")
        return True

    def open_first_pipeline(self):
        """ 打开搜索出的第一条记录 """
        is_not_available = self.is_visible('//*[@colspan="9"]', 1)
        if is_not_available:
            logger.info("不存在筛选出来的流水线")
            return False
        self.click_element_until(Xpather.PIPELINE_FIRST)
        self.switch_to_new(close_current=False)
        logger.info("打开筛选出来的流水线成功!")
        return True

    @do_retry(retry_times=RETRY_TIMES, info='打开门禁配置')
    def open_threshold_config(self):
        self.click_element_until(Xpather.threshold)
        return self.is_visible('//*[@class="pipe-container"]', timeout=2)

    @do_retry(retry_times=RETRY_TIMES, info='打开代码仓配置')
    def open_repository_config(self):
        self.click_element_until(Xpather.SHOW_REPOSITORY)
        return self.is_visible('//button[@ng-click="addSubrepoInfo()"]', timeout=2)

    @do_retry(retry_times=RETRY_TIMES, info='打开模板基本配置')
    def open_modify_config(self):
        return self.click_element_until(Xpather.TEMPLATE_MODIFY)

    def click_tool(self, tool_name):
        @do_retry(retry_times=RETRY_TIMES, info=f'点击节点[{tool_name}]')
        def click():
            _ = self.click_element_until(Xpather.TEMPLATE_TOOL_NODE % tool_name, 2)
            time.sleep(1)
            return _
        return click()

    def click_sub_tool(self, sub_tool_name):
        @do_retry(retry_times=RETRY_TIMES, info=f'点击子节点[{sub_tool_name}]')
        def click():
            _ = self.click_element_until(Xpather.TEMPLATE_SUB_TOOL_NODE % sub_tool_name, 2)
            time.sleep(1)
            return _
        return click()

    def traverse_pipelines(self, codequality_or_mr="cq"):
        """
        遍历流水线的装饰器，跳过 # 注释掉的流水线
        :param codequality_or_mr: 参考 file_reader 方法读取流水线名称
        1. 选择
        CodeQuality流水线:  'c', 'cq', 'codequality'
        MR流水线: 'm', 'mr'
        personal流水线: 'p', 'pr', 'personal'
        fossbot流水线: 'f', 'fb' 'fossbot'
        自定义流水线: 'other'

        2. 使用示例
        'all':
            遍历所有Pipelines下文件夹
        'c':
            遍历CodeQuality流水线
        "cq" 或 "mr" 或 "ps" 或 "fb":
            "cq"遍历CodeQuality流水线；"mr"遍历MR流水线；"ps" 遍历personal流水线；"fb" 遍历fossbot流水线
        ['c', 'p', 'm', 'f']:
            一次遍历CodeQuality流水线；MR流水线；"personal流水线；"fossbot流水线
        :return:
        """
        def decorate(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                func_args = func.__code__.co_varnames
                has_template_name = True if 'template_name' in func_args else False
                names = self.pipeline_chooser(codequality_or_mr)
                for name in names:
                    logger.info(name)
                    if self.open_template_by_name(name):
                        if has_template_name:
                            func(name, *args, **kwargs)   # 执行
                        else:
                            func(*args, **kwargs)
                        time.sleep(0.5)
                    else:
                        logger.error('ERROR: Open template failed!!!')
            return wrapper
        return decorate

    def pipeline_chooser(self, codequality_or_mr=None):
        names = None
        if codequality_or_mr == 'all':
            codequality_or_mr = ['c', 'p', 'm', 'f', 'o']
        if isinstance(codequality_or_mr, list):
            names = [x for cm in codequality_or_mr for x in self.file_reader(cm)]
        elif isinstance(codequality_or_mr, str):
            names = self.file_reader(codequality_or_mr)
        return names

    @staticmethod
    def file_reader(codequality_or_mr=None):
        file_map = {
            'codequality_pipelines.py': ['codequality', 'codequality_pipelines', 'codequality_pipelines.py'],
            'mr_pipelines.py': ['mr', 'mr_pipelines', 'mr_pipelines.py'],
            'personal_pipelines.py': ['personal', 'personal_pipelines', 'personal_pipelines.py'],
            'fossbot_pipelines.py': ['fossbot', 'fossbot_pipelines', 'fossbot_pipelines.py'],
            'other.py': ['other', 'other.py']
        }
        for k, v in file_map.items():
            if codequality_or_mr in v:
                return read_file_by_line_skip(file=f"Pipelines/{k}", startwith='#')
        raise FileNotFoundError(f'未找到{codequality_or_mr}对应的流水线文件')

    def change_threshold_value(self, check_item, value=None, send_key=True, open_or_not=False):
        """ 修改、打开、关闭门禁值 """
        if isinstance(value, float) or isinstance(value, int):
            value = str(value)
        if not self.is_visible(Xpather.THRESHOLD_VALUE % check_item, 1):
            return False
        if send_key:
            self.send_keys_all(Xpather.THRESHOLD_VALUE % check_item, value)
        time.sleep(0.2)
        if open_or_not:
            return self.click_elements(Xpather.THRESHOLD_ENABLE % check_item)
        else:
            return self.click_elements(Xpather.THRESHOLD_DISABLE % check_item)

    def change_threshold_job_value(self, check_item, job_name, value=None, send_key=True, open_or_not=False):
        """ 修改、打开、关闭门禁值 """
        if isinstance(value, float) or isinstance(value, int):
            value = str(value)
        if not self.click_element_until(Xpather.THRESHOLD_JOB_DETAIL % check_item):
            logger.info(f'没有{check_item}')
            return False
        if not self.is_visible(Xpather.THRESHOLD_JOB_VALUE % job_name, 1):
            logger.info(f'没有{job_name}')
            return False
        if send_key:
            self.send_new_keys(Xpather.THRESHOLD_JOB_VALUE % job_name, value)
            logger.info(f'正在输入门禁值: {value}')
        time.sleep(0.2)
        if open_or_not:
            self.click_elements(Xpather.THRESHOLD_JOB_ENABLE % job_name)
        else:
            self.click_elements(Xpather.THRESHOLD_JOB_DISABLE % job_name)
        self.click_element_until(Xpather.THRESHOLD_JOB_DETAIL % check_item)
        logger.info(f'修改门禁值 [{check_item}] [{job_name}] [{value}] 完成。')

    @staticmethod
    def check_threshold_item(check_item):
        """ 检查是否有该门禁值 """
        if check_item not in THRESHOLD_SET:
            logger.info('无此门禁检查项，请在settings.py配置THRESHOLD_SET变量')
            return False
        return True

    def click_select(self, xpath, option=1):
        # 点击 select
        self.click_element(f'{xpath}/option{option}')

    def _open_page(self, url):
        self.open_url(url=url)
        time.sleep(2)
        self.refresh()

    def _next_page(self):
        return self.click_element_until(Xpather.NEXT_PAGE)

    def _prev_page(self):
        return self.click_element_until(Xpather.PREV_PAGE)

    def _search(self, keyword=None):
        self.send_new_keys(Xpather.FILTER, keyword)

    def search_pipeline_exist_row(self, pipeline_name):
        """ 搜索之后，返回流水线所在的行，返回0则代表流水线不存在 """
        row = 0
        a_s = self.browser.find_elements_by_xpath(Xpather.TEMPLATE_A_S)
        for _, a in enumerate(a_s):
            if a.text == pipeline_name:  # 匹配被复制的流水线所在列数
                row = _ + 1
                break
        return row

    def change_branch(self, git_urls, new_branch_name):
        # 打开仓配置
        self.open_repository_config()
        time.sleep(2)

        """ 获取URL """
        # Branch/revision
        urls = self.browser.find_elements_by_xpath('//*[@class="ti-table"]//td[3]/span')
        for index, url in enumerate(urls):
            # logger.info(url.text)
            if url.text in git_urls:
                # 点击修改
                self.click_element(
                    f'//*[@class="ti-table"]/tbody/tr[{index + 1}]//span/i[@ng-click="editSubRepoInfo(item)"]')
                time.sleep(0.2)
                # 修改分支名
                self.send_new_keys(f'//*[@class="ti-table"]/tbody/tr[{index + 1}]//td[4]/input', new_branch_name)
                # 确认修改 √
                self.click_element(
                    f'//*[@class="ti-table"]/tbody/tr[{index + 1}]//span/i[@ng-click="modifySubRepo(1,item);"]')
        # 确认整体修改
        self.click_element_until('//*[@ng-click="submitForSubRepo();"]')
        time.sleep(1)

    @staticmethod
    def get_template_run_detail_url(template_id):
        return f'https://corecd.inhuawei.com/#/home/pipelinerun?templateId={template_id}'


class BaseGetter:
    """
    用于获取CoreCD信息的类，CoreCD信息分为以下4个层次：
        template_info : https://corecd.inhuawei.com/passthrough/api/v1/template_info?templateName=paaslite_kubectl_plugin_mr
        chart_infos : https://corecd.inhuawei.com/passthrough/core_pipeline/v1/template/b3af4c131d674731b27dd4feee24b480/chart_infos
        sub_chart : https://corecd.inhuawei.com/passthrough/core_pipeline/v1/template/5c4c7f6752ef427aa0b0da96835e7ad6/sub_chart/3
        sub_node_info(job_info) : https://corecd.inhuawei.com/passthrough/core_pipeline/v1/job_info/e5539f2a80894542a64dbeb8d96cf324/swx944363?requestType=1&version=NFV_FusionStage+21.2.0

        关于参数:
        1. 一个template拥有一个chart，一个chart有多个sub_chart，比如Cmetrics、CodeDEX、Compile等
        2. 一个sub_chart拥有多个sub_node比如CodeDEX有CodeDEX_C、CodeDEX_Go、CodeDEX_Python
        例如：
        template: paaslite_kubectl_plugin_mr
        chart_id=b3af4c131d674731b27dd4feee24b480
        node(sub_chart): CodeDEX、Cmetrics、Compile...
        sub_node(job): CodeDEX的 CodeDEX_C、CodeDEX_Go、CodeDEX_Python
    """
    def get_command(self, template_name, node, sub_node):
        """ 获取流水线子节点配置的command """
        """
            例如：get_command('paaslite_swr_mr', 'CodeDex', ['CodeDEX_Go'])
            返回： 字符串
                cd ${WORKSPACE}
                # !/bin/sh
                set - x
                ... ...
        """
        res = self.get_sub_node_info(template_name, node, sub_node)
        job_info = json.loads(res['data']['job_info'])
        return job_info['command']

    def get_template_id(self, template_name):
        res = self.get_template_info(template_name)
        return res['data']['templateId'] if res else None

    def get_chart_id_and_node_id(self, template_name, node):
        res = self.get_chart_info(template_name)
        if res is None:
            logger.info(f'{template_name}无此节点{node}')
            return None, None
        chart_id = res['data'][0]['chartId']
        chart_nodes = res['data'][0]['chartNode']
        node_id = ''
        for chart_node in chart_nodes:
            if chart_node['label'] == node:
                node_id = chart_node['id']
        if not node_id:
            logger.info(f'{template_name}无此节点{node}')
            return chart_id, None
        return chart_id, node_id

    def get_sub_node_id(self, template_name=None, node=None, sub_nodes: list = None, chart_id=None, node_id=None):
        res = self.get_sub_chart_info(template_name, node, chart_id, node_id)
        if res is None:
            logger.info(f'{template_name}无此节点{node}')
            return None
        chart_nodes = res['data']['chartNode']
        sub_node_id = ''
        for chart_node in chart_nodes:
            for sub_node in sub_nodes:
                print(sub_node, chart_node['label'])
                if chart_node['label'] == sub_node:
                    sub_node_id = chart_node['remark']
                    logger.info(f'访问节点{sub_node}成功！')
                    return sub_node_id
        if not sub_node_id:
            logger.info(f'无此类节点{sub_nodes}')
            return None

    def get_template_info(self, template_name):
        """ template_info """
        _url = f'https://corecd.inhuawei.com/passthrough/api/v1/template_info?templateName={template_name}'
        return self._get(_url)

    def get_chart_info(self, template_name):
        """ chart_info """
        template_id = self.get_template_id(template_name)
        _url = f'https://corecd.inhuawei.com/passthrough/core_pipeline/v1/template/{template_id}/chart_infos'
        return self._get(_url) if template_id else None

    def get_sub_chart_info(self, template_name=None, node=None, chart_id=None, node_id=None):
        """
        1. 通过 template_name 和 node 获取 sub_chart_info
        2. 通过 chart_id 和 node_id 获取 sub_chart_info
        """
        _url = 'https://corecd.inhuawei.com/passthrough/core_pipeline/v1/template/%s/sub_chart/%s'
        if chart_id is None or node_id is None:
            chart_id, node_id = self.get_chart_id_and_node_id(template_name, node)
        _url = _url % (chart_id, node_id)
        return self._get(_url) if chart_id and node_id else None

    def get_sub_node_info(self, template_name=None, node=None, sub_nodes: list = None, chart_id=None, node_id=None):
        _url = 'https://corecd.inhuawei.com/passthrough/core_pipeline/v1/job_info/%s/swx944363?' \
               'requestType=1&version=NFV_FusionStage+21.2.0'
        sub_node_id = self.get_sub_node_id(template_name, node, sub_nodes, chart_id, node_id)
        _url = _url % sub_node_id
        return self._get(_url) if sub_node_id else None

    def get_last_record(self, template_id):
        """ 获取最新的运行记录 """
        _url = 'https://corecd.inhuawei.com/passthrough/core_pipeline/v1/pipeline/%s/last_record'
        _url = _url % template_id
        return self._get(_url)

    def get_sub_repo_info(self, template_name):
        """
        返回一个数组，示例如下：
        """
        """
            [
                {
                    'addr': 'ssh://git@gitlab.huawei.com:2222/paaslite/paaslite-cicd/FusionStage-Build.git',
                    'type': 'Git',
                    'codedir': 'FusionStage-Build',
                    'source_branch': 'br_FST21.0.0_730_forCenter', 'commit_id': ''
                },
                {
                    'type': 'Git',
                    'addr': 'ssh://git@gitlab.huawei.com:2222/paasliteexplore/SecurityScan.git',
                    'source_branch': 'master',
                    'codedir': 'securityscan', 'commit_id': ''
                },
                ...        
            ]
        """
        chart_info = self.get_chart_info(template_name)
        if chart_info['meta']['number'] == 0:   # 获取失败
            logger.info(chart_info)
            return None
        buildSubRepo = chart_info['data'][0]['buildSubRepo']
        buildSubRepo = json.loads(buildSubRepo)
        sub_repo_info = buildSubRepo['sub_repo_info']
        return sub_repo_info

    @abstractmethod
    def _get(self, _url):
        pass


class InfoGetter(BaseGetter):
    def __init__(self, cookie):
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'referer': 'https://corecd.inhuawei.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/86.0.4240.183 Safari/537.36',
            'Cookie': cookie,
        }
        warnings.filterwarnings('ignore')

    def set_cookie(self, cookie):
        self.headers['Cookie'] = cookie

    def _get(self, _url):
        logger.info(_url)
        response = requests.get(_url, headers=self.headers, verify=False)
        if response.status_code == 200:
            res = json.loads(response.text)
            return res
        else:
            logger.info(f'访问失败: {_url}')
            return None

    def post(self, _url, data=None, json=None):
        logger.info(_url)
        response = requests.post(_url, data=data, json=json, headers=self.headers, verify=False)
        logger.info(str(response))
        logger.info(response.text)


if __name__ == '__main__':
    self = CoreCD_Driver()

    # Login
    self.login()

    """模板页测试"""
    # 打开模板页
    self.open_template_page()

    # 搜索关键字
    self.search_template(keyword="CTtTTTTT")
    self.open_first_template()
    self.search_template(keyword="CodeQuality")
    self.open_first_template()

    """流水线页测试"""
    # 打开流水线页
    self.open_pipeline_page()

    # 搜索关键字
    self.search_pipeline(keyword="AAAAAA")
    self.open_first_pipeline()

    self.search_pipeline(keyword="mr")
    self.open_first_pipeline()

    while self.next_template_page():
        logger.info("下一页")

