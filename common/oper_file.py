# -*- coding: utf-8 -*- 
# __author__ = "Link.Burrows"
# __date__ = "2018-05-29 11:47 PM"
"""封装操作文件的方法"""
import os
import time
import shutil


class OperFile:
    def copy_file(self, src, dst):
        """复制文件"""
        shutil.copyfile(src, dst)

    def trunc_file(self, filename):
        """清空文件"""
        with open(filename, 'w') as fp:
            fp.truncate()

if __name__ == "__main__":
    pwd = os.path.dirname(os.path.abspath(__file__))
    filename = "test.txt"
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    newfile = "test_" + now + ".log"
    src = pwd + '\\' + filename
    dst = pwd + '\\' + newfile
    op_file = OperFile()
    op_file.copy_file(src, dst)
    op_file.trunc_file(src)
