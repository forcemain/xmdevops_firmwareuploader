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
import datetime
import multiprocessing
from multiprocessing.queues import Queue
# 说明: 导入其它模块
from ..conf.config import config
from ..libs.svnchecker import SvnChecker
from ..libs.common import convert2seconds
from .task import chk_updates_process, get_updates_process, generatedir_process


class Server(object):
    def __init__(self, info, errs):
        self.info  = info
        self.errs  = errs
        self.chkqu = Queue()
        self.genqu = Queue()
        self.wkdir = config['rserver']['rsync'].basedir
        self.ppipe = multiprocessing.Pipe(duplex=False)
        self.datas = os.path.join(self.wkdir, 'data')
        self.updir = os.path.join(self.wkdir, 'upgrade_files')

    def run(self):
        os.chdir(self.datas)

        self.generatedir()
        self.chk_updates()
        self.get_updates()

    # 说明: 检测更新固件
    def chk_updates(self, debug=False):
        self.info.info('chk_updates process is started')
        product_items = config['product'].iteritems()
        for k, v in product_items:
            self.info.info('start check {0} last updates'.format(k))
            svn = SvnChecker(
                baseurl=v.baseurl, username=v.svnusr, password=v.passwd,
                seconds=convert2seconds(v.update, v.udunit),
                include=v.include, exclude=v.exclude, debug=debug, queue=self.chkqu
            )
            sec = convert2seconds(v.uprate, v.urunit)
            p = multiprocessing.Process(
                target=chk_updates_process, args=(self, k, v, svn, sec)
            )
            p.daemon = True
            p.start()

    # 说明: 下载更新固件
    def get_updates(self, debug=False):
        self.info.info('get_updates process is started')
        while True:
            updates = self.chkqu.get()
            self.info.info('recv {0} updates from queue'.format(
                len(reduce(lambda x, y: x + y, updates.values()))
            ))
            for k, v in updates.iteritems():
                t = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                d = '{0}_{1}'.format(os.path.basename(k), t)
                if not os.path.exists(d):
                    os.makedirs(d)
                os.chdir(d)
                v.append(k)
                s = os.path.join(self.datas, d)
                p = multiprocessing.Process(
                    target=get_updates_process, args=(self, s, v)
                )
                p.daemon = True
                p.start()
                os.chdir('..')

    # 说明: 生成目录相关
    def generatedir(self, debug=False):
        self.info.info('generatedir process is started')
        p = multiprocessing.Process(
            target=generatedir_process, args=(self,)
        )
        p.daemon = True
        p.start()


    # 说明: 上传固件目录
    def upload_fiels(self, debug=False):
        pass
