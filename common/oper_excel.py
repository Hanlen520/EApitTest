# -*- coding: utf-8 -*-
# @Time    : 2018/5/25 16:50
# @Author  : Burrows
# @FileName: oper_excel.py
""" 封装获取excel数据的方法 """
import os, sys

import data_mapping
import xlrd
from xlutils.copy import copy as xcopy

class OperExcel:
    def __init__(self, file_name=None, sheet_id=None):
        if file_name:
            self.file_name = file_name
            self.sheet_id = sheet_id
        else:
            root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            case_list = ["interface.xlsx"]
            self.file_name = root_dir + "/case/" + case_list[0]
            self.sheet_id = 0
        self.sheet = self.get_sheet()

    def get_sheet(self):
        """ 获取sheet对象 """
        data = xlrd.open_workbook(self.file_name)
        sheet = data.sheets()[self.sheet_id]
        return sheet

    def get_nrows(self):
        """ 获取sheet的总行数 """
        return self.sheet.nrows

    def get_ncols(self):
        """ 获取sheet的总列数 """
        return self.sheet.ncols

    def get_cell(self, row, col):
        """ 获取指定单元格的值 """
        return self.sheet.cell_value(row, col)

    def write_data(self, row, col, value):
        """ 写入数据到excel """
        read_data = xlrd.open_workbook(self.file_name)
        copy_data = xcopy(read_data)  # 复制一份workbook数据到内存
        sheet1 = copy_data.get_sheet(0)
        sheet1.write(row, col, value)
        copy_data.save(self.file_name)

    def get_col_value(self, col_id=None):
        """ 根据列号找到该列的内容 """
        if col_id is not None:
            col_data = self.sheet.col_values(col_id)
        else:
            col_data = self.sheet.col_values(data_mapping.get_case_id())  # 默认取case_id所在列的内容
        return col_data

    def get_rowid_depend_caseid(self, case_id):
        """ 根据caseId找到对应的row_index """
        row_id = 0
        col_values = self.get_col_value(data_mapping.get_case_id())
        for col_id in col_values:
            if case_id in col_id:
                break
            row_id += 1
        return row_id

    # def get_row_data(self, row_id):
    #     """ 根据行号找到该行的内容 """
    #     row_data = self.sheet.row_values(row_id)
    #     return row_data
    #
    # def get_rowdata_depend_caseid(self, case_id):
    #     """ 根据caseId找到对应的rowData """
    #     row_id = self.get_rowid_depend_caseid(case_id)
    #     row_data = self.get_row_data(row_id)
    #     return row_data

if __name__ == "__main__":
    oper_excel = OperExcel()
    print(oper_excel.get_nrows())
    print(oper_excel.get_cell(3, 5))
    print(data_mapping.get_case_id())
    print(oper_excel.get_ncols())
    print(oper_excel.get_rowid_depend_caseid("mock-05"))
