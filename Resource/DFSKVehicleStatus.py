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


class WindowStatus(object):
    @unique
    class CanStatus(Enum):
        Closed = 0
        Opened = 1
        Closing = 2
        Opening = 3
        Stop = 4
        ClosedNotCompletely = 5

    @unique
    class TspStatus(Enum):
        Unknown = 0
        Off = 1
        On = 2


class RoofStatus(object):
    @unique
    class CanStatus(Enum):
        TiltUp = 0
        VentArea = 1
        AntipinchInVent = 2
        FullyClose = 3
        AntipinchInPartiallySlide = 4
        PartiallySlide = 5
        FullyOpen = 6
        Uninitialized = 7

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


class TyrePressureStatus(object):
    @unique
    class CanStatus(Enum):
        Initial = 0
        _1_0_bar = 1
        _1_1_bar = 2
        _1_2_bar = 3
        _1_3_bar = 4
        _1_4_bar = 5
        _1_5_bar = 6
        _1_6_bar = 7
        _1_7_bar = 8
        _1_8_bar = 9
        _1_9_bar = 10
        _2_0_bar = 11
        _2_1_bar = 12
        _2_2_bar = 13
        _2_3_bar = 14
        _2_4_bar = 15
        _2_5_bar = 16
        _2_6_bar = 17
        _2_7_bar = 18
        _2_8_bar = 19
        _2_9_bar = 20
        _3_0_bar = 21
        _3_1_bar = 22
        _3_2_bar = 23
        _3_3_bar = 24
        _3_4_bar = 25
        _3_5_bar = 26
        _3_6_bar = 27
        _3_7_bar = 28
        _3_8_bar = 29
        _3_9_bar = 30
        _4_0_bar = 31

    @unique
    class TspStatus(Enum):
        Invalid = 0
        Initial = 90
        _1_0_bar = 100
        _1_1_bar = 110
        _1_2_bar = 120
        _1_3_bar = 130
        _1_4_bar = 140
        _1_5_bar = 150
        _1_6_bar = 160
        _1_7_bar = 170
        _1_8_bar = 180
        _1_9_bar = 190
        _2_0_bar = 200
        _2_1_bar = 210
        _2_2_bar = 220
        _2_3_bar = 230
        _2_4_bar = 240
        _2_5_bar = 250
        _2_6_bar = 260
        _2_7_bar = 270
        _2_8_bar = 280
        _2_9_bar = 290
        _3_0_bar = 300
        _3_1_bar = 310
        _3_2_bar = 320
        _3_3_bar = 330
        _3_4_bar = 340
        _3_5_bar = 350
        _3_6_bar = 360
        _3_7_bar = 370
        _3_8_bar = 380
        _3_9_bar = 390
        _4_0_bar = 400


class TyreTPMSStatus(object):
    @unique
    class CanStatus(Enum):
        Initial = 0
        Normal = 1
        system_error = 2
        low_battery_voltage = 3
        hight_tire_pressure = 4
        hight_temperature = 5
        rapid_leak = 6
        low_tire_pressure = 7

    @unique
    class TspStatus(Enum):
        Initial = 0
        Normal = 1
        system_error = 2
        low_battery_voltage = 3
        hight_tire_pressure = 4
        hight_temperature = 5
        rapid_leak = 6
        low_tire_pressure = 7
