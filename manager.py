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
import logging.config
# 说明: 导入其它模块
from app.core.main import Server


if __name__ == '__main__':
    logging.config.fileConfig('logging.ini')
    info = logging.getLogger('info')
    errs = logging.getLogger('errs')

    server = Server(info, errs)
    server.run()
