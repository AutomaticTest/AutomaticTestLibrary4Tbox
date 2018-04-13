#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Copyright (C) 2015-2017 Shenzhen Auto-link world Information Technology Co., Ltd.
  All Rights Reserved

  Name: DFSKVehicleStatus.py
  Purpose:

  Created By:    Clive Lau <liuxusheng@auto-link.com.cn>
  Created Date:  2017-02-05

  Changelog:
  Date         Desc
  2017-02-05   Created by Clive Lau
"""

# Builtin libraries

# Third-party libraries
from enum import Enum, unique

# Customized libraries


class EngineStatus(object):
    @unique
    class CanStatus(Enum):
        KeyOff = 0
        KeyOn = 1
        Cranking = 2
        Running = 3

    @unique
    class TspStatus(Enum):
        Unknown = 0
        KeyOff = 1
        KeyOn = 2
        Cranking = 3
        Running = 4


class DoorStatus(object):
    @unique
    class CanStatus(Enum):
        Close = 0
        Open = 1

    @unique
    class TspStatus(Enum):
        Unknown = 0
        Off = 1
        On = 2


class LockStatus(object):
    @unique
    class CanStatus(Enum):
        Default = 0
        Unlock = 1
        Locked = 2
        Error = 3
        Invalid = 4
        InvalidValue1 = 5
        InvalidValue2 = 6
        InitialValue = 7

    @unique
    class TspStatus(Enum):
        Unknown = 0
        Off = 1
        On = 2


class HandbrakeStatus(object):
    @unique
    class CanStatus(Enum):
        Invalid = 0
        Up = 1
        Down = 2
        Reserved = 3

    @unique
    class TspStatus(Enum):
        Unknown = 0
        Off = 1
        On = 2


class DefrostStatus(object):
    @unique
    class CanStatus(Enum):
        Off = 0
        On = 1

    @unique
    class TspStatus(Enum):
        Unknown = 0
        Off = 1
        On = 2


class WiperStatus(object):
    @unique
    class CanStatus(Enum):
        Stop = 0
        LowSpeed = 1
        HighSpeed = 2
        Interrupt = 3
        Wash = 4
        Reserved = 5
        SwitchFailure = 6
        Invalid = 7

    @unique
    class TspStatus(Enum):
        Unknown = 0
        Off = 1
        On = 2


class AcStatus(object):
    @unique
    class CanStatus(Enum):
        Off = 0
        On = 1

    @unique
    class TspStatus(Enum):
        Unknown = 0
        Off = 1
        On = 2


class GearStatus(object):
    @unique
    class CanStatus(Enum):
        P = 0
        R = 1
        N = 2
        D = 3
        Manual1 = 4
        Manual2 = 5
        Manual3 = 6
        Manual4 = 7
        Manual5 = 8
        Manual6 = 9
        S = 10
        Unknown = 11
        Z1 = 12
        Z2 = 13
        Z3 = 14
        Invalid = 15

    @unique
    class TspStatus(Enum):
        P = 0
        R = 1
        N = 2
        D = 3
        Manual1 = 4
        Manual2 = 5
        Manual3 = 6
        Manual4 = 7
        Manual5 = 8
        Manual6 = 9
        Manual7 = 10
        Manual8 = 11
        S = 12
        Unknown = 13
        Z1 = 14
        Z2 = 15
        Z3 = 16
        Invalid = 17


class PepsStatus(object):
    @unique
    class CanStatus(Enum):
        Default = 0
        Off = 1
        Acc = 2
        On = 3
        Start = 4
        InvalidValue1 = 5
        InvalidValue2 = 6
        Invalid = 7

    @unique
    class TspStatus(Enum):
        Default = 0
        Off = 1
        Acc = 2
        On = 3
        Start = 4
        Invalid = 5
