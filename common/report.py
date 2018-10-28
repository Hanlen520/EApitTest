# -*- coding: utf-8 -*-
# @Time    : 2018/6/1 15:34
# @Author  : Burrows
# @FileName: report.py
"""封装生成报告操作"""
import xlsxwriter
import data_mapping
from oper_excel import OperExcel


class Report:
    def __init__(self, report_name=None):
        if report_name is None:
            self.workbook = xlsxwriter.Workbook('report.xlsx')
        else:
            self.workbook = xlsxwriter.Workbook(report_name)
        self.worksheet = self.workbook.add_worksheet("测试总况")
        self.worksheet2 = self.workbook.add_worksheet("测试详情")
        self.op_excel = OperExcel()

    def close(self):
        self.workbook.close()

    # 写入cases数据
    def write_cases_data(self):
        nrows = self.op_excel.get_nrows()  # cases总行数
        ncols = self.op_excel.get_ncols()  # cases总列数
        for row in range(1, nrows):
            for col in range(ncols-1):
                data = self.op_excel.get_cell(row, col)
                self.write_data(row, col, data)

    # 设置写入格式
    def get_format(self, wd, option={}):
        return wd.add_format(option)

    # 设置居中格式
    def get_format_center(self, wd, num=1):
        return wd.add_format({'align': 'center', 'valign': 'vcenter', 'border': num})

    # 写数据-根据坐标
    def _write_center(self, worksheet, cl, data):
        wd = self.workbook
        return worksheet.write(cl, data, self.get_format_center(wd))

    # 写入测试用例数据
    def write_data(self, row, col, data):
        wd = self.workbook
        set_format = self.get_format_center(wd)  # 默认单元格格式
        return self.worksheet2.write(row, col, data, set_format)

    # 写入测试结果数据-根据行列索引
    def write_res_data(self, row, data):
        wd = self.workbook
        col = data_mapping.get_fact_value()
        set_format = self.get_format_center(wd)  # 默认单元格格式
        return self.worksheet2.write(row, col, data, set_format)

    # 写入测试通过状态-根据行列索引
    def write_test_status(self, row, data):
        wd = self.workbook
        col = data_mapping.get_result()
        set_format = self.get_format_center(wd)  # 默认单元格格式
        return self.worksheet2.write(row, col, data, set_format)

    def init_data(self):
        """初始化表格"""
        # 设置sheet1列和行的宽高
        self.worksheet.set_column("A:A", 15)
        self.worksheet.set_column("B:B", 20)
        self.worksheet.set_column("C:C", 20)
        self.worksheet.set_column("D:D", 20)
        self.worksheet.set_column("E:E", 20)
        self.worksheet.set_column("F:F", 20)

        self.worksheet.set_row(1, 30)
        self.worksheet.set_row(2, 30)
        self.worksheet.set_row(3, 30)
        self.worksheet.set_row(4, 30)
        self.worksheet.set_row(5, 30)
        self.worksheet.set_row(6, 30)
        self.worksheet.set_row(7, 30)
        self.worksheet.set_row(8, 30)
        self.worksheet.set_row(9, 30)

        # 设置两种格式,包含字体与背景
        define_format_H1 = self.get_format(self.workbook, {'bold': True, 'font_size': 18})
        define_format_H2 = self.get_format(self.workbook, {'bold': True, 'font_size': 14})
        define_format_H1.set_border(1)
        define_format_H2.set_border(1)
        define_format_H1.set_align("center")
        define_format_H2.set_align("center")
        define_format_H1.set_valign("vcenter")
        define_format_H2.set_valign("vcenter")
        define_format_H2.set_bg_color("gray")
        define_format_H2.set_color("#ffffff")

        # 初始化sheet1数据页
        self.worksheet.merge_range('A1:F1', '测试信息统计', define_format_H2)
        self.worksheet.merge_range('C2:F9', '图片预留位置', define_format_H1)
        self._write_center(self.worksheet, "A2", '测试开始时间')
        self._write_center(self.worksheet, "A3", '测试结束时间')
        self._write_center(self.worksheet, "A4", '测试总耗时')
        self._write_center(self.worksheet, "A5", '测试接口数')
        self._write_center(self.worksheet, "A6", '运行用例数')
        self._write_center(self.worksheet, "A7", '通过用例数')
        self._write_center(self.worksheet, "A8", '失败用例数')
        self._write_center(self.worksheet, "A9", '测试通过率')

        self.worksheet.merge_range('A11:F11', '测试接口统计', define_format_H2)
        self._write_center(self.worksheet, "A12", '接口名称')
        self._write_center(self.worksheet, "B12", '运行用例数')
        self._write_center(self.worksheet, "C12", '通过用例数')
        self._write_center(self.worksheet, "D12", '失败用例数')
        self._write_center(self.worksheet, "E12", '测试通过率')
        self._write_center(self.worksheet, "F12", '失败用例id')

        # 设置sheet2列和行的宽高
        self.worksheet2.set_column("A:A", 10)
        self.worksheet2.set_column("B:B", 12)
        self.worksheet2.set_column("C:C", 20)
        self.worksheet2.set_column("D:D", 30)
        self.worksheet2.set_column("E:E", 10)
        self.worksheet2.set_column("F:F", 10)
        self.worksheet2.set_column("G:G", 12)
        self.worksheet2.set_column("H:H", 12)
        self.worksheet2.set_column("I:I", 15)
        self.worksheet2.set_column("J:J", 10)
        self.worksheet2.set_column("K:K", 10)
        self.worksheet2.set_column("L:L", 12)
        self.worksheet2.set_column("M:M", 20)
        self.worksheet2.set_column("N:N", 30)
        self.worksheet2.set_column("O:O", 10)

        # 初始化sheet2数据页
        self._write_center(self.worksheet2, "A1", '接口名称')
        self._write_center(self.worksheet2, "B1", '测试用例编号')
        self._write_center(self.worksheet2, "C1", '测试用例描述')
        self._write_center(self.worksheet2, "D1", '请求地址')
        self._write_center(self.worksheet2, "E1", '是否运行')
        self._write_center(self.worksheet2, "F1", '请求类型')
        self._write_center(self.worksheet2, "G1", 'headers设置')
        self._write_center(self.worksheet2, "H1", 'cookies设置')
        self._write_center(self.worksheet2, "I1", '关联用例编号')
        self._write_center(self.worksheet2, "J1", '关联字段')
        self._write_center(self.worksheet2, "K1", '依赖字段')
        self._write_center(self.worksheet2, "L1", '请求数据')
        self._write_center(self.worksheet2, "M1", '预期数据')
        self._write_center(self.worksheet2, "N1", '实际数据')
        self._write_center(self.worksheet2, "O1", '测试结果')

    def write_static_data(self, static_data, api_data):
        """
        写入统计数据
        :param static_data 测试概要统计数据
        :param api_data 测试接口统计数据
        """
        # 写入测试数据-统计数据
        if static_data is not None:
            self._write_center(self.worksheet, "B2", static_data['start_strftime'])
            self._write_center(self.worksheet, "B3", static_data['end_strftime'])
            self._write_center(self.worksheet, "B4", static_data['sum_time'])
            self._write_center(self.worksheet, "B5", static_data['api_counts'])
            self._write_center(self.worksheet, "B6", static_data['cases_count'])
            self._write_center(self.worksheet, "B7", static_data['pass_counts'])
            self._write_center(self.worksheet, "B8", static_data['fail_counts'])
            self._write_center(self.worksheet, "B9", static_data['pass_rate'])

        # 写sheet1测试数据-api数据
        if api_data is not None:
            start_row = 13
            for k, v in api_data.items():
                api_name = k
                cases_counts = len(api_data[k]['pass'])+len(api_data[k]['fail'])
                pass_counts = len(api_data[k]['pass'])
                fail_counts = len(api_data[k]['fail'])
                pass_rate = ("%.2f%%" % (pass_counts/cases_counts*100))
                fail_cases = ','.join(api_data[k]['fail'])
                self._write_center(self.worksheet, "A"+str(start_row), api_name)
                self._write_center(self.worksheet, "B"+str(start_row), cases_counts)
                self._write_center(self.worksheet, "C"+str(start_row), pass_counts)
                self._write_center(self.worksheet, "D"+str(start_row), fail_counts)
                self._write_center(self.worksheet, "E"+str(start_row), pass_rate)
                self._write_center(self.worksheet, "F"+str(start_row), fail_cases)
                start_row += 1

            # 插入饼图
            self.pie()

    # 生成饼形图
    def pie(self):
        chart1 = self.workbook.add_chart({'type': 'pie'})
        chart1.add_series({
        'name':       '接口测试统计',
        'categories':'=测试总况!$A$7:$A$8',  # 饼图数据源，类目
        'values':    '=测试总况!$B$7:$B$8',  # 饼图数据源，数据
        'points': [
            {'fill': {'color': '#5ABA10'}},  # 红色
            {'fill': {'color': '#FE110E'}},  # 绿色
        ]
        })
        chart1.set_title({'name': '接口测试统计'})
        chart1.set_style(10)
        # 插入位置
        self.worksheet.insert_chart('C2', chart1, {'x_offset': 60, 'y_offset': 15})

if __name__ == "__main__":
    data_api = {
        'user': {
            'pass': ['mock-01', 'mock-02'],
            'fail': []
        },
        'mockToken': {
            'pass': ['mock-03'],
            'fail': []
        },
        'login': {
            'pass': ['mock-04', 'mock-05'],
            'fail': ['mock-06', 'mock-07']
        },
        'testrele': {
            'pass': ['mock-08', 'mock-09'],
            'fail': []
        }
    }
    data_static = {
        'title': '---------------------------运行结果概要统计:----------------------------',
        'start_strftime': '2018-05-31 15_17_09',
        'end_strftime': '2018-05-31 15_17_09',
        'sum_time': '0.07',
        'api_counts': 4,
        'cases_count': 9,
        'pass_counts': 7,
        'fail_counts': 2,
        'pass_rate': '77.78%',
        'fail_cases': ['mock-06', 'mock-07']
    }
    tr = Report()
    tr.init_data()
    tr.write_res_data(3, 'Hello')
    tr.write_res_data(4, 'Hello')
    tr.write_res_data(5, 'Hello')
    tr.write_static_data(data_static, data_api)
    tr.write_cases_data()
    tr.close()

