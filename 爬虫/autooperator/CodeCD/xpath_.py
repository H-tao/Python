class Xpather:
    submit = '//*[@id="ngdialog1"]/div[2]/div/div[2]/button[1]'     # 确认按钮
    cancel = '//*[@id="ngdialog1"]/div[2]/div/div[2]/button[2]'     # 取消按钮

    # 筛选框
    FILTER = '//*[@id="tablefilter"]'

    # 流水线页面相关
    PIPELINE_TR = '//table/tbody/tr[%s]'   # 流水线行
    PIPELINE_NAME = f'{PIPELINE_TR}/td[2]/span/a'   # 流水线名
    PIPELINE_RUN = f'{PIPELINE_TR}/td[9]/span/i[1]'     # 流水线运行按钮
    PIPELINE_NEXT_PAGE = '//*[@id="content"]/div/div[2]/div/div/div/div[2]/div[2]/div/div[2]/div[2]/a[%s]'   # 下一页流水线
    NUM_LABEL = '//*[@ng-show="showPage"]/label'      # 流水线总数label
    PIPELINE_FIRST = PIPELINE_NAME % 1      # 第一条流水线的a标签

    # 模板页面相关
    TEMPLATE_TR_S = '//*[@class="table-bordered"]/tbody/tr[%s]'
    TEMPLATE_A_S = '//*[@class="table-bordered"]/tbody/tr//span/a'
    THE_TEMPLATE_A = '//*[@class="table-bordered"]/tbody/tr[%s]/td[2]/span/a'    # 搜索后的特定模板
    THE_TEMPLATE_COPY_BUTTON = '//*[@class="table-bordered"]/tbody/tr[%s]/td[11]/span/i[3]'      # 复制按钮
    THE_TEMPLATE_EDIT_BUTTON = '//*[@class="table-bordered"]/tbody/tr[%s]/td[11]/span/i[1]'      # 编辑按钮
    PROJECT_21_2_0_BUTTON = '//*[@class="table-bordered"]/tbody/tr[%s]/td[3]/select/option[text()="NFV_FusionStage 21.2.0"]'
    COMFIRM_MODIFY_BUTTON = '//*[@class="table-bordered"]/tbody/tr[%s]/td[11]/span/i[1]'
    THE_TEMPLATE_VERSION = '//*[@class="table-bordered"]/tbody/tr[%s]/td[4]/span'      # VERSION
    THE_TEMPLATE_PROJECT = '//*[@class="table-bordered"]/tbody/tr[%s]/td[3]/div/input'      # Project
    THE_TEMPLATE_PROJECT_OPTION = '//*[@class="table-bordered"]/tbody/tr[%s]/td[3]/select/option[text()="%s"]'


    THE_TEMPLATE_NAME_SPAN = '//*[@class="table-bordered"]/tbody/tr[%s]/td[2]/span'     # 名称
    THE_TEMPLATE_NAME_INPUT = '//*[@class="table-bordered"]/tbody/tr[%s]/td[2]/input'    # 名称输入框
    THE_TEMPLATE_COPY_CONFIRM = '//*[@class="table-bordered"]/tbody/tr[%s]/td[11]/span/i[1]'      # 确认复制
    THE_TEMPLATE_COPY_CANCEL = '//*[@class="table-bordered"]/tbody/tr[%s]/td[11]/span/i[2]'      # 取消复制
    FIRST_TEMPLATE_TR = TEMPLATE_TR_S % 1
    FIRST_TEMPLATE_A = '%s/td[2]/span/a' % FIRST_TEMPLATE_TR    # 搜索后第一个模板
    FIRST_TEMPLATE_COPY_BUTTON = '%s/td[11]/i[3]' % FIRST_TEMPLATE_TR    # 复制按钮
    FIRST_TEMPLATE_NAME_INPUT = '%s/td[2]/input' % FIRST_TEMPLATE_TR    # 名称输入框
    FIRST_TEMPLATE_COPY_CONFIRM = '%s/td[11]/span/i[1]' % FIRST_TEMPLATE_TR      # 确认复制
    FIRST_TEMPLATE_COPY_CANCEL = '%s/td[11]/span/i[2]' % FIRST_TEMPLATE_TR      # 取消复制
    TEMPLATE_REPLACE = '//div[@class="ngdialog-buttons"]//button[1]'     # 确认替换自动触发模板
    TEMPLATE_REPEAT_INFO = '//*[@id="toast-container"]/div'    # 提示模板名重复

    # 模板详情页
    TEMPLATE_PAGE_DIV = '//*[@id="content"]/div/div[2]/div/div[1]/div/div/div[2]/div[1]/form/div[3]'
    TEMPLATE_MODIFY = '%s/div[2]/div[5]/i' % TEMPLATE_PAGE_DIV
    TEMPLATE_ChartName = '%s/div[1]/div[1]/input' % TEMPLATE_PAGE_DIV
    TEMPLATE_Type = '%s/div[1]/div[2]/select' % TEMPLATE_PAGE_DIV
    TEMPLATE_Type_Personal = '%s/div[1]/div[2]/select/option[1]' % TEMPLATE_PAGE_DIV
    TEMPLATE_Type_Feature_Access = '%s/div[1]/div[2]/select/option[2]' % TEMPLATE_PAGE_DIV
    TEMPLATE_Type_Feature = '%s/div[1]/div[2]/select/option[3]' % TEMPLATE_PAGE_DIV
    TEMPLATE_Type_Master_Access = '%s/div[1]/div[2]/select/option[4]' % TEMPLATE_PAGE_DIV
    TEMPLATE_Type_Master = '%s/div[1]/div[2]/select/option[5]' % TEMPLATE_PAGE_DIV
    TEMPLATE_FailRetryTimes = '%s/div[1]/div[3]/input' % TEMPLATE_PAGE_DIV
    TEMPLATE_SourceBranch = '%s/div[2]/div[1]/input' % TEMPLATE_PAGE_DIV
    TEMPLATE_TargetBranch = '%s/div[2]/div[2]/input' % TEMPLATE_PAGE_DIV
    TEMPLATE_RepositoryURL = '%s/div[2]/div[3]/input' % TEMPLATE_PAGE_DIV
    TEMPLATE_CONFIRM_MODIFY = '%s/div[2]/div[5]/img[2]' % TEMPLATE_PAGE_DIV
    TEMPLATE_TOOL_NODE = '//div[@id="diagram1"]/*[@data-label="%s"]'    # 检查项节点
    TEMPLATE_SUB_TOOL_NODE = '//div[@id="diagram2"]/*[@data-label="%s"]'    # 检查项子节点
    TEMPLATE_Type_option = '%s/div[1]/div[2]/select/option[2]' % TEMPLATE_PAGE_DIV

    # 各个检查项的勾选框
    CHECK_Cmetrics = '//*[@data-label="Cmetrics"]/input'
    CHECK_CodeDex = '//*[@data-label="CodeDex"]/input'
    CHECK_GoStyle = '//*[@data-label="GoStyle"]/input'
    CHECK_Gometalinter = '//*[@data-label="Gometalinter"]/input'
    CHECK_SecurityScan = '//*[@data-label="Securityscan"]/input'
    CHECK_LLT = '//*[@data-label="LLT"]/input'

    # 通用
    NEXT_PAGE = '//*[@class="ti-pag-next"]'     # 下一页
    PREV_PAGE = '//*[@class="ti-pag-prev"]'     # 上一页
    NEXT_PAGE_DISABLED = '//*[@class="ti-pag-next disabled"]'   # 下一页不可用
    PREV_PAGE_DISABLED = '//*[@class="ti-pag-prev disabled"]'   # 上一页不可用

    # 工具配置项通用
    TOOL_CONFIRM_BUTTON = '//*[@id="configpanel_form"]/button[1]'   # 确认
    TOOL_CANCEL_BUTTON = '//*[@id="configpanel_form"]/button[2]'   # 确认
    ENVIRONMENT_SELECT = '//*[@name="configpanel_form"]//*[@ng-mousedown="menuMousedownFn($event)"]'  # environment的下拉框
    ENVIRONMENT_INPUT = '//*[@name="configpanel_form"]//*[@ng-mousedown="menuMousedownFn($event)"]/../input' # environment的input
    # COMMAND_TEXTAREA = '//*[@title="command"]/../div/textarea'
    COMMAND_TEXTAREA = '//span[text()="command:"]/../../div/textarea'

    # Gometalinter配置项

    # Repository配置项
    SHOW_REPOSITORY = '//*[@ng-click=" showSubRepo()"]'    # repository的加号

    # GoStyle配置项
    IS_USE_INCREASE_SWITCH_ENABLE = '//*[@title="isUseIncreaseSwitch"]/../div/select[@ng-change="changeValue()"]' \
                                    '/option[1]'  # 选择isUseIncreaseSwitch为True
    IS_USE_INCREASE_SWITCH_DISABLE = '//*[@title="isUseIncreaseSwitch"]/../div/select[@ng-change="changeValue()"]' \
                                     '/option[2]'  # 选择isUseIncreaseSwitch为False

    # LLT配置项
    LLT_CONFIRM_BUTTON = TOOL_CONFIRM_BUTTON

    # 门禁值
    threshold = '//*[@id="content"]/div/div[2]/div/div[1]/div/div/div[2]/div[1]/form/div[1]/div/button'     # 显示门禁按钮
    THRESHOLD_VALUE = '//span[text()="%s"]/../..//*[@ng-model="item.threshold_value"]'
    THRESHOLD_ENABLE = '//span[text()="%s"]/../..//*[@ng-model="item.threshold_status"]/option[3]'
    THRESHOLD_DISABLE = '//span[text()="%s"]/../..//*[@ng-model="item.threshold_status"]/option[2]'
    THRESHOLD_JOB_DETAIL = '//span[text()="%s"]/../../td[@ng-click="tipCannot(item)"]'
    THRESHOLD_JOB_VALUE = '//span[text()="%s"]/../../td/input[@ng-model="detail.threshold_value"]'
    THRESHOLD_JOB_ENABLE = '//span[text()="%s"]/../../td/input[@ng-model="detail.threshold_status"]/option[3]'
    THRESHOLD_JOB_DISABLE = '//span[text()="%s"]/../../td/input[@ng-model="detail.threshold_status"]/option[2]'



    # https://www.cnblogs.com/lone5wolf/p/10905339.html
