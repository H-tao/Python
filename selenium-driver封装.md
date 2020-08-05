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
## excel_handler

```
#!/usr/bin python
# -*- coding: utf-8 -*-
# __time__ = 2020/7/20

"""
整合代码仓、质量流水线表格，生成 完整的质量流水线信息表格，包括 "质量流水线", "语言", "名称", "维护团队", "归属 XM团队"
由 "codeHub-2020-07-22.xlsx" 和 "CloudPipeline_CodeQuality.xlsx"
生成 "CloudPipeline_CodeQuality-信息整合.xlsx"
"""

"""
代码仓EXCEL文件下载地址:
    http://10.29.181.224:8080/securityboard/html/index.html
"""

import pandas as pd
import re
import os
from collections import defaultdict
import numpy as np
from settings import FINAL_OUTPUT_EXCEL_PATH, PIPELINES_OUTPUT_EXCEL_PATH, PIPELINES_EXCEL_PATH
from settings import CODEREPOSITORY_EXCEL, TEAM_TO_XM_DICT
from settings import DATETIME

# 解决 Pandas 输出省略的问题
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)


class RelatedData():
    def __init__(self):
        # 读取excel文件，并指定Sheet
        pipeline_df = pd.read_excel(PIPELINES_EXCEL_PATH, sheet_name="Sheet2", header=None)
        pipeline_df = pipeline_df.drop_duplicates()

        # 我们的质量流水线名
        self.our_pipelines_list = list(pipeline_df.iloc[:, 0])
        # 提取质量流水线对应的工程名
        self.our_project_name_list = [re.findall(r'PaaSLite_(.*?)_8_0', string=x)[0] for x in self.our_pipelines_list]

        codehub_df = pd.read_excel(CODEREPOSITORY_EXCEL, sheet_name="代码仓")  # 读取代码仓
        self.hub_project_team = codehub_df.loc[:, ["名称", "维护团队", "java", "lua",
                                                   "javascript", "shell", "c/c++", "python", "go"]]  # 取出 名称列 和 维护团队列

        print(self.hub_project_team)
        self.hub_project_team["FormatName"] = [make_format(x.strip()) for x in self.hub_project_team["名称"]]
        print(self.hub_project_team)

        # 流水线工程名对应的维护团队， 注意：某些流水线工程没有对应的 维护团队 设为 ""
        self.hub_project_to_team_dict = defaultdict(str,
                                                    {make_format(x[0].strip()): (x[1] if x[1] != 1 else "") for x in
                                                     self.hub_project_team.fillna(value=1).values})  # 流水线工程名对应的维护团队

        self.team_to_xm_dict = defaultdict(str, TEAM_TO_XM_DICT)  # 维护团队对应的 XM团队
        # 流水线工程名对应的 XM团队
        # 1. 流水线工程名格式化为全小写 "-"转"_"      2. 某些流水线工程没有对应的 XM团队 设为 ""
        self.hub_project_to_xm_dict = defaultdict(str,
                                                  {make_format(key): (self.team_to_xm_dict[value] if value else "") for
                                                   key, value in self.hub_project_to_team_dict.items()})
        # 质量流水线对应的 维护团队
        self.our_project_to_team_dict = {project: self.hub_project_to_team_dict[make_format(project)] for project in
                                         self.our_project_name_list}
        # 质量流水线对应的 XM团队
        self.our_project_to_xm_dict = {project: self.hub_project_to_xm_dict[make_format(project)] for project in
                                       self.our_project_name_list}

        self.handle_special_project()

        self.interate_info()

    @staticmethod
    def change_name(df, column_name, column_value, change_column_name, new_value):
        index = np.where(df[column_name] == column_value)[0]
        if index.size > 0:
            df.at[index[0], change_column_name] = new_value

    def interate_info(self):
        """
        整合每一条流水线的信息（包括"质量流水线", "语言", "名称", "维护团队", "归属 XM团队"），并输出表格
        :return:
        """
        # 读取excel文件，并指定Sheet
        pipeline_df = pd.read_excel(PIPELINES_EXCEL_PATH, sheet_name="Sheet2", header=None,
                                    names=["质量流水线", "语言", "工程名称", "归属 XM团队"])
        pipeline_df = pipeline_df.drop_duplicates()
        pipeline_df["工程名称"] = self.our_project_name_list
        pipeline_df["FormatName"] = [make_format(x) for x in pipeline_df["工程名称"]]
        pipeline_df["归属 XM团队"] = [self.our_project_to_xm_dict[x] for x in self.our_project_name_list]
        pipeline_df["语言"] = ["Go服务"] * len(self.our_project_name_list)
        print(pipeline_df)
        print("*" * 80, "按XM分组排序", "*" * 80)
        print(pipeline_df.sort_values(by=["归属 XM团队", "工程名称"], ascending=[False, True]))

        print("*" * 80, "Merge", "*" * 80)
        one_merge = pd.merge(left=pipeline_df, right=self.hub_project_team, how="left", left_on="FormatName",
                             right_on="FormatName")
        one_merge["维护团队"] = one_merge["维护团队"].fillna(value="K8s应用管理")           # TODO：未归类维护团队的工程，暂时归于K8s应用管理
        one_merge["归属 XM团队"] = [TEAM_TO_XM_DICT[x] if not pd.isna(x) else "" for x in one_merge["维护团队"]]
        self.change_name(one_merge, "工程名称", "EMSAdapterPkg", "语言", "Python服务")
        self.change_name(one_merge, "工程名称", "FSPRIVILEGED", "语言", "Go服务、C&C++服务")
        self.change_name(one_merge, "工程名称", "SWR_API_SERVER", "语言", "Go服务、C&C++服务")
        self.change_name(one_merge, "工程名称", "UPGRADETOOLS", "语言", "Go服务、Python服务")
        self.change_name(one_merge, "工程名称", "VIOLIN", "语言", "Go服务、Python服务")

        print(one_merge.drop(columns="FormatName"))
        # self.save_to_excel(one_merge.drop(columns="FormatName"))

    def save_to_excel(self, df):
        print("======================== 文件保存至 ========================")
        path = f"{PIPELINES_OUTPUT_EXCEL_PATH}-{DATETIME}.xlsx"
        df.to_excel(path)
        print(os.path.abspath(path))
        # df.to_csv(f"{PIPELINES_OUTPUT_EXCEL_PATH}.csv", encoding="ANSI")

    # 有些工程 找不到对应的 XM 团队，单独处理
    def handle_special_project(self):
        """
        单独处理找不到 维护团队 或者 XM团队 的特殊工程
        :return:
        """
        #### 1. 不存在对应的 XM 团队
        # KUBECTL_PLUGIN == kubectl-plugin  : 不存在对应 XM 团队 和维护团队
        # CFETOOLSBOX == cfe-tools          : 不存在对应 XM 团队 和维护团队， 且代码仓名称有误为 cceTools，可修改为 cfe-tools
        #### 2. 代码仓工具名称有误
        # NP_PLUGIN == np-plugin            : 维护团队为 "K8s资源管理"，代码仓名称为 np-device-plugin，可修改为 np-plugin
        # POM == fsadmin                    : 维护团队为 "K8s资源管理"，代码仓名称为 fsadmin，未修改
        # UPGRADETOOLS == upgradetools      : 维护团队为 "部署与升级"，代码仓名称为 upgradebox，可修改为upgradetools

        #### 2. 对应值
        # 工程名称         对应CodeHub名称       维护团队         归属 XM团队
        # CFETOOLSBOX     cceTools                              K8s应用管理XM团队
        # KUBECTL_PLUGIN  kubectl-plugin                        K8s应用管理XM团队
        # NP_PLUGIN       np-device-plugin      K8s资源管理      K8s资源管理XM团队
        # POM             fsadmin               K8s资源管理      K8s资源管理XM团队
        # UPGRADETOOLS    upgradebox            部署与升级       PaaS集成XM团队

        self.change_name(self.hub_project_team, "名称", "cceTools", "FormatName", make_format("CFETOOLSBOX"))
        self.change_name(self.hub_project_team, "名称", "np-device-plugin", "FormatName", make_format("NP_PLUGIN"))
        self.change_name(self.hub_project_team, "名称", "fsadmin", "FormatName", make_format("POM"))
        self.change_name(self.hub_project_team, "名称", "upgradebox", "FormatName", make_format("UPGRADETOOLS"))

    def printf(self):
        print("我们的质量流水线名", end="\t")
        print(self.our_pipelines_list)
        print("我们的质量流水线的工程名", end="\t")
        print(self.our_project_name_list)
        print("CodeHub流水线工程名 - 维护团队", end="\t")
        print(self.hub_project_to_team_dict)
        print("维护团队 - XM团队", end="\t")
        print(self.team_to_xm_dict)
        print("CodeHub流水线工程名 - XM团队", end="\t")
        print(self.hub_project_to_xm_dict)
        # print(self.make_format('FusionStage-Build'))
        print(40 * "=")
        print("我们的质量流水线工程名 - XM团队", end="\t")
        print(self.our_project_to_xm_dict)
        # 输出未找到 XM团队的 工程名
        print("======================  未找到 XM团队的 工程名  ======================")
        for k, v in self.our_project_to_xm_dict.items():
            if not v:
                print(k)
        print("====================================================================")


# 统一大写转小写，"-" 转 "_"
def make_format(name):
    if name:
        return re.sub(r'-', r"_", name.lower())
    else:
        return name


def get_cols(sheet_name, project_name):
    """
    获取工程名所在的列号
    :param sheet_name: EXCEL的 Sheet
    :param project_name: 工程名
    :return: 成功返回列号，否则返回-1
    """
    df = pd.read_excel(FINAL_OUTPUT_EXCEL_PATH, sheet_name=sheet_name)
    cols = pd.DataFrame(data=np.arange(1, len(df.columns) + 1), index=df.iloc[0, :].values)
    try:
        col = cols.at[project_name, 0]
        return col
    except KeyError:
        return -1


def get_pipeline_info_df(project_name, column_name):
    """
    通过流水线工程名，获取流水线的 ["质量流水线", "语言", "名称", "维护团队", "归属 XM团队"] 之一
    :param project_name: CodeHub流水线工程名
    :param column_name: 列名，["质量流水线", "语言", "名称", "维护团队", "归属 XM团队"] 之一
    :return: 找到则返回字符串，否则返回空字符串
    """
    # 读取excel文件，并指定Sheet
    pipeline_df = pd.read_csv(PIPELINES_OUTPUT_EXCEL_PATH, header=0, index_col=0, encoding="ANSI", )
    pipeline_df.index = pipeline_df["名称"]
    pipeline_df = pipeline_df.drop(columns="名称")
    try:
        one_col = pipeline_df.loc[project_name, :]
        res = one_col[column_name]
        return res
    except KeyError:
        return ""


def output_integration_excel():
    d = RelatedData()
    # d.printf()


if __name__ == '__main__':
    output_integration_excel()
    # get_pipeline_info_df("ALARMNOTIFYSERVICE", "语言")
```

## spider

```
#!/usr/bin python
# -*- coding: utf-8 -*-
# __time__ = 2020/7/20


"""
脚本工作思路:
# 0. 输入云龙流水线用户名和密码
# 1. 取得流水线的所有信息（服务名、要爬取的检查数据项、数据项对应EXCEL表格的Sheet、行、列）
# 2. 爬取检查数据项
# 3. 存储数据项到所需要的表格
    存储一条流水线的信息需要:
    a). 爬取的检查数据项值
    b). 检查数据项对应到表格的表单、行、列数据
"""

from settings import GO_CHECK_DATA, GO_EXCEL_INDEX, C_CHECK_DATA, C_EXCEL_INDEX
from settings import Python_CHECK_DATA, Python_EXCEL_INDEX, Only_Python_CHECK_DATA
from settings import FINAL_OUTPUT_EXCEL_PATH, PIPELINES_OUTPUT_EXCEL_PATH, EXECUTABLE_PATH, INPUT_EXCEL_PATH
from settings import CHECK_SET
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui
from selenium import webdriver
import pandas as pd
import numpy as np
import openpyxl
import time
import re
import os

USERNAME = "swx944363"
PASSWORD = ''


class CloudPiplineWebUI:
    def __init__(self):
        self.executable_path = EXECUTABLE_PATH
        self.browser = webdriver.Chrome(
            # 驱动安装路径
            executable_path=self.executable_path,
        )
        self.wb = openpyxl.load_workbook(INPUT_EXCEL_PATH)
        self.current_url = ''

    def open_url(self, url):
        try:
            self.browser.get(url)
            print("Open CloudAnalytics url %s success!" % url)
        except Exception as e:
            print(e)

    def login(self):
        print("Login ...")
        driver = self.browser
        self.is_visible('//*[@id="uid"]')
        element = driver.find_element_by_xpath('//*[@id="uid"]')
        element.send_keys(USERNAME)
        element = driver.find_element_by_xpath('//*[@id="password"]')
        element.send_keys(PASSWORD)
        element = driver.find_element_by_xpath('//*[@name="Submit"]')
        self.element_click(element)

    def select_all_pipelines(self):
        time.sleep(4)  # 等待10秒，待元素加载完全
        self.click_element('//*[@id="filterByService"]/div/div/input')  # 点击- 查询策略框
        self.click_element('//*[@id="filterByService"]/div/ul/ul/li[4]')  # 点击选择- 所有的流水线
        time.sleep(2)

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

    def search_one(self, pipeline_name):
        driver = self.browser
        element = driver.find_element_by_xpath('//*[@id="filterByName"]/div/input')     # 搜索输入框
        element.clear()                     # 清空搜索框原有数据
        element.send_keys(pipeline_name)    # 输入流水线名
        fail_count = 3                      # 失败重试次数
        while fail_count:
            try:
                self.click_element('//*[@id="filterByName"]/div/span[1]')   # 点击搜索按钮
                pipeline_xpath = f'//*[@id="goDetail_{pipeline_name}"]'     # 搜索之后，流水线xpath会根据流水线名动态生成
                self.click_element(pipeline_xpath)                          # 点击流水线
                driver.switch_to.window(driver.window_handles[-1])          # 切换新窗口
                self.click_element('//*[@id="detailQualityID_Build"]')      # 点击- 质量检测报告按钮
                self.is_visible('//*[@id="quality-dialog"]/div/div/stage-all-quality/div/div/div')      # 等待质量检测报告加载
            except NoSuchElementException:
                print("打开新流水线窗口错误，重试中......")
                driver.switch_to.window(driver.window_handles[0])  # 切换回主窗口
                fail_count -= 1
                time.sleep(2)
                continue
            else:
                self.current_url = driver.current_url
                break

    def get_report_data(self):
        driver = self.browser
        # 抓取所有数据
        while True:
            try:
                self.is_visible('//*[@id="quality-dialog"]/div/div/stage-all-quality/div/div/ul/li/ul')
                element = driver.find_element_by_xpath('//*[@id="quality-dialog"]/div/div/stage-all-quality/div/div/ul/li/ul')
                result = element.text.split('\n')
                print("抓取到的所有数据:", len(result), result)
                return result
            except NoSuchElementException:
                element = driver.find_element_by_xpath('//*[@id="quality-dialog"]/div/div/stage-all-quality/div/div/ul/li/p')
                if element.text == "没有数据":
                    print("数据报告未刷新，等待刷新...")
                    time.sleep(2*64)                    # 报告未刷新出来，睡眠2分钟
                    self.click_element('//*[@id="refreshQuality"]')         # 点击刷新按钮
                continue

    def switch_to_main(self):
        driver = self.browser
        driver.close()  # 关闭当前窗口
        driver.switch_to.window(driver.window_handles[0])  # 切换主窗口

    def crawl_one(self, pipeline_name):
        self.search_one(pipeline_name)
        result = self.get_report_data()

        # 数据规整化
        i, len_res = 1, len(result)
        check_dict = {}
        while i < len_res:
            if result[i] in CHECK_SET:
                print(result[i], "====", result[i + 1])
                check_dict[result[i]] = result[i + 1]
                i += 1
            i += 1

        self.switch_to_main()
        # 返回规整化的数据字典
        return check_dict

    def parse_one(self, pipeline_name, languages, project_name):
        # print("===== [" + pipeline_name + "] =====")
        print("======== [数据抓取] =========")
        check_dict = self.crawl_one(pipeline_name)

        # 一条流水线存在多个服务
        check_data, check_index = {}, {}
        language_list = languages.split(sep='、')
        if len(language_list) == 0:
            print("*" * 40, "该流水线未分服务组", "*" * 40)
            return

        for language in language_list:
            if language == "Go服务":
                check_data = GO_CHECK_DATA
                check_index = GO_EXCEL_INDEX
            elif language == "C&C++服务":
                check_data = C_CHECK_DATA
                check_index = C_EXCEL_INDEX
            elif language == "Python服务" and len(language_list) > 1:
                check_data = Python_CHECK_DATA
                check_index = Python_EXCEL_INDEX
            elif language == "Python服务" and len(language_list) == 1:
                check_data = Only_Python_CHECK_DATA
                check_index = Python_EXCEL_INDEX

            print("======== [数据清洗与存储] =========")
            sheet_name = language
            column = self.get_cols(sheet_name=sheet_name, project_name=project_name)
            self.save_hyperlink(sheet_name, column, 2, self.current_url)
            # 一个插件需要多个数据项
            for plugin, items in check_data.items():
                # 清洗出来每一个插件的需要的每一项数据
                for item_name in items:
                    try:
                        check_dict[plugin]
                    except KeyError:
                        # print(f"{plugin}——{item_name}", "KeyError")
                        continue
                    else:
                        item_value = self.get_value(check_dict[plugin], item_name)
                        print(f"{plugin}——{item_name}", item_value)

                        # 存储到 EXCEL 表格
                        row = check_index[item_name]
                        if row != 0:
                            self.save_to_cell(sheet_name, column, row, float(item_value))

    def save_hyperlink(self, sheet_name, column, row, url):
        print(sheet_name, column, row, url)
        try:
            sheet = self.wb[sheet_name]
            try:
                sheet.cell(row=row, column=column).hyperlink = url
            except ValueError:
                print("存储失败，请检查数据项对应的表格行列是否正确")
        except KeyError:
            print("未在表格内找到对应的存储Sheet，请检查表格")

    def save_to_cell(self, sheet_name, column, row, value):
        print(sheet_name, column, row, value)
        try:
            sheet = self.wb[sheet_name]
            try:
                sheet.cell(row=row, column=column, value=value)
            except ValueError:
                print("存储失败，请检查数据项对应的表格行列是否正确")
        except KeyError:
            print("未在表格内找到对应的存储Sheet，请检查表格")

    def save_to_excel(self):
        try:
            self.wb.save(FINAL_OUTPUT_EXCEL_PATH)
        except PermissionError as error:
            print(error)
            print("======== [权限错误，存储失败，请检测是否关闭文件!!!] =========")
        except OSError as error:
            print(error)
            print("======== [存储失败，请检查文件格式!!!] =========")
        else:
            print("======== [所有数据存储至EXCEL表格已完成] =========")
            print(os.path.abspath(FINAL_OUTPUT_EXCEL_PATH))

    @staticmethod
    def get_cols(sheet_name, project_name):
        """
        获取工程名所在的列号
        :param sheet_name: EXCEL的 Sheet
        :param project_name: 工程名
        :return: 成功返回列号，否则返回-1
        """
        df = pd.read_excel(INPUT_EXCEL_PATH, sheet_name=sheet_name)
        cols = pd.DataFrame(data=np.arange(1, len(df.columns) + 1), index=df.iloc[0, :].values)
        try:
            col = cols.at[project_name, 0]
            return col
        except KeyError:
            return -1

    @staticmethod
    def get_value(string, key):
        """
        正则匹配获取数据项的值
        :param string: 爬取下来的包含数据项和数据项值的字符串
        :param key: 要匹配的数据项
        :return: 返回一个字符串类型的数字值
        """
        if not string:
            return 0
        value = re.findall(pattern=f"{key} (.*?) ", string=string)
        if value:
            return value[0]
        else:
            return re.findall(pattern=f"{key} (.*?)$", string=string)[0]


def run():
    """
    运行函数
    :return:
    """
    # 初始化
    win = CloudPiplineWebUI()
    url = 'https://szxy1-cdt.huawei.com/pipeline/home'
    win.open_url(url)
    win.login()
    win.select_all_pipelines()

    # 1. 取得流水线的所有信息
    # 读取excel文件，并指定Sheet
    # pipeline_df = pd.read_csv(f"{PIPELINES_OUTPUT_EXCEL_PATH}.csv", header=0, index_col=0, encoding="ANSI")
    pipeline_df = pd.read_excel(f"{PIPELINES_OUTPUT_EXCEL_PATH}.xlsx", header=0, index_col=0, )
    for index, row in pipeline_df.iterrows():
        pipeline_name, languages, project_name, team, xm = row["质量流水线"], row["语言"], row["工程名称"], row["维护团队"], row[
            "归属 XM团队"]

        # # 精确定位某条流水线示例：
        # if project_name != "ALARMNOTIFYSERVICE" and project_name != "CFETOOLSBOX":
        #     continue

        print(f"第 【{index + 1}】 条流水线 [ {pipeline_name} ] 正在抓取中...")
        # 2. 爬取数据项
        win.parse_one(pipeline_name=pipeline_name, languages=languages, project_name=project_name)

    win.quit()

    # 保存值到excel
    win.save_to_excel()


if __name__ == '__main__':
    run()
```

## settings

```
#!/usr/bin python
# -*- coding: utf-8 -*-
# __time__ = 2020/7/20

"""
配置文件信息:
0. TODO: 两个个文件不可或缺:
INPUT_EXCEL_PATH: 输出文件样本，TODO 人工填写，当文件修改时，EXCEL_INDEX也需要修改
PIPELINES_EXCEL_PATH: 信息整合表格

1. *_PATH:
    各种文件的路径
2. CHECK_DATA说明:
    GO_CHECK_DATA: "GO服务" 要抓取的检查数据项，请对应质量检查报表的数据项填写
    C_CHECK_DATA: "C&C++服务" 要抓取的检查数据项，请对应质量检查报表的数据项填写
3. EXCEL_INDEX说明:
    对应 INPUT_EXCEL_PATH
    GO_EXCEL_INDEX: "GO服务" 对应 INPUT_EXCEL_PATH 的 Sheet，每一个检查数据项对应的 表单列
    C_EXCEL_INDEX: "C&C++服务服务" 对应 INPUT_EXCEL_PATH 的 Sheet，每一个检查数据项对应的 表单列
4. TEAM_TO_XM_DICT:
    维护团队对应的 XM团队
"""

"""
服务说明:
    1. 大部分流水线只包含一个服务
        1) Go
            请查看信息整合表
        2) C
            请查看信息整合表
        3) Python
            EMSAdapterPkg
    2. 有的流水线包含两个服务, 比如:
        1) Go + Python
            VIOLIN fasadmin upgradebox(upgradetools)
        2) C + Python
            SWR_API_SERVER
"""

import datetime
import os
from collections import defaultdict

# webdriver路径
EXECUTABLE_PATH = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'

# 文件目录，一定要存在
INPUT_FILES_DIR = r'./input'
OUTPUT_FILES_DIR = r'./output'
# 当前日期
DATETIME = datetime.datetime.now().strftime("%Y-%m-%d")
ACCURATE_DATETIME = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")

# 必要读取的文件
# 读取输出文件样本
INPUT_EXCEL_PATH = os.path.join(INPUT_FILES_DIR, "PaaS质量统计数据格式.xlsx")
# 要抓取的质量流水线文件路径
PIPELINES_EXCEL_PATH = os.path.join(INPUT_FILES_DIR, "CloudPipeline_CodeQuality.xlsx")
# 代码仓路径
CODEREPOSITORY_EXCEL = os.path.join(INPUT_FILES_DIR, "codeHub-2020-07-22.xlsx")

# 输出文件
# 流水线信息整合文件
PIPELINES_OUTPUT_EXCEL_PATH = os.path.join(INPUT_FILES_DIR, "CloudPipeline_CodeQuality-信息整合")
# 最终输出统计数据的文件路径
FINAL_OUTPUT_EXCEL_PATH = os.path.join(OUTPUT_FILES_DIR, f"NFV_FusionStage 21.0.0 质量统计数据-{ACCURATE_DATETIME}.xlsx")

# 维护团队对应的 XM团队
TEAM_TO_XM_DICT = {
    "IDE组": "PaaS集成XM团队",
    "部署与升级": "PaaS集成XM团队",
    "云化使能": "K8s应用管理XM团队",
    "K8s应用管理": "K8s应用管理XM团队",
    "K8s资源管理": "K8s资源管理XM团队",
    "Other": "K8s应用管理XM团队",
}

# GO服务要爬取的数据项
GO_CHECK_DATA = {
    # 'complie': [],
    'cmetrics(job_Build) (Task Name)': ['Dangerous Functions Total:', 'Redundant Code Total:', 'Code Size:',
                                        'Cyclomatic Complexity Per Method:', 'Lines Per Method:',
                                        'Code Duplication Ratio:', 'File Duplication Ratio:', 'Lines Per File:'],
    'codedex(job_Build) (Task Name)': ['total:'],
    'codingstylecheck(job_Build) (Task Name)': ['NEW:', 'STANDARD_NEW:', 'STANDARD_RECOMMENDED_NEW:'],
    # 'gocyclo(job_Build) (Task Name)': ["max depth:"],         # 此项表格内不需要
    'golint(job_Build) (Task Name)': ['errors:'],
    'govet(job_Build) (Task Name)': ['high priority:', 'normal priority:', 'low priority:'],
    # 'llt(job_Build) (Task Name)': ['fail count:', 'skip count:', 'total count:']
    'FSPRIVILEGED_govet(job_Build) (Task Name)': ['high priority:', 'normal priority:', 'low priority:'],
}

# C&C++服务要爬取的数据项
C_CHECK_DATA = {
    # 'complie': [],
    'cmetrics_C(job_Build) (Task Name)': ['Dangerous Functions Total:', 'Redundant Code Total:', 'Code Size:',
                                          'Cyclomatic Complexity Per Method:', 'Lines Per Method:',
                                          'Code Duplication Ratio:', 'File Duplication Ratio:', 'Lines Per File:'],
    'codedex_C(job_Build) (Task Name)': ['total:'],
    'codingstylecheck_C(job_Build) (Task Name)': ['NEW:', 'STANDARD_NEW:', 'STANDARD_RECOMMENDED_NEW:'],
    'c_cmetrics(job_Build) (Task Name)': ['Dangerous Functions Total:', 'Redundant Code Total:', 'Code Size:',
                                          'Cyclomatic Complexity Per Method:', 'Lines Per Method:',
                                          'Code Duplication Ratio:', 'File Duplication Ratio:', 'Lines Per File:'],
    'c_codedex(job_Build) (Task Name)': ['total:'],
    'c_codingstylecheck(job_Build) (Task Name)': ['NEW:', 'STANDARD_NEW:', 'STANDARD_RECOMMENDED_NEW:'],
    'flexelint(job_Build) (Task Name)': ["error:", "warning:", "info:"],
}

# Python服务要爬取的数据项
Python_CHECK_DATA = {
    # 'complie': [],
    'cmetrics_python(job_Build) (Task Name)': ['Dangerous Functions Total:', 'Redundant Code Total:', 'Code Size:',
                                               'Cyclomatic Complexity Per Method:', 'Lines Per Method:',
                                               'Code Duplication Ratio:', 'File Duplication Ratio:', 'Lines Per File:'],
    'codedex_python(job_Build) (Task Name)': ['total:'],
    'codingstylecheck_python(job_Build) (Task Name)': ['NEW:', 'STANDARD_NEW:', 'STANDARD_RECOMMENDED_NEW:'],
}

# 只有Python服务要爬取的数据项
Only_Python_CHECK_DATA = {
    # 'complie': [],
    'cmetrics(job_Build) (Task Name)': ['Dangerous Functions Total:', 'Redundant Code Total:', 'Code Size:',
                                        'Cyclomatic Complexity Per Method:', 'Lines Per Method:',
                                        'Code Duplication Ratio:', 'File Duplication Ratio:', 'Lines Per File:'],
    'codedex(job_Build) (Task Name)': ['total:'],
    'codingstylecheck(job_Build) (Task Name)': ['NEW:', 'STANDARD_NEW:', 'STANDARD_RECOMMENDED_NEW:'],
}

CHECK_SET = set(GO_CHECK_DATA) | set(C_CHECK_DATA) | \
         set(Python_CHECK_DATA) | set(Only_Python_CHECK_DATA)

# 表头行数
HEADER_LINE_NUM = 2

# GO服务不同数据项对应的EXCEL行号
GO_EXCEL_INDEX = defaultdict(int, {
    # "complie ..": 3,
    "Dangerous Functions Total:": 4,
    "Redundant Code Total:": 5,
    "high priority:": 6,
    "normal priority:": 7,
    "low priority:": 8,
    "errors:": 9,
    "total:": 10,
    "NEW:": 11,
    "STANDARD_NEW:": 12,
    "STANDARD_RECOMMENDED_NEW:": 13,
    "Code Size:": 14,
    "Cyclomatic Complexity Per Method:": 15,
    "Lines Per Method:": 16,
    "Code Duplication Ratio:": 17,
    "File Duplication Ratio:": 18,
    "Lines Per File:": 19,
})

# C&C++服务不同数据项对应的EXCEL行号
C_EXCEL_INDEX = defaultdict(int, {
    # "complie ..": 3,
    "Dangerous Functions Total:": 4,
    "Redundant Code Total:": 5,
    "error:": 6,
    "warning:": 7,
    "info:": 8,
    "total:": 9,
    "NEW:": 10,
    "STANDARD_NEW:": 11,
    "STANDARD_RECOMMENDED_NEW:": 12,
    "Code Size:": 13,
    "Cyclomatic Complexity Per Method:": 14,
    "Lines Per Method:": 15,
    "Code Duplication Ratio:": 16,
    "File Duplication Ratio:": 17,
    "Lines Per File:": 18,
})

# Python服务不同数据项对应的EXCEL行号
Python_EXCEL_INDEX = defaultdict(int, {
    # "complie ..": 3,
    "Dangerous Functions Total:": 4,
    "Redundant Code Total:": 5,
    "total:": 6,
    "NEW:": 7,
    "STANDARD_NEW:": 8,
    "STANDARD_RECOMMENDED_NEW:": 9,
    "Code Size:": 10,
    "Cyclomatic Complexity Per Method:": 11,
    "Lines Per Method:": 12,
    "Code Duplication Ratio:": 13,
    "File Duplication Ratio:": 14,
    "Lines Per File:": 15,
})
```
