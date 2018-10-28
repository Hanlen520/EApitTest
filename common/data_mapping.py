# -*- coding: utf-8 -*-
# @Time    : 2018/5/25 16:26
# @Author  : Burrows
# @FileName: data_mapping.py

""" 对应excel中的字段名，封装获取列数据的方法 """

class DataMapping:
    interface_name = '0'  # 接口名称
    case_id = '1'  # 用例id
    case_desc = '2'  # 用例描述
    url = '3'  # 测试url
    is_run = '4'  # 是否需要运行
    method = '5'  # 请求方法
    headers_set = '6'  # headers设置
    cookies_set = '7'  # cookies设置
    rele_case_id = '8'  # 关联的case_id
    rele_key = '9'  # 关联的字段
    depend_rele_key = '10'  # 依赖关联的字段
    request_data = '11'  # 请求数据
    expect_value = '12'  # 预期值
    fact_value = '13'  # 实际值
    result = '14'  # 测试结果


# 获取interface_name列的index值
def get_interface_name():
    return int(DataMapping.interface_name)


# 获取case_id列的index值
def get_case_id():
    return int(DataMapping.case_id)


# 获取case_desc列的index值
def get_case_desc():
    return int(DataMapping.case_desc)


# 获取url列的index值
def get_url():
    return int(DataMapping.url)


# 获取is_run列的index值
def get_is_run():
    return int(DataMapping.is_run)


# 获取method列的index值
def get_method():
    return int(DataMapping.method)


# 获取headers_set列的index值
def get_headers_set():
    return int(DataMapping.headers_set)


# 获取cookies_set列的index值
def get_cookies_set():
    return int(DataMapping.cookies_set)


# 获取rele_case_id列的index值
def get_rele_case_id():
    return int(DataMapping.rele_case_id)


# 获取rele_key列的index值
def get_rele_key():
    return int(DataMapping.rele_key)


# 获取depend_rele_key列的index值
def get_depend_rele_key():
    return int(DataMapping.depend_rele_key)


# 获取request_data列的index值
def get_request_data():
    return int(DataMapping.request_data)


# 获取expect_value列的index值
def get_expect_value():
    return int(DataMapping.expect_value)


# 获取fact_value列的index值
def get_fact_value():
    return int(DataMapping.fact_value)


# 获取result列的index值
def get_result():
    return int(DataMapping.result)

if __name__ == '__main__':
    print(get_interface_name())  # 0
    print(get_fact_value())  # 13

