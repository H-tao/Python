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
SHOW_WINDOWS = False

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
FINAL_OUTPUT_EXCEL_PATH = os.path.join(OUTPUT_FILES_DIR, f"NFV_FusionStage 21.1.0 质量统计数据-{ACCURATE_DATETIME}.xlsx")

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
    "Llt Tc Changed Coverage": 20,
    "Llt Tc Total Coverage": 21,
    "Llt Tc Total Number": 22,
    "Llt Problem Interception": 23,
    "Llt Tc Pass Rate": 24,
    "Llt URL": 25,
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
