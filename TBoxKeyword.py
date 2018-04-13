#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Copyright (C) 2015-2018 Shenzhen Auto-link world Information Technology Co., Ltd.
  All Rights Reserved

  Name: Config.py
  Purpose:

  Created By:    Clive Lau <liuxusheng@auto-link.com.cn>
  Created Date:  2017-01-01

  Changelog:
  Date         Desc
  2017-01-01   Created by Clive Lau
"""

# Builtin libraries
import os
import time

# Third-party libraries
from robot.api import logger

# Custom libraries
from TBoxCore import TBoxCore


class TBoxKeyword(object):
    def __init__(self):
        self._tag = self.__class__.__name__ + ': '
        logger.console(self._tag + "__init__ called")
        self._tbox = None

    def initialize(self, device, server, channel, baudrate):
        """ 初始化 TBox 设备

        :return:
        """
        logger.info(self._tag + "Initialize called")
        self._tbox = TBoxCore(device, server, channel, baudrate)
        self._tbox.on_create()

    def uninitialize(self):
        """ 反初始化 TBox 设备

        :return:
        """
        logger.info(self._tag + "Uninitialize called")
        self._tbox.on_destroy()

    def log_cleanup(self):
        """ 清理TBox设备log

        :return:
        """
        logger.info(self._tag + 'Cleaning log for TBox')
        TBoxCore.on_clean_log()

    def log_collection(self):
        """ 收集TBox设备log

        :return:
        """
        logger.info(self._tag + 'Collecting log for TBox')
        timestamp = time.strftime('%Y%m%d', time.localtime(time.time()))
        path = os.path.expandvars('$HOME') + '/Desktop/' + timestamp + '_Sherlock-TBox/' + 'dev_log'
        TBoxCore.on_collect_log(path)

    def wait_until_ready(self):
        """ 等待 TBox 成功连接 MQTT Broker

        :return: True if succeed to connect MQTT Broker or not
        """
        logger.info(self._tag + "Wait until ready called")
        return self._tbox.wait_until_ready()

    def request_remote_ota(self, version, addr, timeout=30):
        """ 请求远程升级

        :param timeout: 设置超时

        :return: True if succeed to configuration or not
        """
        logger.info(self._tag + "Request remote control called")
        return self._tbox.on_request_remote_ota(version, addr, timeout)

    def request_remote_control(self, item, data, timeout=30):
        """ 请求远程控制

        :param timeout: 设置超时

        :return: True if succeed to configuration or not
        """
        logger.info(self._tag + "Request remote control called")
        return self._tbox.on_request_remote_control(item, data, timeout)

    def request_remote_diagnosis(self, timeout=30):
        """ 请求远程诊断

        :param timeout: 设置超时

        :return: True if succeed to configuration or not
        """
        logger.info(self._tag + "Request remote diagnosis called")
        return self._tbox.on_request_remote_diagnosis(timeout)

    def request_remote_config(self, item, data, timeout=30):
        """ 请求远程配置

        :param item: 配置项

        :param data: 配置数据

        :param timeout: 设置超时

        :return: True if succeed to configuration or not
        """
        logger.info(self._tag + "Request remote config called")
        return self._tbox.on_request_remote_config(item, data, timeout)

    def request_can_config(self, item, data, timeout=10):
        """ 请求CAN配置

        :param item: 配置项

        :param data: 配置数据

        :param timeout: 设置超时

        :return: True if succeed to configuration or not
        """
        logger.info(self._tag + "Request CAN config called")
        return self._tbox.on_request_can_config(item, data, timeout)

    def request_can_data(self, item, timeout=10):
        """ 请求指定CAN数据

        :param item: 配置项

        :param timeout: 设置超时

        :return: Specified data
        """
        logger.info(self._tag + "Request CAN data called")
        return self._tbox.on_request_can_data(item, timeout)


if __name__ == '__main__':
    pass
