#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Copyright (C) 2015-2018 Shenzhen Auto-link world Information Technology Co., Ltd.
  All Rights Reserved

  Name: TBoxCore.py
  Purpose:

  Created By:    Clive Lau <liuxusheng@auto-link.com.cn>
  Created Date:  2018-01-11

  Changelog:
  Date         Desc
  2018-01-11   Created by Clive Lau
"""

# Builtin libraries
import os
import re
import time

# Customized libraries
import Utils
from MqttComm.MqttComm import MqttComm
from CanComm.CanComm import CanComm
from DesignPattern.Singleton import Singleton

# Third-party libraries
from robot.api import logger
if Utils.is_windows_os():
    import psutil
    import win32com


class TBoxCore(Singleton):
    def __init__(self, device, server, channel, baudrate):
        self._tag = self.__class__.__name__ + ' '
        logger.info(self._tag + "__init__ called")

        self._expected_device = device
        self._mqttc = MqttComm(device, server)
        self._pcan = CanComm(channel, baudrate)

    def __del__(self):
        logger.info(self._tag + "__del__ called")

    def on_create(self):
        logger.info(self._tag + "on_create called")
        self._mqttc.on_create()
        self._pcan.on_create()

    def on_destroy(self):
        logger.info(self._tag + "on_destroy called")
        self._mqttc.on_destroy()
        self._pcan.on_destroy()
        logger.info(self._tag + "on_destroy end")

    @staticmethod
    def on_clean_log():
        if not TBoxCore.is_connected():
            raise TBoxCoreError("TBox Connect Fault")
        (status, output) = Utils.getstatusoutput("adb shell ls")
        if not status:
            try:
                result = re.findall("[a-z]*log", output)
                if result.__len__() == 0:
                    raise IndexError
                (status, output) = Utils.getstatusoutput("adb shell rm mpulog tsplog systemlog mculog")
                if not status:
                    logger.info("remove log Success!")
            except IndexError:
                logger.info("No find mpulog tsplog systemlog mculog")

    @staticmethod
    def is_connected():
        (status, output) = Utils.getstatusoutput('adb get-state')
        if not status and output.find('device') != -1:
            return True
        return False

    @staticmethod
    def get_special_log(path, obj):
        (status, output) = Utils.getstatusoutput("adb shell logcat -v time -d -b " + obj + " -f " + obj + "log")
        if not status:
            Utils.getstatusoutput("adb pull " + obj + "log " + path)

    @staticmethod
    def on_collect_log(path):
        if not TBoxCore.is_connected():
            raise TBoxCoreError("Exception on collect log")
        try:
            os.makedirs(path)
        except OSError, e:
            logger.warn(str(e))
        TBoxCore.get_special_log(path, 'mcu')
        TBoxCore.get_special_log(path, 'mpu')
        TBoxCore.get_special_log(path, 'system')
        TBoxCore.get_special_log(path, 'tsp')

    def wait_until_ready(self):
        # count = 0
        # while count < 60:
        #     if self._mqttc.is_connected:
        #         return True
        #     time.sleep(1)
        #     count += 1
        # return False
        while not self._mqttc.is_connected:
            time.sleep(1)
        return str(True)

    def on_request_can_config(self, item, data, timeout):
        """
        """
        logger.info(self._tag + "on_request_can_config called")
        return self._pcan.on_request(item, data)

    def on_request_tsp_data(self, item, timeout):
        """
        """
        logger.info(self._tag + "on_request_tsp_data called")
        return self._mqttc.on_request_tsp_data(item, timeout)

    def on_request_tsp_config(self, item, data, timeout):
        """
        """
        logger.info(self._tag + "on_request_tsp_config called")
        return self._mqttc.on_request_config(item, data, timeout)

    def on_request_remote_diagnosis(self, timeout):
        """
        """
        logger.info(self._tag + "on_request_remote_diagnosis called")
        return self._mqttc.on_request_diagnosis(timeout)

    def on_request_remote_control(self, item, data, timeout):
        """
        """
        logger.info(self._tag + "on_request_remote_control called")
        return self._mqttc.on_request_control(item, data, timeout)

    def on_request_ota_cmd(self, ver, addr, timeout):
        """
        """
        logger.info(self._tag + "on_request_ota_cmd called")
        return self._mqttc.on_request_ota_cmd(ver, addr, timeout)

    def check_vdlog(self):
        if not TBoxCore.is_connected():
            raise TBoxCoreError("Exception on collect log")
        try:
            (status, output) = Utils.getstatusoutput("adb shell ls /data")
            if not status:
                vdlog = re.findall('vdlog', output)[0]
                logger.info(self._tag + "find " + vdlog + " in /data")
        except IndexError:
            logger.info(self._tag + "Do not find vdlog!")
            logger.info(self._tag + "Create vdlog now...")
            Utils.getstatusoutput('adb shell touch /data/vdlog')
            if not status:
                logger.info(self._tag + "Create Success")


class TBoxCoreError(Exception):
    pass


if __name__ == '__main__':
    pass
