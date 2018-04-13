#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Copyright (C) 2015-2017 Shenzhen Auto-link world Information Technology Co., Ltd.
  All Rights Reserved

  Name: CanProtoDFSK.py
  Purpose:

  Created By:    Clive Lau <liuxusheng@auto-link.com.cn>
  Created Date:  2017-12-28

  Changelog:
  Date         Desc
  2017-12-28   Created by Clive Lau
"""

# Builtin libraries

# Third-party libraries

# Customized libraries
from CanMsgBasic import *
from Resource.DFSKVehicleStatus import EngineStatus
from Resource.DFSKVehicleStatus import DoorStatus
from Resource.DFSKVehicleStatus import LockStatus
from Resource.DFSKVehicleStatus import HandbrakeStatus
from Resource.DFSKVehicleStatus import DefrostStatus
from Resource.DFSKVehicleStatus import WiperStatus
from Resource.DFSKVehicleStatus import AcStatus
from Resource.DFSKVehicleStatus import GearStatus
from Resource.DFSKVehicleStatus import PepsStatus


class Tbox011(CanMsgBasic):
    """  """
    def __init__(self):
        super(Tbox011, self).__init__('TBOX_011',
                                     EnumMsgType.Normal,
                                     0x011,
                                     EnumMsgTransmitType.Cycle,
                                     EnumMsgSignalType.Cycle,
                                     10,
                                     8,
                                     ['0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00'])
        # Request BCM open or close door
        self.__control_lock = 0
        # Notice BCM silent or sound shift
        self.__look_for_car = 0
        # Request PEPS remote control of the engine
        self.__control_engine = 0
        # Request PEPS power off or on
        self.__control_power = 0
        # 控制空调标志
        self.__control_ac_flag = 0
        # 设置温度
        self.__control_temperature = 0
        # 前除霜按键
        self.__control_front_defrost = 0
        # 后除霜及后视镜加热按键
        self.__control_rear_defrost = 0
        # 关闭空调按键
        self.__control_ac = 0

    @property
    def control_lock(self):
        """ Request BCM open or close door """
        return self.__control_lock

    @property
    def look_for_car(self):
        """ Notice BCM silent or sound shift """
        return self.__look_for_car

    @property
    def control_engine(self):
        """ Request PEPS remote control of the engine """
        return self.__control_engine

    @property
    def control_power(self):
        """ Request PEPS power off or on """
        return self.__control_power

    @property
    def control_ac_flag(self):
        """ 控制空调标志 """
        return self.__control_ac_flag

    @property
    def control_temperature(self):
        """ 设置空调温度 """
        return self.__control_temperature

    @property
    def control_front_defrost(self):
        """ 控制前除霜 """
        return self.__control_front_defrost

    @property
    def control_rear_defrost(self):
        """ 控制后除霜及后视镜加热 """
        return self.__control_rear_defrost

    @property
    def control_ac_key(self):
        """ 控制空调 """
        return self.__control_ac

    def encode(self):
        # control_lock + look_for_car + control_engine + control_power
        self._msg_data[0] = hex((self.__control_lock << 0) |
                                (self.__look_for_car << 2) |
                                (self.__control_engine << 4) |
                                (self.__control_power << 6))
        # 控制空调标志 + 设置空调温度
        self._msg_data[1] = hex((self.__control_ac_flag << (8 % 8)) |
                                (self.__control_temperature << (9 % 8)))
        # 控制前除霜 + 控制后除霜及后视镜加热 + 控制空调
        self._msg_data[2] = hex((self.__control_front_defrost << (16 % 8)) |
                                (self.__control_rear_defrost << (17 % 8)) |
                                (self.__control_ac << (19 % 8)))
        return self._msg_data

    def decode(self, *args):
        super(Tbox011, self).decode()
        # Request BCM open or close door
        self.__control_lock = self._msg_data[0] & (0x3 << 0)
        # Notice BCM silent or sound shift
        self.__look_for_car = self._msg_data[0] & (0x3 << 2)
        # Request PEPS remote control of the engine
        self.__control_engine = self._msg_data[0] & (0x3 << 4)
        # Request PEPS power off or on
        self.__control_power = self._msg_data[0] & (0x3 << 6)
        # 控制空调标志
        self.__control_ac_flag = self._msg_data[1] & (0x1 << (8 % 8))
        # 设置温度
        self.__control_temperature = self._msg_data[1] & (0x7 << (9 % 8))
        # 前除霜按键
        self.__control_front_defrost = self._msg_data[2] & (0x1 << (16 % 8))
        # 后除霜及后视镜加热按键
        self.__control_rear_defrost = self._msg_data[2] & (0x1 << (17 % 8))
        # 关闭空调按键
        self.__control_ac = self._msg_data[2] & (0x1 << (18 % 8))

    def dump(self):
        super(Tbox011, self).dump()


class Sas300(CanMsgBasic):
    """  """
    def __init__(self):
        super(Sas300, self).__init__('SAS_300',
                                     EnumMsgType.Normal,
                                     0x300,
                                     EnumMsgTransmitType.Cycle,
                                     EnumMsgSignalType.Cycle,
                                     100,
                                     8,
                                     ['0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00'])
        # Message Counter
        self.__msg_counter = 0
        # 方向盘角度
        self.__steering_angle = 0

    @property
    def steering_angle(self):
        """ 方向盘角度 """
        return float(self.__steering_angle)

    @steering_angle.setter
    def steering_angle(self, value):
        """ 方向盘角度 """
        try:
            if not isinstance(value, float):
                raise AttributeError
            self.__steering_angle = 0xFFFF if value < -780.0 or value > 779.9 else value
        except AttributeError:
            print("AttributeError on steering_angle")

    def encode(self):
        # Message Counter
        self._msg_data[0] = hex(self.__msg_counter)
        # 方向盘角度
        self._msg_data[3] = hex(self.__steering_angle >> 8)
        self._msg_data[4] = hex(self.__steering_angle % 256)
        return self._msg_data

    def dump(self):
        super(Sas300, self).dump()


class Ems302(CanMsgBasic):
    """ 发动机管理系统 """
    @unique
    class ValidInvalidStatus(Enum):
        Valid = 0
        Invalid = 1

    def __init__(self):
        super(Ems302, self).__init__('EMS_302',
                                     EnumMsgType.Normal,
                                     0x302,
                                     EnumMsgTransmitType.Cycle,
                                     EnumMsgSignalType.Cycle,
                                     100,
                                     8,
                                     ['0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00'])
        # 发动机转速故障
        self.__engine_speed_error = 0
        # 节气门位置故障
        self.__throttle_position_error = 0
        # 加速踏板故障
        self.__acc_pedal_error = 0
        # 发动机转速
        self.__engine_speed = 0
        # 发动机节气门位置
        self.__engine_throttle_position = 0
        # 加速踏板位置
        self.__acc_pedal = 0

    @property
    def engine_speed(self):
        """ 发动机转速 """
        return float(self.__engine_speed * 0.25)

    @engine_speed.setter
    def engine_speed(self, value):
        """ 发动机转速 """
        try:
            if not isinstance(value, float):
                raise AttributeError
            if value < 0.0 or value > 16383.5:
                self.__engine_speed_error = Ems302.ValidInvalidStatus.Invalid.value
                self.__engine_speed = 0xFFFF
            else:
                self.__engine_speed_error = Ems302.ValidInvalidStatus.Valid.value
                self.__engine_speed = int(value / 0.25)
        except AttributeError:
            print("AttributeError on engine_speed")

    @property
    def acc_pedal(self):
        """ 加速踏板位置 """
        return float(self.__acc_pedal * 0.4)

    @acc_pedal.setter
    def acc_pedal(self, value):
        """ 加速踏板位置 """
        try:
            if not isinstance(value, float):
                raise AttributeError
            if value < 0.0 or value > 100.0:
                self.__acc_pedal_error = Ems302.ValidInvalidStatus.Invalid.value
                self.__acc_pedal = 0xFF
            else:
                self.__acc_pedal_error = Ems302.ValidInvalidStatus.Valid.value
                self.__acc_pedal = int(value / 0.4)
        except AttributeError:
            print("AttributeError on acc_pedal")

    def encode(self):
        # 发动机转速故障 + 节气门位置故障 + 加速踏板故障
        self._msg_data[0] = hex((self.__engine_speed_error << 2) |
                                (self.__throttle_position_error << 3) |
                                (self.__acc_pedal_error << 4))
        # 发动机转速
        self._msg_data[1] = hex(self.__engine_speed >> 8)
        self._msg_data[2] = hex(self.__engine_speed % 256)
        # 发动机节气门位置
        self._msg_data[3] = hex(self.__engine_throttle_position)
        # 加速踏板位置
        self._msg_data[4] = hex(self.__acc_pedal)
        return self._msg_data

    def dump(self):
        super(Ems302, self).dump()
        # print("-> EMS_EngineSpeedErr:\t\t" + Ems302.ValidInvalidStatus(self.engine_speed_error).name)
        # print("-> EMS_ThrottlePosErr:\t\t" + Ems302.ValidInvalidStatus(self.throttle_position_error).name)
        # print("-> EMS_AccPedalErr:\t\t\t" + Ems302.ValidInvalidStatus(self.acc_pedal_error).name)
        # print("-> EMS_EngineSpeed:\t\t\t" + (str(self.engine_speed) if self.__engine_speed != int('FFFF', 16) else 'Invalid'))
        # print("-> EMS_EngineThrottlePos:\t" + (str(self.engine_throttle_position) if self.__engine_throttle_position != int('FF', 16) else 'Invalid'))
        # print("-> EMS_AccPedal:\t\t\t" + (str(self.acc_pedal) if self.__acc_pedal != int('FF', 16) else 'Invalid'))


class Ems303(CanMsgBasic):
    """ 发动机管理系统 """
    @unique
    class EngineStartFlag(Enum):
        NotFinished = 0
        Finished = 1

    def __init__(self):
        super(Ems303, self).__init__('EMS_303',
                                     EnumMsgType.Normal,
                                     0x303,
                                     EnumMsgTransmitType.Cycle,
                                     EnumMsgSignalType.Cycle,
                                     100,
                                     8,
                                     ['0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00'])
        # 发动机运行状态
        self.__engine_status = 0
        # 发动机启动成功状态
        self.__engine_start_flag = 0

    @property
    def engine_status(self):
        """ 发动机运行状态 """
        return self.__engine_status

    @engine_status.setter
    def engine_status(self, status):
        """ 发动机运行状态 """
        try:
            if status not in EngineStatus.CanStatus:
                raise AttributeError
            self.__engine_status = status.value
            if status == EngineStatus.CanStatus.Running:
                self.__engine_start_flag = Ems303.EngineStartFlag.Finished.value
            else:
                self.__engine_start_flag = Ems303.EngineStartFlag.NotFinished.value
        except AttributeError:
            print("AttributeError on engine_status")

    def encode(self):
        # 发动机运行状态　+ 发动机启动成功状态
        self._msg_data[0] = hex((self.__engine_status << 0) |
                                (self.__engine_start_flag << 3))
        return self._msg_data

    def dump(self):
        super(Ems303, self).dump()


class Tcu328(CanMsgBasic):
    """ 变速箱控制单元 """
    @unique
    class ValidInvalidStatus(Enum):
        Valid = 0
        Invalid = 1

    def __init__(self):
        super(Tcu328, self).__init__('TCU_328',
                                     EnumMsgType.Normal,
                                     0x328,
                                     EnumMsgTransmitType.Cycle,
                                     EnumMsgSignalType.Cycle,
                                     100,
                                     8,
                                     ['0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00'])
        # Gear Position
        self.__gear_position_status = 0
        # Validity of Gear Position
        self.__gear_position_vd = 0
        # TCU warning for meter display
        self.__ind_fault_status = 0

    @property
    def gear_position_status(self):
        """ 变速箱档位 """
        return self.__gear_position_status

    @gear_position_status.setter
    def gear_position_status(self, status):
        """ 变速箱档位 """
        try:
            if status not in GearStatus.CanStatus:
                self.__gear_position_vd = Tcu328.ValidInvalidStatus.Invalid.value
                raise AttributeError
            self.__gear_position_status = status.value
            self.__gear_position_vd = Tcu328.ValidInvalidStatus.Valid.value
        except AttributeError:
            print("AttributeError on gear_position_status")

    def encode(self):
        # Gear Position + Gear Position VD
        self._msg_data[0] = hex((self.__gear_position_status << 0) |
                                (self.__gear_position_vd << 4))
        # IND Fault Status
        self._msg_data[2] = hex(self.__ind_fault_status << (17 % 8))
        return self._msg_data

    def dump(self):
        super(Tcu328, self).dump()


class Abs330(CanMsgBasic):
    """ 刹车防抱死系统 """
    @unique
    class SuccessFailureStatus(Enum):
        Success = 0
        Failure = 1

    @unique
    class ValidInvalidStatus(Enum):
        Valid = 0
        Invalid = 1

    def __init__(self):
        super(Abs330, self).__init__('ABS_330',
                                     EnumMsgType.Normal,
                                     0x330,
                                     EnumMsgTransmitType.Cycle,
                                     EnumMsgSignalType.Cycle,
                                     100,
                                     8,
                                     ['0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00'])
        # ABS system has detected a failure which does not allow a reliable ABS regulation and is therefore switched off
        self.__abs_failure = 0
        # ABS system has detected a heavy fault, which does not even allow a reliable electronic brake distribution and is therefore completely shut down
        self.__ebd_failure = 0
        # vehicle reference speed
        self.__vehicle_speed = 0
        # vehicle reference speed valid
        self.__vehicle_speed_valid = 0
        # every message increments the counter
        self.__message_counter = 0
        # vehicle reference speed checksum
        self.__checksum = 0

    @property
    def vehicle_speed(self):
        """ 车速 """
        return float(self.__vehicle_speed * 0.05625)

    @vehicle_speed.setter
    def vehicle_speed(self, value):
        """ 车速 """
        try:
            if not isinstance(value, float):
                raise AttributeError
            if value < 0.0 or value > 270.0:
                self.__vehicle_speed = 0
                self.__vehicle_speed_valid = Abs330.ValidInvalidStatus.Invalid.value
            else:
                self.__vehicle_speed = int(value / 0.05625)
                self.__vehicle_speed_valid = Abs330.ValidInvalidStatus.Valid.value
        except AttributeError:
            print("AttributeError on vehicle_speed")

    def encode(self):
        # ABS Failure + EBD Failure
        self._msg_data[0] = hex((self.__vehicle_speed >> 8) |
                                (self.__ebd_failure << 5) |
                                (self.__abs_failure << 6))
        # vehicle reference speed
        self._msg_data[1] = hex(self.__vehicle_speed % 256)
        # vehicle reference speed valid
        self._msg_data[2] = hex(self.__vehicle_speed_valid << (16 % 8))
        # message counter
        self._msg_data[6] = hex(self.__message_counter << (52 % 8))
        # checksum
        checksum = 0
        for idx in range(0, 7):
            checksum ^= int(self._msg_data[idx], 16)
        self._msg_data[7] = hex(checksum)
        return self._msg_data

    def dump(self):
        super(Abs330, self).dump()


class Peps341(CanMsgBasic):
    """ 无钥匙进入和启动系统 """
    def __init__(self):
        super(Peps341, self).__init__('PEPS_341',
                                      EnumMsgType.Normal,
                                      0x341,
                                      EnumMsgTransmitType.Cycle,
                                      EnumMsgSignalType.Cycle,
                                      100,
                                      8,
                                      ['0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00'])
        # 电源分配状态
        self.__power_mode = 0
        # 智能钥匙电池电量低提示
        self.__fob_low_bat_warning = 0
        # 远程模式
        self.__remote_mode = 0
        # ECU故障类型指示
        self.__escl_ecu_fail_warning = 0
        # ECU故障提示
        self.__ecu_fail_warning = 0
        # 发动机启动请求
        self.__engine_start_request = 0
        # 防盗认证结果
        self.__release_sig = 0

    @property
    def power_mode(self):
        """ PEPS电源分配状态 """
        return self.__power_mode

    @power_mode.setter
    def power_mode(self, status):
        """ PEPS电源分配状态 """
        try:
            if status not in PepsStatus.CanStatus:
                raise AttributeError
            self.__power_mode = status.value
        except AttributeError:
            print("AttributeError on power_mode")

    def encode(self):
        # 电源分配状态　+ 智能钥匙电池电量低提示 + 远程模式
        self._msg_data[0] = hex((self.__power_mode << 0) |
                                (self.__fob_low_bat_warning << 5) |
                                (self.__remote_mode << 6))
        # ESCL ECU故障类型指示
        self._msg_data[1] = hex(self.__escl_ecu_fail_warning << (8 % 8))
        # ECU故障提示
        self._msg_data[2] = hex(self.__ecu_fail_warning << (22 % 8))
        # 发动机启动请求
        self._msg_data[3] = hex(self.__engine_start_request << (24 % 8))
        # 防盗认证结果
        self._msg_data[4] = hex(self.__release_sig << (35 % 8))
        return self._msg_data

    def dump(self):
        super(Peps341, self).dump()


class Bcm350(CanMsgBasic):
    """ 车身控制器 """
    @unique
    class LampStatus(Enum):
        Off = 0
        On = 1
        NotUsed = 2
        Error = 3

    @unique
    class FindVehicleStatus(Enum):
        Invalid = 0
        NotAllowed = 1
        Executing = 2
        Finished = 3

    def __init__(self):
        super(Bcm350, self).__init__('BCM_350',
                                     EnumMsgType.Normal,
                                     0x350,
                                     EnumMsgTransmitType.Cycle,
                                     EnumMsgSignalType.Cycle,
                                     100,
                                     8,
                                     ['0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00'])
        # 近光灯工作状态
        self.__low_beam_status = 0
        # 远光灯工作状态
        self.__high_beam_status = 0
        # 前雾灯工作状态
        self.__front_fog_lamp_status = 0
        # 后雾灯工作状态
        self.__rear_fog_lamp_status = 0
        # 左转向灯信号
        self.__turn_indicator_left = 0
        # 右转向灯信号
        self.__turn_indicator_right = 0
        # 左前门状态
        self.__driver_door_status = 0
        # 右前门状态
        self.__passenger_door_status = 0
        # 左后门状态
        self.__left_rear_door_status = 0
        # 右后门状态
        self.__right_rear_door_status = 0
        # 尾门状态
        self.__tailgate_status = 0
        # 左前门门锁状态
        self.__driver_door_lock_status = 7
        # 手刹信号
        self.__handbrake_signal = 0
        # 寻车控制请求执行状态
        self.__find_car_valid = 0

    @property
    def driver_door_status(self):
        """ 左前门状态 """
        return self.__driver_door_status

    @driver_door_status.setter
    def driver_door_status(self, status):
        """ 左前门状态 """
        try:
            if status not in DoorStatus.CanStatus:
                raise AttributeError
            self.__driver_door_status = status.value
        except AttributeError:
            print("AttributeError on driver_door_status")

    @property
    def passenger_door_status(self):
        """ 右前门状态 """
        return self.__passenger_door_status

    @passenger_door_status.setter
    def passenger_door_status(self, status):
        """ 右前门状态 """
        try:
            if status not in DoorStatus.CanStatus:
                raise AttributeError
            self.__passenger_door_status = status.value
        except AttributeError:
            print("AttributeError on passenger_door_status")

    @property
    def left_rear_door_status(self):
        """ 左后门状态 """
        return self.__left_rear_door_status

    @left_rear_door_status.setter
    def left_rear_door_status(self, status):
        """ 左后门状态 """
        try:
            if status not in DoorStatus.CanStatus:
                raise AttributeError
            self.__left_rear_door_status = status.value
        except AttributeError:
            print("AttributeError on left_rear_door_status")

    @property
    def right_rear_door_status(self):
        """ 右后门状态 """
        return self.__right_rear_door_status

    @right_rear_door_status.setter
    def right_rear_door_status(self, status):
        """ 右后门状态 """
        try:
            if status not in DoorStatus.CanStatus:
                raise AttributeError
            self.__right_rear_door_status = status.value
        except AttributeError:
            print("AttributeError on right_rear_door_status")

    @property
    def tailgate_status(self):
        """ 尾门状态 """
        return self.__tailgate_status

    @tailgate_status.setter
    def tailgate_status(self, status):
        """ 尾门状态 """
        try:
            if status not in DoorStatus.CanStatus:
                raise AttributeError
            self.__tailgate_status = status.value
        except AttributeError:
            print("AttributeError on tailgate_status")

    @property
    def driver_door_lock_status(self):
        """ 左前门门锁状态 """
        return self.__driver_door_lock_status

    @driver_door_lock_status.setter
    def driver_door_lock_status(self, status):
        """ 左前门门锁状态 """
        try:
            if status not in LockStatus.CanStatus:
                raise AttributeError
            self.__driver_door_lock_status = status.value
        except AttributeError:
            print("AttributeError on driver_door_lock_status")

    @property
    def handbrake_signal(self):
        """ 手刹信号 """
        return self.__handbrake_signal

    @handbrake_signal.setter
    def handbrake_signal(self, status):
        """ 手刹信号 """
        try:
            if status not in HandbrakeStatus.CanStatus:
                raise AttributeError
            self.__handbrake_signal = status.value
        except AttributeError:
            print("AttributeError on handbrake_signal")

    def encode(self):
        # 近光灯工作状态 + 远光灯工作状态 + 前雾灯工作状态 + 后雾灯工作状态
        self._msg_data[0] = hex((self.__low_beam_status << 0) |
                                (self.__high_beam_status << 2) |
                                (self.__front_fog_lamp_status << 4) |
                                (self.__rear_fog_lamp_status << 6))
        # 左转向灯信号 + 右转向灯信号 + 左前门状态 + 右前门状态 + 左后门状态 + 右后门状态
        self._msg_data[1] = hex((self.__turn_indicator_left << (8 % 8)) |
                                (self.__turn_indicator_right << (10 % 8)) |
                                (self.__driver_door_status << (12 % 8)) |
                                (self.__passenger_door_status << (13 % 8)) |
                                (self.__left_rear_door_status << (14 % 8)) |
                                (self.__right_rear_door_status << (15 % 8)))
        # 尾门状态 + 左前门门锁状态 + 手刹信号 + 寻车控制请求执行状态
        self._msg_data[2] = hex((self.__tailgate_status << (16 % 8)) |
                                (self.__driver_door_lock_status << (17 % 8)) |
                                (self.__handbrake_signal << (20 % 8)) |
                                (self.__find_car_valid << (22 % 8)))
        return self._msg_data

    def dump(self):
        super(Bcm350, self).dump()
        # print("-> BCM_LowBeamStatus:\t\t" + EnumLampStatus(self.low_beam_status).name)
        # print("-> BCM_HighBeamStatus:\t\t" + EnumLampStatus(self.high_beam_status).name)
        # print("-> BCM_FrontFogLampStatus:\t" + EnumLampStatus(self.front_fog_lamp_status).name)
        # print("-> BCM_RearFogLampStatus:\t" + EnumLampStatus(self.rear_fog_lamp_status).name)
        # print("-> BCM_TurnIndicatorLeft:\t" + EnumLampStatus(self.turn_indicator_left).name)
        # print("-> BCM_TurnIndicatorRight:\t" + EnumLampStatus(self.turn_indicator_right).name)
        # print("-> BCM_DriverDoorStatus:\t" + EnumDoorStatus(self.driver_door_status).name)
        # print("-> BCM_PassengerDoorStatus:\t" + EnumDoorStatus(self.passenger_door_status).name)
        # print("-> BCM_LeftRearDoorStatus:\t" + EnumDoorStatus(self.left_rear_door_status).name)
        # print("-> BCM_RightRearDoorStatus:\t" + EnumDoorStatus(self.right_rear_door_status).name)
        # print("-> BCM_TailgateStatus:\t\t" + EnumDoorStatus(self.tailgate_status).name)
        # print("-> BCM_DriverDoorLockStatus:" + EnumLockStatus(self.driver_door_lock_status).name)
        # print("-> BCM_HandbrakeSignal:\t\t" + EnumHandbrakeStatus(self.handbrake_signal).name)
        # print("-> BCM_FindCarValid:\t\t" + EnumFindCarStatus(self.find_car_valid).name)


class Ems360(CanMsgBasic):
    """ 发动机管理系统 """
    def __init__(self):
        super(Ems360, self).__init__('EMS_360',
                                     EnumMsgType.Normal,
                                     0x360,
                                     EnumMsgTransmitType.Cycle,
                                     EnumMsgSignalType.Cycle,
                                     100,
                                     8,
                                     ['0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00'])
        # MIL指示灯
        self.__mil = 0
        # 防盗认证结果
        self.__release_sig = 0
        # 瞬时油耗
        self.__fuel_consumption = 0

    @property
    def fuel_consumption(self):
        """ 瞬时油耗 """
        return float(self.__fuel_consumption * 0.217)

    @fuel_consumption.setter
    def fuel_consumption(self, value):
        """ 瞬时油耗 """
        try:
            if not isinstance(value, float):
                raise AttributeError
            self.__fuel_consumption = 0xFFFF if value < 0.0 or value > 14220.878 else int(value / 0.217)
        except AttributeError:
            print("AttributeError on acc_pedal")

    def encode(self):
        # MIL指示灯
        self._msg_data[3] = hex(self.__mil << (24 % 8))
        # 防盗认证结果
        self._msg_data[5] = hex(self.__release_sig << (43 % 8))
        # 瞬时油耗
        self._msg_data[6] = hex(self.__fuel_consumption >> 8)
        self._msg_data[7] = hex(self.__fuel_consumption % 256)
        return self._msg_data

    def dump(self):
        super(Ems360, self).dump()


class Bcm365(CanMsgBasic):
    """ 车身控制器 """
    @unique
    class ValidInvalidStatus(Enum):
        Invalid = 0
        Valid = 1

    def __init__(self):
        super(Bcm365, self).__init__('BCM_365',
                                     EnumMsgType.Normal,
                                     0x365,
                                     EnumMsgTransmitType.Cycle,
                                     EnumMsgSignalType.Cycle,
                                     100,
                                     8,
                                     ['0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00'])
        # ESCL电源请求的响应信号
        self.__escl_power_resp = 0
        # ESCL解锁信号反馈
        self.__escl_unlock_feedback = 0
        # 电源继电器输出状态
        self.__power_relay_output_status = 0
        # 点火信号状态
        self.__ignition_status = 0
        # 雨刷状态
        self.__wiper_status = 0
        # 前挡风玻璃洗涤喷水信号
        self.__sprinkler_status = 0
        # 前挡风玻璃洗涤喷水信号有效标志
        self.__sprinkler_status_valid = 0
        # 后除霜状态
        self.__rear_defrost_status = 0
        # 后除霜状态有效标志位
        self.__rear_defrost_status_valid = 0
        # 外后视镜折叠状态
        self.__exterior_mirror_elec_flod_status = 0
        # 车身防盗状态
        self.__vehicle_antt_status = 0

    @property
    def rear_defrost_status(self):
        """ 后除霜状态 """
        return self.__rear_defrost_status

    @rear_defrost_status.setter
    def rear_defrost_status(self, status):
        """ 后除霜状态 """
        try:
            if status not in DefrostStatus.CanStatus:
                self.__rear_defrost_status_valid = Bcm365.ValidInvalidStatus.Invalid.value
                raise AttributeError
            self.__rear_defrost_status = status.value
            self.__rear_defrost_status_valid = Bcm365.ValidInvalidStatus.Valid.value
        except AttributeError:
            print("AttributeError on rear_defrost_status")

    @property
    def wiper_status(self):
        """ 雨刷状态 """
        return self.__wiper_status

    @wiper_status.setter
    def wiper_status(self, status):
        """ 雨刷状态 """
        try:
            if status not in WiperStatus.CanStatus:
                raise AttributeError
            self.__wiper_status = status.value
        except AttributeError:
            print("AttributeError on wiper_status")

    def encode(self):
        # ESCL电源请求的响应信号 + ESCL解锁信号反馈 + 电源继电器输出状态
        self._msg_data[0] = hex((self.__escl_power_resp << 0) |
                                (self.__escl_unlock_feedback << 2) |
                                (self.__power_relay_output_status << 4))
        # 点火信号状态　+　雨刷状态 + 前挡风玻璃洗涤喷水信号　+ 前挡风玻璃洗涤喷水信号有效标志
        self._msg_data[1] = hex((self.__ignition_status << (8 % 8)) |
                                (self.__wiper_status << (11 % 8)) |
                                (self.__sprinkler_status << (14 % 8)) |
                                (self.__sprinkler_status_valid << (15 % 8)))
        # 后除霜状态　+ 后除霜状态有效标志
        self._msg_data[2] = hex((self.__rear_defrost_status << (16 % 8)) |
                                (self.__rear_defrost_status_valid << (17 % 8)) |
                                (self.__exterior_mirror_elec_flod_status << (18 % 8)) |
                                (self.__vehicle_antt_status << (20 % 8)))
        return self._msg_data

    def dump(self):
        super(Bcm365, self).dump()


class Ac378(CanMsgBasic):
    """ 空调 """
    def __init__(self):
        super(Ac378, self).__init__('AC_378',
                                    EnumMsgType.Normal,
                                    0x378,
                                    EnumMsgTransmitType.Cycle,
                                    EnumMsgSignalType.Cycle,
                                    100,
                                    8,
                                    ['0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00'])
        # 当前环境温度(摄氏度)
        self.__outside_ambient_temperature = 0
        # 当前环境温度有效状态
        self.__outside_ambient_temperature_valid = 0
        # 空调系统中压信号
        self.__pressure_status = 0
        # 空调系统中压信号有效标志
        self.__pressure_status_valid = 0
        # 压缩机开关请求
        self.__ac_request = 0
        # 压缩机开关请求有效状态
        self.__ac_request_valid = 0
        # 鼓风机开关状态
        self.__blower_on_off_status = 0
        # 鼓风机开关状态有效标志
        self.__blower_on_off_status_valid = 0
        # 后除霜开关请求
        self.__rear_defrost_request = 0
        # 后除霜开关请求有效标志
        self.__rear_defrost_request_valid = 0
        # 按键或旋钮操作导致空调控制器状态发生变化时,需向DVD请求显示变更(此标志维持的时间为:100ms,即空调控制器只需发一次)
        self.__display_active = 0
        # AC Max状态
        self.__ac_max_mode = 0
        # 设置温度
        self.__set_temperature = 0
        # 鼓风机当前档位
        self.__blower_speed_level = 0
        # 出风模式
        self.__air_distribute_mode = 0
        # 前除霜状态
        self.__defrost_mode = 0
        # 内外循环状态
        self.__air_let_mode = 0
        # Auto模式状态
        self.__auto_mode = 0
        # Off状态
        self.__on_off_state = 0
        # Rear状态
        self.__rear_mode = 0
        # AC工作指示灯
        self.__ac_indicator = 0

    @property
    def set_temperature(self):
        """ 设置温度 """
        return float(self.__set_temperature * 0.5)

    @set_temperature.setter
    def set_temperature(self, value):
        """ 设置温度 """
        try:
            if not isinstance(value, float):
                raise AttributeError
            # self.__set_temperature = int('7F', 16) if value < 17.0 or value > 32.0 else int(value / 0.5)
            self.__set_temperature = int(value / 0.5)
        except AttributeError:
            print("AttributeError on set_temperature")

    @property
    def defrost_mode(self):
        """ 前除霜状态 """
        return self.__defrost_mode

    @defrost_mode.setter
    def defrost_mode(self, status):
        """ 前除霜状态 """
        try:
            if status not in DefrostStatus.CanStatus:
                raise AttributeError
            self.__defrost_mode = status.value
        except AttributeError:
            print("AttributeError on defrost_mode")

    @property
    def on_off_state(self):
        """ OnOff状态 """
        return self.__on_off_state

    @on_off_state.setter
    def on_off_state(self, status):
        """ OnOff状态 """
        try:
            if status not in AcStatus.CanStatus:
                raise AttributeError
            self.__on_off_state = status.value
        except AttributeError:
            print("AttributeError on on_off_state")

    def encode(self):
        # 当前环境温度(摄氏度)
        self._msg_data[0] = hex(self.__outside_ambient_temperature)
        # 当前环境温度有效状态 + 空调系统中压信号 + 空调系统中压信号有效状态 + 压缩机开关请求 + 压缩机开关请求有效状态 + 鼓风机开关状态 + 鼓风机开关状态有效状态
        self._msg_data[1] = hex((self.__outside_ambient_temperature_valid << (8 % 8)) |
                                (self.__pressure_status << (9 % 8)) |
                                (self.__pressure_status_valid << (11 % 8)) |
                                (self.__ac_request << (12 % 8)) |
                                (self.__ac_request_valid << (13 % 8)) |
                                (self.__blower_on_off_status << (14 % 8)) |
                                (self.__blower_on_off_status_valid << (15 % 8)))
        # 后除霜开关请求 + 后除霜开关请求有效标志位 + 按键或旋钮操作导致空调控制器状态发生变化 + AC MAX状态
        self._msg_data[2] = hex((self.__rear_defrost_request << (20 % 8)) |
                                (self.__rear_defrost_request_valid << (21 % 8)) |
                                (self.__display_active << (22 % 8)) |
                                (self.__ac_max_mode << (23 % 8)))
        # 设置温度
        self._msg_data[3] = hex(self.__set_temperature << (24 % 8))
        # 鼓风机当前档位 + 出风模式 + 前除霜状态
        self._msg_data[4] = hex((self.__blower_speed_level << (32 % 8)) |
                                (self.__air_distribute_mode << (36 % 8)) |
                                (self.__defrost_mode << (39 % 8)))
        # 内外循环状态 + Auto模式状态 + Off状态 + Rear状态　+ AC工作指示灯
        self._msg_data[5] = hex((self.__air_let_mode << (40 % 8)) |
                                (self.__auto_mode << (41 % 8)) |
                                (self.__on_off_state << (42 % 8)) |
                                (self.__rear_mode << (43 % 8)) |
                                (self.__ac_indicator << (44 % 8)))
        return self._msg_data

    def dump(self):
        super(Ac378, self).dump()


class Ic380(CanMsgBasic):
    """ 组合仪表 """
    def __init__(self):
        super(Ic380, self).__init__('IC_380',
                                     EnumMsgType.Normal,
                                     0x380,
                                     EnumMsgTransmitType.Cycle,
                                     EnumMsgSignalType.Cycle,
                                     100,
                                     8,
                                     ['0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00'])
        # 驾驶位安全带状态
        self.__driver_seat_belt_status = 0
        # 驾驶位安全带状态有效位
        self.__driver_seat_belt_status_valid = 0
        # 总里程
        self.__total_mileage = 0

    @property
    def total_mileage(self):
        """ 总里程 """
        return int(self.__total_mileage * 10)

    @total_mileage.setter
    def total_mileage(self, value):
        """ 总里程 """
        try:
            if not isinstance(value, int):
                raise AttributeError
            self.__total_mileage = 0xFFFF if value < 0.0 or value > 655350 else int(value / 10)
        except AttributeError:
            print("AttributeError on total_mileage")

    def encode(self):
        # 驾驶位安全带状态　+ 驾驶位安全带状态有效位
        self._msg_data[0] = hex((self.__driver_seat_belt_status << 0) |
                                (self.__driver_seat_belt_status_valid << 1))
        # 总里程
        self._msg_data[1] = hex(self.__total_mileage >> 8)
        self._msg_data[2] = hex(self.__total_mileage % 256)
        return self._msg_data

    def dump(self):
        super(Ic380, self).dump()


class Bcm401(CanMsgBasic):
    """ BCM网络管理报文 """
    @unique
    class NmStatus(Enum):
        Inactive = 0
        Active = 1

    def __init__(self):
        super(Bcm401, self).__init__('BCM_401',
                                     EnumMsgType.NM,
                                     0x401 - 0x400,
                                     EnumMsgTransmitType.Event,
                                     EnumMsgSignalType.Cycle,
                                     200,
                                     8,
                                     ['0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00'])
        # 近光灯工作状态
        self.__destination_address = 0x1
        self.__alive = 0x1
        self.__ring = 0
        self.__limp_home = 0
        self.__sleep_indication = 0
        self.__sleep_acknowledge = 0

    def encode(self):
        # 目标地址
        self._msg_data[0] = hex(self.__destination_address << 0)
        # Alive + Ring + LimpHome + SleepIndication + SleepAcknowledge
        self._msg_data[1] = hex((self.__alive << (8 % 8)) |
                                (self.__ring << (9 % 8)) |
                                (self.__limp_home << (10 % 8)) |
                                (self.__sleep_indication << (12 % 8)) |
                                (self.__sleep_acknowledge << (13 % 8)))
        return self._msg_data

    def dump(self):
        super(Bcm401, self).dump()
        # print("-> BCM_NM_DestinationAddress:" + hex(self.destination_address))
        # print("-> BCM_NM_Alive:\t\t\t " + EnumNmStatus(self.alive).name)
        # print("-> BCM_NM_Ring:\t\t\t\t " + EnumNmStatus(self.ring).name)
        # print("-> BCM_NM_LimpHome:\t\t\t " + EnumNmStatus(self.limp_home).name)
        # print("-> BCM_NM_SleepIndication:\t " + EnumNmStatus(self.sleep_indication).name)
        # print("-> BCM_NM_SleepAcknowledge:\t " + EnumNmStatus(self.sleep_acknowledge).name)


if __name__ == '__main__':
    pass
