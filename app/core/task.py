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
import os
import time
import wget
import shutil
import gevent
from gevent.pool import Pool
# 说明: 导入其它模块
from ..conf.config import rpattern
from ..libs.common import convert2unicode
from ..libs.firmware import f_getdevids, f_convertid, f_note2dict


# 说明: 后台检测更新固件
def chk_updates_process(self, k, v, svn, sec):
    while True:
        svn.last_changed()
        self.info.info('{0} will be checked after {1} {2}'.format(k, v.uprate, v.urunit))
        time.sleep(sec)


# 说明: 后台下载更新固件
def get_updates_process(self, src, fir):
    p = Pool(4)
    r = p.map(wget.download, fir)
    self.genqu.put((src, r))
    self.info.info('task {0} coroutine pool with {1} updates done'.format(src, len(fir)))


# 说明: 后台生成固件目录
def generatedir_process(self):
    dev_id = ''
    rs_key = ()
    rsinfo = {}
    while True:
        base_dirs, dir_files = self.genqu.get()
        self.info.info('found {0} with {1} updates'.format(base_dirs, len(dir_files)))
        rspath = os.path.join(base_dirs, 'ReleaseNote')
        # 注意: ReleaseNote不存在
        if not os.path.exists(rspath):
            self.errs.error('can not found ReleaseNote {0}'.format(rspath))
            continue
        rsinfo = f_note2dict(rspath)
        # 注意: ReleaseNote格式错
        if not rsinfo:
            dir_files.remove('ReleaseNote')
            self.errs.error('{0} with wrong format[{1}]'.format(rspath, '|'.join(dir_files)))
            shutil.rmtree(base_dirs)
            continue
        dir_files.remove('ReleaseNote')
        for f in dir_files:
            fpath = os.path.join(base_dirs, f)
            # 注意: 可能下载失败
            if not os.path.exists(fpath):
                self.errs.error('can not found {0}'.format(fpath))
                continue
            dev_id = f_convertid(f_getdevids(fpath))
            # 注意: 打包文件问题
            if not dev_id:
                self.errs.error('convert {0} dev_id with error'.format(fpath))
                continue
            # 注意: RELEAS的问题
            for key in rsinfo.keys():
                date = ''.join(key[0].split('-'))
                flag = key[1]
                if all(map(lambda s:s in fpath, (date, flag))):
                    rs_key = key
                    break
            if not rs_key:
                self.errs.error('releasenote with no record for {0}'.format(fpath))
                continue
            # 说明: 生成相关文件
            dpath = os.path.join(self.updir, dev_id)
            if not os.path.exists(dpath):
                os.makedirs(dpath)
            # 说明: 获取固件时间
            ddate = rs_key[0]
            dpath = os.path.join(dpath, ddate)
            if os.path.exists(dpath):
                continue
            os.makedirs(dpath)
            # 说明: 生成相关文件
            clang = os.path.join(dpath, 'ChangeLog_Chinese.dat')
            with open(clang, 'w+b') as fd:
                clines = rsinfo[rs_key]['ChangeLog_SimpChinese']
                clines = map(lambda s: convert2unicode(s) + os.linesep, clines)
                fd.writelines(clines)
            elang = os.path.join(dpath, 'ChangeLog_English.dat')
            with open(elang, 'w+b') as fd:
                elines = rsinfo[rs_key]['ChangeLog_English']
                elines = map(lambda s: convert2unicode(s) + os.linesep, elines)
                fd.writelines(elines)
            level = os.path.join(dpath, 'Level_{0}.dat'.format(
                rsinfo[rs_key]['Level']
            ))
            with open(level, 'w+b') as fd:
                pass
            dfirm = os.path.join(dpath, f)
            shutil.copy2(fpath, dfirm)
            self.info.info('handler {0} successfully'.format(fpath))
        # 说明: 删除原目录
        shutil.rmtree(base_dirs)

