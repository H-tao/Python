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
