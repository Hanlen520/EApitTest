# -*- coding: utf-8 -*-
# @Time    : 2018/5/25 19:52
# @Author  : Burrows
# @FileName: start.py
"""框架执行主入口"""
import logging
import logging.config
import os
import time

import data_mapping
from casedata import CaseData
from oper_excel import OperExcel
from oper_json import OperJson
from rele_data import ReleData
from report import Report
from res_assert import ResAssert
from run_method import RunMethod

from test_demo.jiatui_api_test.src.oper_file import OperFile


class RunTest:
    def __init__(self):
        self.ru_method = RunMethod()
        self.case_data = CaseData()
        self.re_assert = ResAssert()
        self.op_excel = OperExcel()
        self.op_file = OperFile()
        self.op_json = OperJson()

        # 初始化运行数据
        self.start_row = 1  # 起始运行行号
        self.nrows = self.case_data.get_cases_lines()  # 总行数
        # rootpath
        self.rootdir = os.path.dirname(os.path.abspath(__file__))
        # 读取日志配置
        log_conf_file = 'logging.conf'  # 日志配置文件
        log_path = self.rootdir + "\\conf\\" + log_conf_file  # 日志配置文件绝对路径
        logging.config.fileConfig(log_path)
        self.logger = logging.getLogger('simpleExample')
        # 生成日志文件
        log_src = "run.log"  # 运行时日志，logging.conf中配置
        self.run_log_src = self.rootdir + '\\log\\' + log_src
        # 统计测试数据
        self.static_all = {}  # 概要统计字典
        self.pass_cases = []  # 运行通过的用例集
        self.fail_cases = []  # 运行失败的用例集
        list_apis = self.op_excel.get_col_value(data_mapping.get_interface_name())
        list_apis.pop(0)
        self.api_set = set(list_apis)  # 本次测试接口集合
        self.static_apis = {}  # 详细接口统计字典
        for case_id in self.api_set:
            self.static_apis[case_id] = {'pass': [], 'fail': []}

    def setup(self):
        """初始化环境"""
        self.logger.info("开始程序运行".ljust(16, "."))
        self.logger.info("开始初始化环境".ljust(64, "#"))
        self.op_json.setup_data()
        self.op_file.trunc_file(self.run_log_src)
        self.logger.info("初始化环境完成".ljust(64, "#"))

    def teardown(self):
        """恢复环境"""
        self.logger.info("开始恢复环境".ljust(64, "#"))
        self.logger.info("恢复环境完成".ljust(64, "#"))
        self.logger.info("退出程序运行".ljust(16, "."))
        self.test_report.close()

    def start(self):
        """程序执行入口"""
        self.setup()
        self.logger.info("开始测试".ljust(32, "-"))
        # 生成报告与运行时日志
        start_time = time.time()  # 测试开始时间戳
        start_strftime = time.strftime("%Y-%m-%d %H_%M_%S")    # 测试开始时间
        report_dir = self.rootdir + '\\report\\' + 'report_' + start_strftime + '\\'
        os.mkdir(report_dir)
        log_report = "run_" + start_strftime + ".log"  # 报告伴随日志
        run_log_report = report_dir + log_report
        report_file = report_dir + 'report_' + start_strftime + '_result.xlsx'   # 生成报告文件
        case_file = self.rootdir + '\\case\\' + 'interface.xlsx'     # 测试用例文件
        self.test_report = Report(report_file)  # 报告文件
        self.test_report.init_data()
        self.test_report.write_cases_data()
        # tmp_file = 'tmp.xlsx'      # 临时文件，临时保存测试源文件
        # self.op_file.copy_file(case_file, tmp_file)  # 复制case临时文件，用于还原case

        # 运行用例
        for row in range(self.start_row, self.nrows):
            is_run = self.case_data.get_is_run(row)

            # 如果需要运行
            if is_run is True:
                # 获取case运行数据
                api_name = self.case_data.get_api_name(row)
                case_id = self.case_data.get_case_id(row)
                url = self.case_data.get_url(row)
                method = self.case_data.get_method(row)
                request_data = self.case_data.get_request_data(row)
                expect_data = self.case_data.get_expect_data(row)
                headers_data = self.case_data.get_headers(row)
                cookies_data = self.case_data.get_cookies(row)
                rele_case_id = self.case_data.get_rele_case_id(row)

                # 解决依赖数据问题
                if rele_case_id is not None:
                    rele_case = ReleData(rele_case_id, row)
                    depend_key = self.case_data.get_depend_key(row)
                    depend_data = rele_case.deal_rele(depend_key)
                    request_data[depend_key] = depend_data

                # 执行case
                res = self.ru_method.run_main(method, url, request_data, headers=headers_data, cookies=cookies_data)
                self.logger.info("测试case_id: %s".center(32, '*') % case_id)

                # 断言T/F，并根据断言结果写入测试数据
                assert_status = self.re_assert.is_contain(expect_data, res.text)
                if assert_status:
                    # self.case_data.write_resp_data(row, res.text)
                    # self.case_data.write_case_status(row, "pass")
                    self.test_report.write_test_status(row, "pass")  # 写入通过状态
                    self.logger.info("测试结果: pass")
                    self.static_apis[api_name]['pass'].append(case_id)
                    self.pass_cases.append(case_id)
                else:
                    # self.case_data.write_resp_data(row, res.text)
                    # self.case_data.write_case_status(row, "fail")
                    self.test_report.write_test_status(row, "fail")  # 写入通过状态
                    self.logger.info("测试结果: fail")
                    self.logger.info("断言数据: %s" % expect_data)
                    self.static_apis[api_name]['fail'].append(case_id)
                    self.fail_cases.append(case_id)
                self.test_report.write_res_data(row, res.text)  # 写入响应值
                self.logger.info("响应码: %s" % res.status_code)
                self.logger.info("响应头: %s" % res.headers)
                self.logger.info("响应数据: %s" % res.text)
                self.logger.info("请求方式: %s" % res.request.method)
                self.logger.info("请求地址: %s" % res.request.url)
                self.logger.info("请求头: %s" % res.request.headers)
                self.logger.info("请求数据: %s" % res.request.body)
        # 统计信息
        end_time = time.time()  # 测试结束时间戳
        self.static_all['title'] = "运行结果概要统计:".center(64, '-')
        self.static_all['start_strftime'] = start_strftime
        self.static_all['end_strftime'] = time.strftime("%Y-%m-%d %H_%M_%S")  # 测试结束时间
        self.static_all['sum_time'] = "%.2f" % (end_time - start_time)  # 运行时间
        self.static_all['api_counts'] = len(list(self.api_set))  # 本次测试接口数量
        self.static_all['cases_count'] = len(self.pass_cases)+len(self.fail_cases)  # 运行的用例数
        self.static_all['pass_counts'] = len(self.pass_cases)
        self.static_all['fail_counts'] = len(self.fail_cases)
        self.static_all['pass_rate'] = ("%.2f%%" % (self.static_all['pass_counts']/self.static_all['cases_count']*100))
        self.static_all['fail_cases'] = self.fail_cases
        self.logger.info("""
                    {_title}
                    测试开始时间： {_start_strftime}
                    测试结束时间： {_end_strftime}
                    测 试  耗 时： {_sum_time}
                    测试接口总数： {_api_counts}
                    运行的用例数： {_cases_count}
                    通过的用例数： {_pass_counts}
                    失败的用例数： {_fail_counts}
                    测试通过率 ： {_pass_rate}
                    失败的用例集： {_fail_cases}
            """.format(
                _title=self.static_all['title'],
                _start_strftime=self.static_all['start_strftime'],
                _end_strftime=self.static_all['end_strftime'],
                _sum_time=self.static_all['sum_time'],
                _api_counts=self.static_all['api_counts'],
                _cases_count=self.static_all['cases_count'],
                _pass_counts=self.static_all['pass_counts'],
                _fail_counts=self.static_all['fail_counts'],
                _pass_rate=self.static_all['pass_rate'],
                _fail_cases=self.static_all['fail_cases']
                )
        )
        self.logger.info("运行接口详细统计:".center(64, '-'))
        # 子接口详细统计信息
        # {api_1:{'pass': [], 'fail': []},api_2:{'pass': [], 'fail': []}...}
        for k, v in self.static_apis.items():
            if len(v['fail']) == 0:
                fail_cases_id = None
            else:
                fail_cases_id = ",".join(v['fail'])
            self.logger.info("""
                    接口  名称： {_api_name}
                    运行用例数： {_run_cases}
                    通过用例数： {_pass_cases_counts}
                    失败用例数： {_fail_cases_counts}
                    失败用例id： {_fail_cases_id}
            """.format(
                _api_name=k,
                _run_cases=len(v['pass'])+len(v['fail']),
                _pass_cases_counts=len(v['pass']),
                _fail_cases_counts=len(v['fail']),
                _fail_cases_id=fail_cases_id
                )
            )

        # 生成报告，恢复环境
        self.op_file.copy_file(self.run_log_src, run_log_report)
        self.test_report.write_static_data(self.static_all, self.static_apis)
        # self.op_file.copy_file(case_file, report_file)
        # self.op_file.copy_file(tmp_file, case_file)
        # os.remove(tmp_file)
        self.logger.info("用例运行结束，测试停止".ljust(32, "-"))
        self.teardown()

if __name__ == "__main__":
    runtest = RunTest()
    runtest.start()
