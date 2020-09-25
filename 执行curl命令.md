Curl命令详解：
https://www.cnblogs.com/xingxia/p/linux_curl.html
```
import argparse
import os
import pandas as pd
import re
import json
import subprocess

"""
拉取新分支，从swx944363_test拉取一个swx944363_test_10
$ python getBranchInLinux.py --getBranch --ref swx944363_test --target swx944363_test_10

删除分支，删除分支swx944363_test_10
$ python getBranchInLinux.py --delBranch --target swx944363_test_10
"""


workbook = pd.read_excel("configTable.xlsx", sheet_name='Sheet1')
GITHUB_API = " https://gitlab.huawei.com/api/v4/projects/%(project_id)s"
CURL_POST = "curl --request POST --header"
CURL_GET = "curl --header"
CURL_DEL = "curl --request DELETE --header"
# 获取配置文件中token信息
private_token = workbook.at[0, "private_tokens"]
TOKEN = f'"PRIVATE-TOKEN: {private_token}"'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--delBranch', required=False, help='delete branch', action="store_true")
    parser.add_argument('--getBranch', required=False, help='get branch', action="store_true")
    parser.add_argument('--ref', default='master', help="要拉取的原分支")
    parser.add_argument('--target', help="拉出的目标分支/要删除的分支")

    args = parser.parse_args()
    ref, target = args.ref, args.target
    if target is None:
        raise Exception("请使用 [ --target 分支名 ] 指定目标分支")

    if args.getBranch:
        print("="*20, "开始拉取新分支", "--原分支:", ref, "--目标分支:", target, "="*20)
    elif args.delBranch:
        print("="*20, "开始删除分支", "[ ", target, " ]", "="*20)
        # print("为确保安全，删除分支功能未启用，请确认需要删除分支，修改代码重新提交后启用")
    read_config_tabel(ref, target, get_=args.getBranch, delele_=args.delBranch)


def read_config_tabel(ref_branch, target_branch, get_=False, delele_=False):
    for i in range(workbook.shape[0]):
        git_url = workbook.at[i, 'url']
        project_id = workbook.at[i, "id"]
        target_branch = re.sub('/', '%2F', target_branch)
        print("代码仓ID:", project_id, "代码仓地址:", git_url)
        project_url = GITHUB_API % {'project_id': project_id}

        if get_:
            get_branchs(ref_branch, target_branch, project_url)
        if delele_:
            del_branchs(target_branch, project_url)


def get_branchs(ref_branch, target_branch, project_url):
    # 拉分支
    params = f'-d "ref={ref_branch}&branch={target_branch}"'
    get_new_branch_command = ' '.join([CURL_POST, TOKEN, params, f'{project_url}/repository/branches'])
    response = execute_command(get_new_branch_command)
    res_dict = json.dumps(response)
    if target_branch in res_dict:
        print("SUCCESS: 创建分支成功！")
    else:
        raise Exception("FAIL: 创建分支失败! " + str(res_dict))

    # 分支保护， 默认设置committer可合入
    params = f'-d "name={target_branch}&push_access_level=0&merge_access_level=40"'
    protect_branch_command = ' '.join([CURL_POST, TOKEN, params, f'{project_url}/protected_branches'])
    # response = execute_command(protect_branch_command)


def del_branchs(target_branch, project_url):
    # 先取消分支保护
    unprotect_branch_command = ' '.join([CURL_DEL, TOKEN, f'{project_url}/protected_branches/{target_branch}'])
    response = execute_command(unprotect_branch_command)

    # 删除分支
    del_branch_command = ' '.join([CURL_DEL, TOKEN, f'{project_url}/repository/branches/{target_branch}'])
    response = execute_command(del_branch_command)
    res_dict = json.dumps(response)
    if 'message' in res_dict:
        raise Exception("FAIL: 删除分支失败! " + str(res_dict))


def execute_command(command_str):
    print(command_str)
    response = subprocess.Popen(command_str, shell=True, stdout=subprocess.PIPE).stdout
    print("="*40, "message", "="*40)
    response = response.read().decode('utf-8')
    print(response)
    return response


if __name__ == '__main__':
    print("*"*200)
    main()
    print("*"*200)
```
