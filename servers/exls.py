#!/bin/env python
# -*- encoding: utf-8 -*-
#-------------------------------------------------------------------------------
# Purpose:     txt转换成Excel
# Author:      zhoujy
# Created:     2013-05-07
# update:      2013-05-07
#-------------------------------------------------------------------------------
import pandas as pd


class exls:

    def toExcel(path: str, data: map, sheet_name: str):
        df = pd.DataFrame(data)
        df.to_excel(path, sheet_name=sheet_name, index=False)

    def read(path: str):
        df = pd.read_excel(path, sheet_name=None)
        return df