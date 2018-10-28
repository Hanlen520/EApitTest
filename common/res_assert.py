# -*- coding: utf-8 -*-
# @Time    : 2018/5/26 10:02
# @Author  : Burrows
# @FileName: res_assert.py
"""封装断言方法"""


class ResAssert:
    def is_contain(self, expect, res):
        """判断两个字符串是否为包含关系"""
        flag = None
        if not isinstance(res, str):
            raise TypeError("bad operand type: %s" % res)
        if not isinstance(expect, str):
            raise TypeError("bad operand type: %s" % expect)
        if expect in res:
            flag = True
        else:
            flag = False
        return flag

if __name__ == "__main__":
    expect1 = "aabc"
    expect2 = "test"
    resp = "abcdetestfg"
    r = ResAssert()
    print(r.is_contain(expect1, resp))
    print(r.is_contain(expect2, resp))
