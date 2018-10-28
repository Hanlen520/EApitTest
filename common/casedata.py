# -*- coding: utf-8 -*-
# @Time    : 2018/5/25 18:07
# @Author  : Burrows
# @FileName: casedata.py

""" 封装获取testcase所需单元格数据的所有方法 """
import data_mapping
from oper_excel import OperExcel
from oper_json import OperJson


class CaseData:
    def __init__(self):
        self.op_excel = OperExcel()
        self.op_json = OperJson()
        self.op_headers = OperJson("request_headers.json")  # json文件不能为空
        self.op_cookies = OperJson("request_cookies.json")  # json文件不能为空
        self.no_request_data = "no"

    def get_cases_lines(self):
        """获取excel总行数，即总用例数"""
        return self.op_excel.get_nrows()

    def get_case_id(self, row):
        """获取case_id编号"""
        col_index = data_mapping.get_case_id()
        case_id = self.op_excel.get_cell(row, col_index)
        return case_id

    def get_api_name(self, row):
        """获取接口名称"""
        col_index = data_mapping.get_interface_name()
        api_name = self.op_excel.get_cell(row, col_index)
        return api_name

    def get_url(self, row):
        """获取指定行的url值"""
        col_index = data_mapping.get_url()
        url = self.op_excel.get_cell(row, col_index)
        return url

    def get_is_run(self, row):
        """获取指定行的is_run值"""
        col_index = data_mapping.get_is_run()
        is_run = self.op_excel.get_cell(row, col_index)
        flag = None
        if is_run.lower() == "yes":
            flag = True
        else:
            flag = False
        return flag

    def get_method(self, row):
        """获取指定行的method值"""
        col_index = data_mapping.get_method()
        method = self.op_excel.get_cell(row, col_index)
        return method

    def get_if_request_data(self, row):
        """获取指定行的request_data值"""
        col_index = data_mapping.get_request_data()
        request_data = self.op_excel.get_cell(row, col_index)
        return request_data

    def get_request_data(self, row):
        """获取json文件中的请求数据value"""
        req_data = self.get_if_request_data(row)
        if req_data.lower() == self.no_request_data:
            return self.no_request_data
        else:
            request_data = self.op_json.read_jsondata(req_data)
            return request_data

    def get_expect_data(self, row):
        """获取预期值"""
        col_index = data_mapping.get_expect_value()
        expect_data = self.op_excel.get_cell(row, col_index)
        return expect_data

    def write_resp_data(self, row, resp):
        """写入响应数据,可用日志记录响应"""
        col_index = data_mapping.get_fact_value()
        self.op_excel.write_data(row, col_index, resp)

    def write_case_status(self, row, status):
        """写入用例运行结果 pass or fail,可用日志记录结果"""
        col_index = data_mapping.get_result()
        self.op_excel.write_data(row, col_index, status)

    def get_cookies(self, row):
        """获取cookie_set值yes or no,为yes则取request_cookies.json数据"""
        col_index = data_mapping.get_cookies_set()
        cookie_set = self.op_excel.get_cell(row, col_index)
        if cookie_set == "yes":
            cookie_data = self.op_cookies.read_jsondata()
            return cookie_data
        else:
            return None

    def get_headers(self, row):
        """获取headers_set值yes or no,为yes则取request_headers.json数据"""
        col_index = data_mapping.get_headers_set()
        headers_set = self.op_excel.get_cell(row, col_index)
        if headers_set == "yes":
            headers_data = self.op_headers.read_jsondata()
            return headers_data
        else:
            return None

    def get_rele_case_id(self, row):
        """获取关联的caseId"""
        col_index = data_mapping.get_rele_case_id()
        rele_caseid = self.op_excel.get_cell(row, col_index)
        if rele_caseid != "":
            return rele_caseid
        else:
            return None

    def get_rele_case_key(self, row):
        """获取关联的case所需响应字段"""
        col_index = data_mapping.get_rele_key()
        rele_case_key = self.op_excel.get_cell(row, col_index)
        return rele_case_key

    def get_depend_key(self, row):
        """获取依赖关联数据的字段"""
        col_index = data_mapping.get_depend_rele_key()
        depend_key = self.op_excel.get_cell(row, col_index)
        return depend_key

if __name__ == "__main__":
    CaseData = CaseData()
    print(CaseData.get_url(5))
    print(CaseData.get_is_run(5))
    print(CaseData.get_method(5))
    print(CaseData.get_request_data(5))
    print(CaseData.get_headers(5))
    print(CaseData.get_rele_case_id(8))
    print(CaseData.get_rele_case_key(8))
    print(CaseData.get_depend_key(8))



