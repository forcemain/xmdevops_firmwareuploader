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
import re
import json
import string
import zipfile
# 说明: 导入其它模块


# 说明: 获取DEVID值
def f_getdevids(binfpath):
    devids = ''

    # 注意: 读取压缩异常
    try:
        zfile = zipfile.ZipFile(binfpath, 'r')
    except Exception, e:
        pass
    else:
        for z in zfile.namelist():
            if z == 'InstallDesc':
                zdata = zfile.read(z)
                if 'DevID' in zdata:
                    devids = json.loads(zdata)['DevID']

    return devids


# 说明: 转换DEVID值
def f_convertid(dev_id):
    res_id = ''

    # 注意: DEVID格式有误
    if len(dev_id) != 24:
        return res_id
    if dev_id[5] < '5':
        res_id = dev_id[:8] + 'XXXXXXXXXXX' + dev_id[19:]
    else:
        res_id = dev_id[:8] + dev_id[8:13].replace('2','0').replace('3','1') + '0000' + dev_id[17:]

    return res_id


# 说明: 解析SVN日志
def f_note2dict(releasenote):
    date2firmware = {}
    note2firmware = {}
    start_records = False

    with open(releasenote,'r+b') as rhandler:
        for cur_line in rhandler:
            match = re.match('(\\d{4}-\\d{1,2}-\\d{1,2})\\W+([A-Z-0-9_a-z]+)', cur_line)
            if match:
                cur_date, cur_type = match.groups()
                date2firmware.update({(cur_date, cur_type): []})
                start_records = True
            if start_records:
                date2firmware[cur_date,cur_type].append(cur_line)

    for cur_key, cur_val in date2firmware.iteritems():
        add_flag = True

        if not cur_val[2:]:
            add_flag = False
        if cur_key[0] not in cur_val[2]:
            add_flag = False
        if cur_val[2][0] in string.whitespace:
            add_flag = False
        # 注意: 文件格式错误
        if not add_flag:
            continue

        change_dict = {
            'Level': None,
            'XmCloudUpgrade': None,
            'ChangeLog_SimpChinese': [],
            'ChangeLog_English': []
        }
        for cur_item in cur_val[3:]:
            cur_item = cur_item.rstrip()
            match = re.match('(Level|XmCloudUpgrade|ChangeLog_SimpChinese|ChangeLog_English)\\s*=\\s*(.*)', cur_item)
            if match:
                match_key, match_val = match.groups()
                match_key = match_key.strip()
                match_val = match_val.strip()
                if not match_val:
                    match_val = []
                if match_key == 'XmCloudUpgrade' and not match_val == '1':
                    add_flag = False
                    break
                change_dict.update({match_key: match_val})
            else:
                # 注意: 文件格式错误
                try:
                    change_dict[match_key].append(cur_item)
                except Exception, e:
                    pass

        if add_flag:
            note2firmware.update({cur_key: change_dict})

    return note2firmware


if __name__ == '__main__':
    pass
