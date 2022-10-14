#!/bin/env python
# -*- encoding: utf-8 -*-
#-------------------------------------------------------------------------------
# Purpose:     txt转换成Excel
# Author:      zhoujy
# Created:     2013-05-07
# update:      2013-05-07
#-------------------------------------------------------------------------------
import os
import pandas as pd
from posixpath import abspath, dirname

#-------------------------------------------------------------------------------
# 一般来说是要先找 py 文件所在的目录
#-------------------------------------------------------------------------------
root_path = dirname(abspath(__file__))
print('\033[0;36;40m文件目录:  %s\033[0m' % root_path)

file_path = os.path.join(root_path, '11.xlsx')


def toExcel():
    list1 = [10, 20, 30, 40]
    list2 = [40, 30, 20, 10]
    col1 = "X"
    col2 = "Y"
    data = pd.DataFrame({col1: list1, col2: list2})
    data.to_excel(file_path, sheet_name='为了部落', index=False)


toExcel()
