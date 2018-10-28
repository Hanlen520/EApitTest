# -*- coding: utf-8 -*-
# @Time    : 2018/5/26 14:49
# @Author  : Burrows
# @FileName: oper_json.py
"""封装操作json文件数据的方法"""

import json
import os


class OperJson:
    def __init__(self, filename=None):
        """传入json文件名，默认打开并读取该文件"""
        self.rootpath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        reqs_jsonfile = []
        if filename is None:
            reqs_jsonfile.append("request_data.json")  # 可能存在多个请求数据文件
        else:
            reqs_jsonfile.append(filename)
        self.reqs_jsonpath = self.rootpath + '/data/' + reqs_jsonfile[0]
        self.json_data = self.read_json()
        self.rele_data = "rele_data.json"  # 关联数据文件

    def read_json(self):
        """读取json文件数据"""
        with open(self.reqs_jsonpath) as fp:
            json_data = json.load(fp)
            return json_data

    def read_jsondata(self, key=None):
        """读取jsondata数据"""
        if key is None:
            return self.json_data
        else:
            return self.json_data.get(key)

    def write_data_to_jsonfile(self, data, filename):
        """将指定的数据追加写入到json文件"""
        self.reqs_jsonpath = self.rootpath + '/data/' + filename
        with open(self.reqs_jsonpath, 'r') as fr:
            src_data = json.load(fr)
        for k in data:
            src_data[k] = data[k]
        new_data = json.dumps(src_data, ensure_ascii=False, indent=2, sort_keys=True)
        # print(new_data)
        with open(self.reqs_jsonpath, 'w') as fw:
            fw.write(new_data)

    def setup_data(self):
        """初始化rele_data.json数据"""
        filename = self.rele_data
        self.rele_jsonpath = self.rootpath + '/data/' + filename
        with open(self.rele_jsonpath, 'w') as fp:
            fp.write(json.dumps({}))

if __name__ == "__main__":
    # op_json = OperJson()
    # print(op_json.read_jsondata())
    # print(op_json.read_jsondata("mock-04"))
    # op_json.write_data_to_jsonfile({"write_test": "testdata111"}, "request_headers.json")

    test_data = {'e': '5555', 'f': '6666'}
    test_data2 = {'e1': '33', 'f1': '22'}
    filename = "rele_data.json"
    op_json = OperJson(filename)
    print(op_json.read_jsondata("hehe"))
    op_json.write_data_to_jsonfile(test_data, filename)
    op_json.write_data_to_jsonfile(test_data2, filename)
    # op_json.setup_data()

