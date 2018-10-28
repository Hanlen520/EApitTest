# -*- coding: utf-8 -*-
# @Time    : 2018/5/28 9:59
# @Author  : Burrows
# @FileName: rele_data.py
"""处理关联数据"""
import json

from oper_excel import OperExcel
from casedata import CaseData
from run_method import RunMethod
from oper_json import OperJson

from jsonpath_rw import parse as j_parse


class ReleData:
    def __init__(self, case_id, row_id):
        self.op_excel = OperExcel()
        self.case_data = CaseData()
        self.ru_method = RunMethod()
        self.json_file = "rele_data.json"
        self.op_json = OperJson(self.json_file)
        self.case_id = case_id  # 需要关联的case_id
        self.row_id = row_id  # 需要关联值的case所在行下标

    def run_rele_case(self):
        """ 执行关联的case，返回响应结果数据 """
        row_id = self.op_excel.get_rowid_depend_caseid(self.case_id)
        url = self.case_data.get_url(row_id)
        method = self.case_data.get_method(row_id)
        request_data = self.case_data.get_request_data(row_id)
        headers = self.case_data.get_headers(row_id)
        cookies = self.case_data.get_cookies(row_id)
        # json化响应数据
        res = self.ru_method.run_main(method, url, request_data, headers=headers, cookies=cookies).json()
        res = json.dumps(res, ensure_ascii=False, indent=2, sort_keys=True)
        return json.loads(res)

    def parse_resp(self):
        """
            获取并解析响应结果数据，返回第一个找到的关联值
        """
        rele_key = self.case_data.get_rele_case_key(self.row_id)
        resp_data = self.run_rele_case()
        json_regu = j_parse(rele_key)
        madle = json_regu.find(resp_data)
        first_data = [k.value for k in madle][0]
        return first_data

    def deal_rele(self, depend_key):
        """
            :key 关联的字段名
            解析rele_data.json文件:
                如果关联key存在，则取其值
                如果关联key不存在，则重新运行关联case的请求，获取并解析响应结果数据，返回第一个找到的关联值,并将关联的key与value写入json文件
        """
        data = self.op_json.read_jsondata(depend_key)
        if data is None:
            depend_data = self.parse_resp()
            rele_kv = {}
            rele_kv[depend_key] = depend_data
            self.op_json.write_data_to_jsonfile(rele_kv, self.json_file)
        else:
            depend_data = data
        return depend_data

if __name__ == "__main__":
    rd = ReleData("mock-04", 8)
    print(rd.parse_resp())
    key = "name1"
    rd.deal_rele(key)
