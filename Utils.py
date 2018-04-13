#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Copyright (C) 2015-2018 Shenzhen Auto-link world Information Technology Co., Ltd.
  All Rights Reserved

  Name: Utils.py
  Purpose:

  Created By:    Clive Lau <liuxusheng@auto-link.com.cn>
  Created Date:  2018-04-13

  Changelog:
  Date         Desc
  2018-04-13   Created by Clive Lau
"""

# Builtin libraries
import platform
import commands
import subprocess

# Third-party libraries
# from robot.api import logger

# Customized libraries


def is_windows_os():
    return platform.system() == 'Windows'


def getstatusoutput(cmd):
    output = ''
    if is_windows_os():
        try:
            status = subprocess.call(cmd)
            if not status:
                output = subprocess.check_output(cmd)
        except WindowsError:
            status = 255
            output = ''
    else:
        try:
            (status, output) = commands.getstatusoutput(cmd)
        except Exception:
            status = 255
            output = ''
    return status, output


if __name__ == '__main__':
    pass
