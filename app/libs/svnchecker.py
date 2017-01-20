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
import pysvn
import urllib
import datetime
import urlparse
# 说明: 导入其它模块
from ..conf.config import colorama, rpattern


# 说明: 检测SVN指定时间段更新
class SvnChecker(object):
    def __init__(self, baseurl, username, password, seconds, include,
                 exclude, endtime=time.time(), debug=False, queue=None):
        self.debug = debug
        self.queue = queue
        self.include = include
        self.exclude = exclude
        self.baseurl = baseurl
        self.seconds = seconds
        self.endtime = endtime
        self.username = username
        self.password = password

        self.svnclient = pysvn.Client()
        # 说明: 设置验证
        self.svnclient.set_default_username(self.username)
        self.svnclient.set_default_password(self.password)
        # 说明: 回显回调
        self.svnclient.callback_notify = self.__echo_callback
        # 说明: 验证回调
        self.svnclient.callback_get_login = self.__credentials_callback

    def __echo_callback(self, event_dict):
        if not self.debug:
            return
        print event_dict

    @staticmethod
    def __credentials_callback(realm, uname, upass, is_save):
        return True, None, None, False

    # 说明: 获取更新
    def last_changed(self):
        change_files = {}
        # 说明: 开始时间
        cur = datetime.datetime.now()
        sta = cur - datetime.timedelta(seconds=self.seconds)
        sta = time.mktime(sta.timetuple())
        end = self.endtime

        revision_min = pysvn.Revision(pysvn.opt_revision_kind.date, sta)
        revision_max = pysvn.Revision(pysvn.opt_revision_kind.date, end)
        svnsummaries = self.svnclient.diff_summarize(
            self.baseurl, revision_min, self.baseurl, revision_max
        )

        for cur_item in svnsummaries:
            # 说明: 文件类型
            file_kind = pysvn.node_kind.file
            # 说明: 文件路径
            file_path = cur_item['path']
            # 说明: 节点类型
            node_kind = cur_item['node_kind']
            # 说明: 基础过滤
            if node_kind != file_kind:
                continue
            file_name = os.path.basename(file_path)
            if not file_name.endswith('.bin'):
                continue
            if any(map(lambda s: s in file_name, self.exclude)):
                continue
            if not all(map(lambda s: s in file_name, self.include)):
                continue
            # 说明: 正则过滤
            rematch = rpattern.search(file_path)
            if not rematch:
                continue
            fullurl = urlparse.urljoin(self.baseurl, file_path)
            release = urlparse.urljoin(rematch.group(1), 'ReleaseNote')
            release = urlparse.urljoin(self.baseurl, release)
            fullurl = urllib.quote(fullurl.encode('utf-8'), safe=':/')
            release = urllib.quote(release.encode('utf-8'), safe=':/')
            # print '#=> release: {0} fullurl: {1}'.format(release, fullurl)
            change_files.setdefault(release, []).append(fullurl)
        # 说明: 压入队列
        if self.queue:
            self.queue.put(change_files)
        return change_files

if __name__ == '__main__':
    pass
