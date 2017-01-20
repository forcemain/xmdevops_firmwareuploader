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
import colorama
# 说明: 导入其它模块


class __IPC(object):
    baseurl = ''
    include = []
    exclude = []
    update = 10
    # 说明: 在线检测时间单元(月(m)-日(d)-时(H)-分(M)-秒(S))
    udunit = 'd'
    # 说明: 更新频率时间单元
    uprate = 30
    urunit = 'S'
    svnusr = ''
    passwd = ''
    mailto = [],


class __DVR(object):
    baseurl = ''
    include = []
    exclude = []
    update = 10
    udunit = 'd'
    uprate = 30
    urunit = 'S'
    svnusr = ''
    passwd = ''
    mailto = []


class __XMJP(object):
    baseurl = ''
    include = []
    exclude = []
    update = 10
    udunit = 'd'
    uprate = 30
    urunit = 'S'
    svnusr = ''
    passwd = ''
    mailto = [],


class __JVFENG(object):
    baseurl = ''
    include = []
    exclude = []
    update = 10
    udunit = 'd'
    uprate = 30
    urunit = 'S'
    svnusr = ''
    passwd = ''
    mailto = ''


class __RSYNC(object):
    basedir = ''
    rsdir = '',
    rpath = '/usr/bin/rsync',
    ruser = '',
    raddr = '',
    rddir = 'upgrade_server',
    rpass = '/etc/rsync.password'


# 说明: 主要相关配置信息
config = {
    'rserver': {
        'rsync': __RSYNC,
    },
    'product': {
        'xmjp': __XMJP, 'ipc': __IPC, 'dvr': __DVR
    },
}
colorama.init()
rpattern = re.compile(r'(.*/)(\d{4}-\d{1,2}-\d{1,2}[^/]+)(/.*)')
