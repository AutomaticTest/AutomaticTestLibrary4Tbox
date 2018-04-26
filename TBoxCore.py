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

# Third-party libraries
import psutil
import win32com
from robot.api import logger

# Customized libraries
import Utils
from MqttComm.MqttComm import MqttComm
from CanComm.CanComm import CanComm
from DesignPattern.Singleton import Singleton


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
        if TBoxCore.is_connected():
            Utils.getstatusoutput("adb shell rm mpulog tsplog systemlog mculog")

    @staticmethod
    def is_connected():
        # wmi = win32com.client.GetObject("winmgmts:")
        # for usb in wmi.InstancesOf("win32_usbcontrollerdevice"):
        #     logger.info("is_connected")
        #     if "VID_1C9E&PID_9B00" in usb.Dependent:
        #         return True
        #     return False
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
        try:
            os.makedirs(path)
        except OSError, e:
            logger.warn(str(e))
            # if e.errno == 17:
            #     shutil.rmtree(path)
            #     os.mkdir(path)
        if not TBoxCore.is_connected():
            raise TBoxCoreError("Exception on collect log")
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
        return True

    def on_request_can_config(self, item, data, timeout):
        """
        """
        logger.info(self._tag + "on_request_can_config called")
        return self._pcan.on_request(item, data)

    def on_request_can_data(self, item, timeout):
        """
        """
        logger.info(self._tag + "on_request_can_data called")
        return self._mqttc.on_request_can_data(item, timeout)

    def on_request_remote_config(self, item, data, timeout):
        """
        """
        logger.info(self._tag + "on_request_remote_config called")
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

    def on_request_remote_ota(self, version, addr, timeout):
        """
        """
        logger.info(self._tag + "on_request_remote_ota called")
        return self._mqttc.on_request_remote_ota(version, addr, timeout)

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
