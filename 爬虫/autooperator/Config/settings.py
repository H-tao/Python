import datetime
import os
from collections import defaultdict

USERNAME = ''
PS = ''

# webdriver路径
EXECUTABLE_PATH = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
SHOW_WINDOWS = True


""" ==================================== 分割线 =================================== """
"""                              以下为各文件对应的路径                              """
""" ==================================== 分割线 =================================== """

# 项目根路径
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
# 文件目录，一定要存在
INPUT_FILES_DIR = os.path.join(ROOT_PATH, r'CodeCD/input')
OUTPUT_FILES_DIR = os.path.join(ROOT_PATH, r'CodeCD/output')
# 当前日期
DATETIME = datetime.datetime.now().strftime("%Y-%m-%d")
ACCURATE_DATETIME = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")

# 必要读取的文件
# 读取输出文件样本
INPUT_EXCEL_PATH = os.path.join(INPUT_FILES_DIR, "CoreCD质量统计数据格式修改版.xlsx")
# 要抓取的质量流水线文件路径
PIPELINES_EXCEL_PATH = os.path.join(INPUT_FILES_DIR, "CloudPipeline_CodeQuality.xlsx")
# 代码仓路径
CODEREPOSITORY_EXCEL = os.path.join(INPUT_FILES_DIR, "NFV_FusionStage_21.1.0.B020构建使用的全量代码仓.xlsx")
# MR构建失败格式表
MR_FAILURE_EXCEL = os.path.join(INPUT_FILES_DIR, "MR构建失败记录格式表.xlsx")

# 输出文件
# 流水线信息整合文件
PIPELINES_OUTPUT_EXCEL_PATH = os.path.join(INPUT_FILES_DIR, "CoreCD_CodeQuality_Pipelines-信息整合.xlsx")
# 最终输出统计数据的文件路径
FINAL_OUTPUT_EXCEL_PATH = os.path.join(OUTPUT_FILES_DIR, f"NFV_FusionStage 21.3.0 CoreCD质量统计数据-{ACCURATE_DATETIME}.xlsx")
