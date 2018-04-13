#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
  Copyright (C) 2015-2017 Shenzhen Auto-link world Information Technology Co., Ltd.
  All Rights Reserved

  Name: CanMsgBasic.py
  Purpose:

  Created By:    Clive Lau <liuxusheng@auto-link.com.cn>
  Created Date:  2017-12-28

  Changelog:
  Date         Desc
  2017-12-28   Created by Clive Lau
"""

# Builtin libraries
import time

# Third-party libraries
from enum import Enum, unique


@unique
class EnumMsgType(Enum):
    # 常规应用报文(Normal Communication message)
    Normal = 0
    # 网络管理报文(Network Management message)
    NM = 1
    # 诊断报文(Diagnostic message)
    Diag = 2


@unique
class EnumMsgTransmitType(Enum):
    Cycle = 0
    Event = 1
    IfActive = 2
    # Cycle and Event
    CE = 3
    # Cycle if Active
    CA = 4


@unique
class EnumMsgSignalType(Enum):
    Cycle = 0
    OnWrite = 1
    OnWriteWithRepetition = 2
    OnChange = 3
    OnChangeWithRepetition = 4
    IfActive = 5
    IfActiveWithRepetition = 6


class CanMsgBasic(object):
    """"""
    def __init__(self, name, msg_type, msg_id, transmit_type, signal_type, periodic_time, length, data):
        # 报文名称
        self._msg_name = name
        # 报文类型
        self._msg_type = msg_type
        # 报文标识符
        self._msg_id = msg_id
        # 报文发送类型
        self._msg_transmit_type = transmit_type
        # 报文信号发送类型
        self._msg_signal_type = signal_type
        # 报文周期时间
        self._msg_periodic_time = periodic_time
        # 报文长度
        self._msg_length = length
        # 报文数据
        self._msg_data = data
        # extra
        self._msg_expected_utc = time.time() + (self._msg_periodic_time / 1000)

    def get_name(self):
        return self._msg_name

    def get_type(self):
        return self._msg_type

    def get_id(self):
        return self._msg_id

    def get_transmit_type(self):
        return self._msg_transmit_type

    def get_signal_type(self):
        return self._msg_signal_type

    def get_periodic_time(self):
        return self._msg_periodic_time

    def get_expected_utc(self):
        return self._msg_expected_utc

    def set_expected_utc(self, curr_utc):
        self._msg_expected_utc = time.time() + (self._msg_periodic_time / 1000)

    def get_length(self):
        return self._msg_length

    def encode(self):
        pass

    def decode(self, *args):
        for i in range(8 if self._msg_length > 8 else self._msg_length):
            self._msg_data[i] = args[i]

    def dump(self):
        print("========== " + self.__class__.__name__ + " ==========")


if __name__ == '__main__':
    pass
