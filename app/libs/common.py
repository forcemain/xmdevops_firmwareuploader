#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#
# Authors: limanman
# 51CTOBG: http://xmdevops.blog.51cto.com/
# Purpose:
#
"""
from __future__ import absolute_import
# 说明: 导入公共模块
import chardet
import calendar
import datetime
# 说明: 导入其它模块


# 说明: 时间转换
def convert2seconds(value, unit):
    currentime = datetime.datetime.now()
    monthrange = calendar.monthrange(currentime.year, currentime.month)
    converts = {
        'm': 60*60*24*monthrange[-1],
        'd': 60*60*24,
        'H': 60*60,
        'M': 60,
        'S': 1,
    }
    return converts[unit]*value


# 说明: 编码转换
def convert2unicode(value):
    result = ''
    encode = chardet.detect(value)['encoding']
    if encode:
        result = value.decode(encode, 'replace').encode('utf-8')
    return result

