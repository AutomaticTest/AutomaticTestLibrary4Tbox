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
from robot.api import logger

# Customized libraries
from CanMsgBasic import *
from Resource.DFSKVehicleStatus import EngineStatus
from Resource.DFSKVehicleStatus import TyrePressureStatus
from Resource.DFSKVehicleStatus import TyreTPMSStatus
from Resource.DFSKVehicleStatus import DoorStatus
from Resource.DFSKVehicleStatus import LockStatus
from Resource.DFSKVehicleStatus import HandbrakeStatus
from Resource.DFSKVehicleStatus import DefrostSwitch
from Resource.DFSKVehicleStatus import WiperStatus
from Resource.DFSKVehicleStatus import AcStatus
from Resource.DFSKVehicleStatus import GearStatus
from Resource.DFSKVehicleStatus import PepsStatus
from Resource.DFSKVehicleStatus import WindowStatus
from Resource.DFSKVehicleStatus import RoofStatus
from Resource.DFSKVehicleStatus import BlowerSpeedLevel


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
    @unique
    class ValidInvalidStatus(Enum):
        Invalid = 0
        Valid = 1

    def __init__(self):
        super(Sas300, self).__init__('SAS_300',
                                     EnumMsgType.Normal,
                                     0x300,
                                     EnumMsgTransmitType.Cycle,
                                     EnumMsgSignalType.Cycle,
                                     100,
                                     8,
                                     ['0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00'])
        # Byte 0
        # Message Counter
        self.__msg_counter = 0
        # Message Checksum
        self.__msg_checksum = 0
        # Byte 1
        # 方向盘角度有效位
        self.__steering_angle_valid = 0
        # 校准状态
        self.__calibrated_status = 0
        # trimming_status
        self.__trimming_status = 0
        # inter_st_flags
        self.__inter_st_flags = 0
        # 方向盘角度速率
        self.__steering_angle_speed = 0
        # 方向盘角度
        self.__steering_angle = 0

    @property
    def steering_angle(self):
        """ 方向盘角度 """
        return (self.__steering_angle * 0.1) - 780

    @steering_angle.setter
    def steering_angle(self, value):
        """ 方向盘角度 """
        try:
            self.__steering_angle_valid = Sas300.ValidInvalidStatus.Invalid.value
            self.__steering_angle = 0xFFFF
            if not isinstance(value, float):
                raise AttributeError
            if value >= -780.0 or value < 780.0:
                self.__steering_angle_valid = Sas300.ValidInvalidStatus.Valid.value
                self.__steering_angle = int((value + 780) * 10)
        except AttributeError:
            logger.error("AttributeError on steering_angle")

    def encode(self):
        # Message Counter + Message Checksum
        self._msg_data[0] = hex((self.__msg_counter << 0) |
                                (self.__msg_checksum << 4))
        # 方向盘角度有效位 + 校准状态 + trimming_status + inter_st_flags
        self._msg_data[1] = hex((self.__steering_angle_valid << (8 % 8)) |
                                (self.__calibrated_status << (9 % 8)) |
                                (self.__trimming_status << (10 % 8)) |
                                (self.__inter_st_flags << (11 % 8)))
        # 方向盘角度速率
        self._msg_data[2] = hex(self.__steering_angle_speed << (16 % 8))
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
        # Byte 0
        # 制动踏板状态
        self.__brake_pedal_status = 0
        # 发动机转速故障
        self.__engine_speed_error = 0
        # 节气门位置故障
        self.__throttle_position_error = 0
        # 加速踏板故障
        self.__acc_pedal_error = 0
        # 进气温度传感器故障
        self.__intake_air_temp_sensor_error = 0
        # 刹车灯状态
        self.__brake_lamp_status = 0
        # 刹车灯状态有效
        self.__brake_lamp_status_valid = 0
        # Byte 2
        # 发动机转速
        self.__engine_speed = 0
        # Byte 3
        # 发动机节气门位置
        self.__engine_throttle_position = 0
        # Byte 4
        # 加速踏板位置
        self.__acc_pedal = 0
        # Byte 5
        # 怠速状态
        self.__idle_speed_status = 0
        # Byte 6
        # 进气温度
        self.__intake_air_temp = 0

    @property
    def engine_speed(self):
        """ 发动机转速 """
        return self.__engine_speed * 0.25

    @engine_speed.setter
    def engine_speed(self, value):
        """ 发动机转速 """
        try:
            self.__engine_speed_error = Ems302.ValidInvalidStatus.Invalid.value
            self.__engine_speed = 0xFFFF
            if not isinstance(value, int):
                raise AttributeError
            if value >= 0 or value < 16384:
                self.__engine_speed_error = Ems302.ValidInvalidStatus.Valid.value
                self.__engine_speed = int(value / 0.25)
        except AttributeError:
            logger.error("AttributeError on engine_speed")

    @property
    def acc_pedal(self):
        """ 加速踏板位置 """
        return self.__acc_pedal * 0.4

    @acc_pedal.setter
    def acc_pedal(self, value):
        """ 加速踏板位置 """
        try:
            self.__acc_pedal_error = Ems302.ValidInvalidStatus.Invalid.value
            self.__acc_pedal = 0xFF
            if not isinstance(value, float):
                raise AttributeError
            if value >= 0.0 or value <= 100.0:
                self.__acc_pedal_error = Ems302.ValidInvalidStatus.Valid.value
                self.__acc_pedal = int(value / 0.4)
        except AttributeError:
            logger.error("AttributeError on acc_pedal")

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
        # Byte 0
        # 发动机运行状态
        self.__engine_status = 0
        # 发动机启动成功状态
        self.__engine_start_flag = 0
        # Engine fuel cut off status
        self.__fuel_cut_off_status = 0
        # Driving cycle detection
        self.__detect_driving_cycle = 0
        # Byte 5
        # 升档提示
        self.__gear_up = 0
        # 降档提示
        self.__gear_down = 0
        # 目标档位
        self.__target_gear = 0
        # Byte 6
        # 当前档位
        self.__curr_gear = 0

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
            logger.error("AttributeError on engine_status")

    def encode(self):
        # 发动机运行状态　+ 发动机启动成功状态 + Engine fuel cut off status + Driving cycle detection
        self._msg_data[0] = hex((self.__engine_status << 0) |
                                (self.__engine_start_flag << 3) |
                                (self.__fuel_cut_off_status << 4) |
                                (self.__detect_driving_cycle << 6))
        # 升档提示 + 降档提示 + 目标档位
        self._msg_data[5] = hex((self.__gear_up << (42 % 8)) |
                                (self.__gear_down << (43 % 8)) |
                                (self.__target_gear << (44 % 8)))
        # 当前档位
        self._msg_data[6] = hex((self.__curr_gear << (52 % 8)))
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
        # TCU request MIL on
        self.__tcu_mil_status = 0
        # TCU request AC state fixed or not
        self.__tcu_ac_fix_state = 0
        # TCU允许SBW换挡标志位
        self.__tcu_gear_shift_allowed = 0
        # "Invalid Value=0xFF Vehicle Speed caculated by TCU"
        self.__tcu_veh_speed_value = 0
        # TCU request FAN on（high speed）
        self.__tcu_cooling_fan_rq = 0
        # TCU warning for meter display
        self.__tcu_ind_fault_status = 0
        # Winter Mode Fault
        self.__tcu_winter_mode_fault = 0
        # Winter Mode
        self.__tcu_winter_mode_status = 0
        # TCU request AC off
        self.__tcu_ac_off_rq = 0
        # Clutch status（when the transmission is VT5, the signal  repesents DNR clutch state.）
        self.__tcu_clutch_status = 0
        # Invalid Value=0xFF Transmission temperature
        self.__tcu_temp_value = 0
        # Max engine speed limited value
        self.__tcu_engspd_maxlimt_value = 0
        # Request max engine speed limit
        self.__tcu_engspd_maxlmit_rq = 0
        # TCU is in emergency mode or not
        self.__tcu_emerg_mode_status = 0
        # Cruise Control Status
        self.__tcu_cruise_control_status = 0

        self.__tcu_counter_msg_2 = 0
        # 校验和
        self.__tcu_checksum_msg_2 = 0

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
            logger.error("AttributeError on gear_position_status")

    def encode(self):
        # Gear Position + Gear Position VD
        self._msg_data[0] = hex((self.__gear_position_status << 0) |
                                (self.__gear_position_vd << 4) |
                                (self.__tcu_mil_status << 5) |
                                (self.__tcu_ac_fix_state << 6) |
                                (self.__tcu_gear_shift_allowed << 7))
        self._msg_data[1] = hex((self.__tcu_veh_speed_value << (8 % 8)))
        # IND Fault Status
        self._msg_data[2] = hex((self.__tcu_cooling_fan_rq << (16 % 8)) |
                                (self.__tcu_ind_fault_status << (17 % 8)) |
                                (self.__tcu_winter_mode_fault << (18 % 8)) |
                                (self.__tcu_winter_mode_status << (19 % 8)) |
                                (self.__tcu_ac_off_rq << (20 % 8)) |
                                (self.__tcu_clutch_status << (21 % 8)))
        self._msg_data[3] = hex(self.__tcu_temp_value << (24 % 8))
        self._msg_data[4] = hex(self.__tcu_engspd_maxlimt_value << (32 % 8))
        self._msg_data[5] = hex((self.__tcu_engspd_maxlmit_rq << (40 % 8)) |
                                (self.__tcu_emerg_mode_status << (41 % 8)) |
                                (self.__tcu_cruise_control_status << (42 % 8)))
        self._msg_data[6] = hex(self.__tcu_counter_msg_2 << (52 % 8))
        self._msg_data[7] = hex(self.__tcu_checksum_msg_2 << (56 % 8))
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
        # Byte 0
        # indicates ABS intervention active
        self.__abs_active = 0
        # ABS system has detected a failure which does not allow a reliable ABS regulation and is therefore switched off
        self.__abs_failure = 0
        # ABS system has detected a heavy fault, which does not even allow a reliable electronic brake distribution and is therefore completely shut down
        self.__ebd_failure = 0
        # Byte 1
        # vehicle reference speed
        self.__vehicle_speed = 0
        # Byte 2
        # vehicle reference speed valid
        self.__vehicle_speed_valid = 0
        # Indicates BLS Valid
        self.__bls_active_valid = 0
        # Byte 3
        # this signal indicates if HBB is active or not
        self.__hbb_intervention = 0
        # this signal indicates the status of HBB
        self.__hbb_status = 0
        # Indicating brake pedal actived by driver or not
        self.__bls_active = 0
        # Byte 4
        # 制动主缸压力
        self.__mas_cyl_brake_pressure = 0
        # Byte 6
        # every message increments the counter
        self.__message_counter = 0
        # Byte 7
        # vehicle reference speed checksum
        self.__checksum = 0

    @property
    def vehicle_speed(self):
        """ 车速 """
        return self.__vehicle_speed * 0.05625

    @vehicle_speed.setter
    def vehicle_speed(self, value):
        """ 车速 """
        try:
            self.__vehicle_speed = 0x1FFF
            self.__vehicle_speed_valid = Abs330.ValidInvalidStatus.Invalid.value
            if not isinstance(value, int):
                raise AttributeError
            if value >= 0 or value <= 270:
                self.__vehicle_speed = int(value / 0.05625)
                self.__vehicle_speed_valid = Abs330.ValidInvalidStatus.Valid.value
        except AttributeError:
            logger.error("AttributeError on vehicle_speed")

    def encode(self):
        # ABS intervention active + ABS Failure + EBD Failure
        self._msg_data[0] = hex(((self.__vehicle_speed >> 8) << 0) |
                                (self.__ebd_failure << 5) |
                                (self.__abs_failure << 6) |
                                (self.__abs_active << 7))
        # vehicle reference speed
        self._msg_data[1] = hex(self.__vehicle_speed & 0xFF)
        # vehicle reference speed valid
        self._msg_data[2] = hex((self.__vehicle_speed_valid << (16 % 8)) |
                                (self.__bls_active_valid << (17 % 8)))
        # hbb_intervention + hbb_status + bls_active
        self._msg_data[3] = hex((self.__hbb_intervention << (28 % 8)) |
                                (self.__hbb_status << (29 % 8)) |
                                (self.__bls_active << (31 % 8)))
        # 制动主缸压力
        self._msg_data[4] = hex((self.__mas_cyl_brake_pressure << (32 % 8)))
        # message counter
        self._msg_data[6] = hex(self.__message_counter << (52 % 8))
        # checksum
        # checksum = 0
        # for idx in range(0, 7):
        #     checksum ^= int(self._msg_data[idx], 16)
        # self._msg_data[7] = hex(checksum)
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
        # Byte 0
        # 电源分配状态
        self.__power_mode = 0
        # 启动时不在P档提示(AT/DCT车型)
        self.__not_p_warning = 0
        # 启动时不在N档提示(AMT车型)
        self.__not_n_warning = 0
        # 智能钥匙电池电量低提示
        self.__fob_low_bat_warning = 0
        # 远程模式
        self.__remote_mode = 0
        # Byte 1
        # ECU故障类型指示
        self.__escl_ecu_fail_warning = 0
        # PEPS智能钥匙配对状态(预留)
        self.__fob_pairing_status = 0
        # 启动按钮故障提示
        self.__ssb_fail_warning = 0
        # PE锁车时电源未关提示
        self.__dr_lock_no_pwr_off_ind = 0
        # PE锁车时条件不满足提示(门开)
        self.__dr_lock_dr_opened_ind = 0
        # PE锁车时钥匙在车内提示
        self.__dr_lock_sk_rmndr_ind = 0
        # ECU故障提示
        self.__ecu_fail_warning = 0
        # 发动机启动请求
        self.__engine_start_request = 0
        # 防盗认证结果
        self.__release_sig = 0

    @property
    def peps_power_status(self):
        """ PEPS电源分配状态 """
        return self.__power_mode

    @peps_power_status.setter
    def peps_power_status(self, status):
        """ PEPS电源分配状态 """
        try:
            if status not in PepsStatus.CanStatus:
                raise AttributeError
            self.__power_mode = status.value
        except AttributeError:
            logger.error("AttributeError on power_mode")

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
        # Byte 0
        # 近光灯工作状态
        self.__low_beam_status = 0
        # 远光灯工作状态
        self.__high_beam_status = 0
        # 前雾灯工作状态
        self.__front_fog_lamp_status = 0
        # 后雾灯工作状态
        self.__rear_fog_lamp_status = 0
        # Byte 1
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
        # Byte 2
        # 后备箱状态
        self.__tailgate_status = 0
        # 左前门门锁状态
        self.__driver_door_lock_status = 7
        # 手刹状态
        self.__handbrake_signal = 0
        # 寻车控制请求执行状态
        self.__find_car_valid = 0
        # Byte 3
        # 引擎盖状态
        self.__hood_status = 0

    @property
    def lf_door_status(self):
        """ 左前门状态 """
        return self.__driver_door_status

    @lf_door_status.setter
    def lf_door_status(self, status):
        """ 左前门状态 """
        try:
            if status not in DoorStatus.CanStatus:
                raise AttributeError
            self.__driver_door_status = status.value
        except AttributeError:
            logger.error("AttributeError on lf_door_status")

    @property
    def rf_door_status(self):
        """ 右前门状态 """
        return self.__passenger_door_status

    @rf_door_status.setter
    def rf_door_status(self, status):
        """ 右前门状态 """
        try:
            if status not in DoorStatus.CanStatus:
                raise AttributeError
            self.__passenger_door_status = status.value
        except AttributeError:
            logger.error("AttributeError on rf_door_status")

    @property
    def lr_door_status(self):
        """ 左后门状态 """
        return self.__left_rear_door_status

    @lr_door_status.setter
    def lr_door_status(self, status):
        """ 左后门状态 """
        try:
            if status not in DoorStatus.CanStatus:
                raise AttributeError
            self.__left_rear_door_status = status.value
        except AttributeError:
            logger.error("AttributeError on lr_door_status")

    @property
    def rr_door_status(self):
        """ 右后门状态 """
        return self.__right_rear_door_status

    @rr_door_status.setter
    def rr_door_status(self, status):
        """ 右后门状态 """
        try:
            if status not in DoorStatus.CanStatus:
                raise AttributeError
            self.__right_rear_door_status = status.value
        except AttributeError:
            logger.error("AttributeError on rr_door_status")

    @property
    def trunk_door_status(self):
        """ 后备箱状态 """
        return self.__tailgate_status

    @trunk_door_status.setter
    def trunk_door_status(self, status):
        """ 后备箱状态 """
        try:
            if status not in DoorStatus.CanStatus:
                raise AttributeError
            self.__tailgate_status = status.value
        except AttributeError:
            logger.error("AttributeError on trunk_door_status")

    @property
    def lock_door_status(self):
        """ 左前门门锁状态 """
        return self.__driver_door_lock_status

    @lock_door_status.setter
    def lock_door_status(self, status):
        """ 左前门门锁状态 """
        try:
            if status not in LockStatus.CanStatus:
                raise AttributeError
            self.__driver_door_lock_status = status.value
        except AttributeError:
            logger.error("AttributeError on lock_door_status")

    @property
    def handbrake_status(self):
        """ 手刹状态 """
        return self.__handbrake_signal

    @handbrake_status.setter
    def handbrake_status(self, status):
        """ 手刹状态 """
        try:
            if status not in HandbrakeStatus.CanStatus:
                raise AttributeError
            self.__handbrake_signal = status.value
        except AttributeError:
            logger.error("AttributeError on handbrake_status")

    @property
    def hood_status(self):
        """ 引擎盖状态 """
        return self.__hood_status

    @hood_status.setter
    def hood_status(self, status):
        """ 引擎盖状态 """
        try:
            if status not in DoorStatus.CanStatus:
                raise AttributeError
            self.__hood_status = status.value
        except AttributeError:
            logger.error("AttributeError on hood_status")

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
        # 引擎盖状态
        self._msg_data[3] = hex((self.__hood_status << (27 % 8)))
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
            logger.error("AttributeError on acc_pedal")

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
        # 左前车窗状态
        self.__lf_window_status = 0
        # 右前车窗状态
        self.__rf_window_status = 0
        # 左后车窗状态
        self.__lr_window_status = 0
        # 右后车窗状态
        self.__rr_window_status = 0
        # 天窗状态
        self.__roof_window_status = 0

    @property
    def rear_defrost_switch(self):
        """ 空调后除霜开关状态 """
        return self.__rear_defrost_status

    @rear_defrost_switch.setter
    def rear_defrost_switch(self, status):
        """ 空调后除霜开关状态 """
        try:
            if status not in DefrostSwitch.CanStatus:
                self.__rear_defrost_status_valid = Bcm365.ValidInvalidStatus.Invalid.value
                raise AttributeError
            self.__rear_defrost_status = status.value
            self.__rear_defrost_status_valid = Bcm365.ValidInvalidStatus.Valid.value
        except AttributeError:
            logger.error("AttributeError on rear_defrost_switch")

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
            logger.error("AttributeError on wiper_status")

    @property
    def lf_window_status(self):
        """ 左前车窗状态 """
        return self.__lf_window_status

    @lf_window_status.setter
    def lf_window_status(self, status):
        """ 左前车窗状态 """
        try:
            if status not in WindowStatus.CanStatus:
                raise AttributeError
            self.__lf_window_status = status.value
        except AttributeError:
            logger.error("AttributeError on lf_window_status")

    @property
    def rf_window_status(self):
        """ 右前车窗状态 """
        return self.__rf_window_status

    @rf_window_status.setter
    def rf_window_status(self, status):
        """ 右前车窗状态 """
        try:
            if status not in WindowStatus.CanStatus:
                raise AttributeError
            self.__rf_window_status = status.value
        except AttributeError:
            logger.error("AttributeError on rf_window_status")

    @property
    def lr_window_status(self):
        """ 左后车窗状态 """
        return self.__lr_window_status

    @lr_window_status.setter
    def lr_window_status(self, status):
        """ 左后车窗状态 """
        try:
            if status not in WindowStatus.CanStatus:
                raise AttributeError
            self.__lr_window_status = status.value
        except AttributeError:
            logger.error("AttributeError on lr_window_status")

    @property
    def rr_window_status(self):
        """ 右后车窗状态 """
        return self.__rr_window_status

    @rr_window_status.setter
    def rr_window_status(self, status):
        """ 右后车窗状态 """
        try:
            if status not in WindowStatus.CanStatus:
                raise AttributeError
            self.__rr_window_status = status.value
        except AttributeError:
            logger.error("AttributeError on rr_window_status")

    @property
    def roof_window_status(self):
        """ 天窗状态 """
        return self.__roof_window_status

    @roof_window_status.setter
    def roof_window_status(self, status):
        """ 天窗状态 """
        try:
            if status not in RoofStatus.CanStatus:
                raise AttributeError
            self.__roof_window_status = status.value
        except AttributeError:
            logger.error("AttributeError on roof_window_status")

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
        # 左前车窗状态 + 右前车窗状态
        self._msg_data[3] = hex(((self.__roof_window_status >> 1) << (24 % 8)) |
                                (self.__lf_window_status << (26 % 8)) |
                                (self.__rf_window_status << (29 % 8)))
        # 左后车窗状态 + 右后车窗状态 + 天窗状态
        self._msg_data[4] = hex((self.__lr_window_status << (33 % 8)) |
                                (self.__rr_window_status << (36 % 8)) |
                                ((self.__roof_window_status & 0x1) << (39 % 8)))
        return self._msg_data

    def dump(self):
        super(Bcm365, self).dump()


class Bcm383(CanMsgBasic):
    """ 车轮胎压传感器、胎压、温度 """
    def __init__(self):
        super(Bcm383, self).__init__('BCM_383',
                                     EnumMsgType.Normal,
                                     0x383,
                                     EnumMsgTransmitType.Cycle,
                                     EnumMsgSignalType.Cycle,
                                     100,
                                     8,
                                     ['0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00'])
        # 左前车轮胎压传感器状态
        self.__lf_tpms_status = 0
        # 左前车轮胎压
        self.__lf_tyre_pressure = 0
        # 左前车轮温度
        self.__lf_tyre_temperature = 0
        # 右前车轮胎压传感器状态
        self.__rf_tpms_status = 0
        # 右前车轮胎压
        self.__rf_tyre_pressure = 0
        # 右前车轮温度
        self.__rf_tyre_temperature = 0
        # 左后车轮胎压传感器状态
        self.__lr_tpms_status = 0
        # 左后车轮胎压
        self.__lr_tyre_pressure = 0
        # 左后车轮温度
        self.__lr_tyre_temperature = 0
        # 右后车轮胎压传感器状态
        self.__rr_tpms_status = 0
        # 右后车轮胎压
        self.__rr_tyre_pressure = 0
        # 右后车轮温度
        self.__rr_tyre_temperature = 0

    @property
    def lf_tpms_status(self):
        """ 左前车轮胎压传感器状态 """
        return self.__lf_tpms_status

    @lf_tpms_status.setter
    def lf_tpms_status(self, status):
        """ 左前车轮胎压传感器状态 """
        try:
            if status not in TyreTPMSStatus.CanStatus:
                raise AttributeError
            self.__lf_tpms_status = status.value
        except AttributeError:
            logger.error("AttributeError on lf_tpms_status")

    @property
    def lf_tire_pressure(self):
        """ 左前车轮胎压 """
        return self.__lf_tyre_pressure * 0.1 + 0.9

    @lf_tire_pressure.setter
    def lf_tire_pressure(self, status):
        """ 左前车轮胎压 """
        try:
            if status not in TyrePressureStatus.CanStatus:
                raise AttributeError
            self.__lf_tyre_pressure = status.value
        except AttributeError:
            logger.error("AttributeError on lf_tyre_pressure")

    @property
    def rf_tire_pressure(self):
        """ 右前车轮胎压 """
        return self.__rf_tyre_pressure * 0.1 + 0.9

    @rf_tire_pressure.setter
    def rf_tire_pressure(self, status):
        """ 右前车轮胎压 """
        try:
            if status not in TyrePressureStatus.CanStatus:
                raise AttributeError
            self.__rf_tyre_pressure = status.value
        except AttributeError:
            logger.error("AttributeError on rf_tyre_pressure")

    @property
    def lr_tire_pressure(self):
        """ 左前车轮胎压 """
        return self.__lr_tyre_pressure * 0.1 + 0.9

    @lr_tire_pressure.setter
    def lr_tire_pressure(self, status):
        """ 左前车轮胎压 """
        try:
            if status not in TyrePressureStatus.CanStatus:
                raise AttributeError
            self.__lr_tyre_pressure = status.value
        except AttributeError:
            logger.error("AttributeError on lr_tyre_pressure")

    @property
    def rr_tire_pressure(self):
        """ 右后车轮胎压 """
        return self.__rr_tyre_pressure * 0.1 + 0.9

    @rr_tire_pressure.setter
    def rr_tire_pressure(self, status):
        """ 右后车轮胎压 """
        try:
            if status not in TyrePressureStatus.CanStatus:
                raise AttributeError
            self.__rr_tyre_pressure = status.value
        except AttributeError:
            logger.error("AttributeError on rr_tyre_pressure")

    def encode(self):
        # 左前车轮胎压传感器状态、左前车轮胎压
        self._msg_data[0] = hex((self.__lf_tpms_status << 0) |
                                (self.__lf_tyre_pressure << 3))
        # 左前车轮温度
        self._msg_data[1] = hex((self.__lf_tyre_temperature << (8 % 8)))

        # 右前车轮胎压传感器状态、右前车轮胎压
        self._msg_data[2] = hex((self.__rf_tpms_status << (16 % 8)) |
                                (self.__rf_tyre_pressure << (19 % 8)))
        # 右前车轮碾温度
        self._msg_data[3] = hex((self.__rf_tyre_temperature << (24 % 8)))

        # 左后车轮胎压传感器状态、左前车轮胎压
        self._msg_data[4] = hex((self.__lr_tpms_status << (32 % 8)) |
                                (self.__lr_tyre_pressure << (35 % 8)))
        # 左后车轮温度
        self._msg_data[5] = hex((self.__lr_tyre_temperature << (40 % 8)))

        # 右后车轮胎压传感器状态、右前车轮胎压
        self._msg_data[6] = hex((self.__rr_tpms_status << (48 % 8)) |
                                (self.__rr_tyre_pressure << (51 % 8)))
        # 右后车轮碾温度
        self._msg_data[7] = hex((self.__rr_tyre_temperature << (56 % 8)))
        return self._msg_data

    def dump(self):
        super(Bcm383, self).dump()


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
        # Byte 0
        # 当前环境温度(摄氏度)
        self.__outside_ambient_temperature = 0
        # Byte 1
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
        # Byte 2
        # 后除霜开关请求
        self.__rear_defrost_request = 0
        # 后除霜开关请求有效标志
        self.__rear_defrost_request_valid = 0
        # 按键或旋钮操作导致空调控制器状态发生变化时,需向DVD请求显示变更(此标志维持的时间为:100ms,即空调控制器只需发一次)
        self.__display_active = 0
        # AC Max状态
        self.__ac_max_mode = 0
        # Byte 3
        # 设置温度
        self.__set_temperature = 0
        # Byte 4
        # 鼓风机当前档位
        self.__blower_speed_level = 0
        # 出风模式
        self.__air_distribute_mode = 0
        # 前除霜状态
        self.__defrost_mode = 0
        # Byte 5
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
        # Byte 7
        # 空调压力
        self.__ac_pressure = 0

    @property
    def ac_temperature(self):
        """ 设置温度 """
        return self.__set_temperature * 0.5

    @ac_temperature.setter
    def ac_temperature(self, value):
        """ 设置温度 """
        try:
            if not isinstance(value, float):
                raise AttributeError
            # self.__set_temperature = int('7F', 16) if value < 17.0 or value > 32.0 else int(value / 0.5)
            self.__set_temperature = int(value / 0.5)
        except AttributeError:
            logger.error("AttributeError on ac_temperature")

    @property
    def front_defrost_switch(self):
        """ 空调前除霜开关状态 """
        return self.__defrost_mode

    @front_defrost_switch.setter
    def front_defrost_switch(self, status):
        """ 空调前除霜开关状态 """
        try:
            if status not in DefrostSwitch.CanStatus:
                raise AttributeError
            self.__defrost_mode = status.value
        except AttributeError:
            logger.error("AttributeError on front_defrost_switch")

    @property
    def ac_switch(self):
        """ 空调开关状态 """
        return self.__on_off_state

    @ac_switch.setter
    def ac_switch(self, status):
        """ 空调开关状态 """
        try:
            if status not in AcStatus.CanStatus:
                raise AttributeError
            self.__on_off_state = status.value
        except AttributeError:
            logger.error("AttributeError on ac_switch")

    @property
    def blower_speed_level(self):
        """ 鼓风机档位 """
        return self.__on_off_state

    @blower_speed_level.setter
    def blower_speed_level(self, status):
        """ 鼓风机档位 """
        try:
            if status not in BlowerSpeedLevel.CanStatus:
                raise AttributeError
            self.__blower_speed_level = status.value
        except AttributeError:
            logger.error("AttributeError on blower_speed_level")

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


class Ic34A(CanMsgBasic):
    """ 组合仪表 """
    def __init__(self):
        super(Ic34A, self).__init__('IC_34A',
                                     EnumMsgType.Normal,
                                     0x34A,
                                     EnumMsgTransmitType.Cycle,
                                     EnumMsgSignalType.Cycle,
                                     100,
                                     8,
                                     ['0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00'])
        # Byte 0
        # 瞬时油耗
        self.__temp_fuel_consump = 0
        # 小计流程
        self.__sub_total_mileage = 0
        # 单次里程平均油耗
        self.__single_trip_aver_fuel_consump = 0

    @property
    def temp_fuel_consumption(self):
        """ 瞬时油耗 """
        return self.__temp_fuel_consump * 0.1

    @temp_fuel_consumption.setter
    def temp_fuel_consumption(self, value):
        """ 瞬时油耗 """
        try:
            if not isinstance(value, float):
                raise AttributeError
            self.__temp_fuel_consump = int(value * 10)
        except AttributeError:
            logger.error("AttributeError on temp_fuel_consumption")

    @property
    def sub_total_mileage(self):
        """ 小计里程 """
        return self.__sub_total_mileage

    @sub_total_mileage.setter
    def sub_total_mileage(self, value):
        """ 小计里程 """
        try:
            if not isinstance(value, int):
                raise AttributeError
            if value < 50:
                value = 50
            self.__sub_total_mileage = value
        except AttributeError:
            logger.error("AttributeError on sub_total_mileage")

    def encode(self):
        # 瞬时油耗 + 小计里程
        self._msg_data[0] = hex(self.__temp_fuel_consump >> 2)
        self._msg_data[1] = hex(((self.__sub_total_mileage >> 4) << (8 % 8)) |
                                ((self.__temp_fuel_consump & 0x3) << (14 % 8)))
        # 小计里程
        self._msg_data[2] = hex(((self.__sub_total_mileage & 0xF) << (20 % 8)))
        # 单次里程平均油耗
        self._msg_data[3] = hex((self.__single_trip_aver_fuel_consump << (26 % 8)))
        return self._msg_data

    def dump(self):
        super(Ic34A, self).dump()


class Ic367(CanMsgBasic):
    """ 组合仪表 """
    def __init__(self):
        super(Ic367, self).__init__('IC_367',
                                     EnumMsgType.Normal,
                                     0x367,
                                     EnumMsgTransmitType.Cycle,
                                     EnumMsgSignalType.Cycle,
                                     100,
                                     8,
                                     ['0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00', '0x00'])
        # Byte 1
        # 仪表显示车速有效
        self.__speed_displayed_valid = 0
        # 仪表显示车速
        self.__speed_displayed = 0
        # Byte 2
        # 平均油耗
        self.__average_oil_consumption = 0
        # Byte 6
        # 报文计数器
        self.__rolling_counter = 0
        # 剩余油量报警
        self.__fuel_remain_warning = 0
        # 机油压力低报警
        self.__engine_oil_level_low_warning = 0
        # 制动液位低报警
        self.__brake_oil_level_low_warning = 0
        # 校验和
        self.__checksum = 0

    @property
    def average_oil_consumption(self):
        """ 平均油耗 """
        return self.__average_oil_consumption * 0.1

    @average_oil_consumption.setter
    def average_oil_consumption(self, value):
        """ 平均油耗 """
        try:
            self.__average_oil_consumption = 0x400
            if not isinstance(value, int):
                raise AttributeError
            self.__average_oil_consumption = value * 10
        except AttributeError:
            logger.error("AttributeError on average_oil_consumption")

    def encode(self):
        # 仪表显示车速有效 + 仪表显示车速 + 平均油耗
        self._msg_data[0] = hex((self.__speed_displayed >> 5))
        self._msg_data[1] = hex(((self.__average_oil_consumption >> 8) << (8 % 8)) |
                                (self.__speed_displayed_valid << (10 % 8)) |
                                ((self.__speed_displayed & 0x1F) << (11 % 8)))
        # 平均油耗
        self._msg_data[2] = hex(self.__average_oil_consumption & 0xFF)
        # 报文计数器 + 剩余油量报警 + 机油压力低报警 + 制动液位低报警
        self._msg_data[6] = hex((self.__rolling_counter << (48 % 8)) |
                                (self.__fuel_remain_warning << (52 % 8)) |
                                (self.__engine_oil_level_low_warning << (53 % 8)) |
                                (self.__brake_oil_level_low_warning << (54 % 8)))
        # 校验和
        self._msg_data[7] = hex(self.__checksum << (56 % 8))
        return self._msg_data

    def dump(self):
        super(Ic367, self).dump()


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
        # Byte 0
        # 驾驶位安全带状态
        self.__driver_seat_belt_status = 0
        # 驾驶位安全带状态有效位
        self.__driver_seat_belt_status_valid = 0
        # 副驾驶位安全带状态
        self.__passenger_seat_belt_status = 0
        # 副驾驶位安全带状态有效位
        self.__passenger_seat_belt_status_valid = 0
        # 第二排座位左边安全带状态
        self.__second_row_left_seat_belt_status = 0
        # 第二排座位左边安全带状态有效位
        self.__second_row_left_seat_belt_status_valid = 0
        # 第二排座位中间安全带状态
        self.__second_row_middle_seat_belt_status = 0
        # 第二排座位中间安全带状态有效位
        self.__second_row_middle_seat_belt_status_valid = 0
        # Byte 2
        # 里程
        self.__mileage = 0
        # Byte 4
        # 第二排座位右边安全带状态
        self.__second_row_right_seat_belt_status = 0
        # 油位信号输入电路对电源短路标志位
        self.__oil_signal_short_to_battery = 0
        # 油位信号输入电路对地短裤标志位
        self.__oil_signal_short_to_gnd = 0
        # 油位信号输入电路对开路标志位
        self.__oil_signal_open = 0
        # 续航里程
        self.__driving_mileage = 0
        # Byte 5
        # 剩余油量
        self.__residual_oil_volume = 0
        # 第二排座位右边安全带状态有效位
        self.__second_row_right_seat_belt_status_valid = 0
        # Byte 6
        # 报文计数器
        self.__rolling_counter = 0
        # Byte 7
        # 校验和
        self.__checksum = 0

    @property
    def total_mileage(self):
        """ 里程 """
        return self.__mileage * 10

    @total_mileage.setter
    def total_mileage(self, value):
        """ 里程 """
        try:
            self.__mileage = 0xFFFF
            if not isinstance(value, long):
                raise AttributeError
            if value <= 655350:
                self.__mileage = int(value / 10)
        except AttributeError:
            logger.error("AttributeError on total_mileage")

    @property
    def driving_mileage(self):
        """ 续航里程 """
        return self.__driving_mileage - 50

    @driving_mileage.setter
    def driving_mileage(self, value):
        """ 续航里程 """
        try:
            if not isinstance(value, int):
                raise AttributeError
            self.__driving_mileage = value
        except AttributeError:
            logger.error("AttributeError on driving_mileage")

    @property
    def residual_oil(self):
        """ 剩余油量 """
        return self.__residual_oil_volume

    @residual_oil.setter
    def residual_oil(self, value):
        """ 剩余油量 """
        try:
            if not isinstance(value, int):
                raise AttributeError
            self.__residual_oil_volume = value
        except AttributeError:
            logger.error("AttributeError on residual_oil")

    def encode(self):
        # 驾驶位安全带状态　+ 驾驶位安全带状态有效位 + 副驾驶位安全带状态 + 副驾驶位安全带状态有效位 + 第二排座位左边安全带状态 + 第二排座位左边安全带状态有效位 + 第二排座位中间安全带状态 + 第二排座位中间安全带状态有效位
        self._msg_data[0] = hex((self.__driver_seat_belt_status << 0) |
                                (self.__driver_seat_belt_status_valid << 1) |
                                (self.__passenger_seat_belt_status << 2) |
                                (self.__passenger_seat_belt_status_valid << 3) |
                                (self.__second_row_left_seat_belt_status << 4) |
                                (self.__second_row_left_seat_belt_status_valid << 5) |
                                (self.__second_row_middle_seat_belt_status << 6) |
                                (self.__second_row_middle_seat_belt_status_valid << 7))
        # 里程
        self._msg_data[1] = hex(self.__mileage >> 8)
        self._msg_data[2] = hex(self.__mileage & 0xFF)
        # 第二排座位右边安全带状态 + 油位信号输入电路对电源短路标志位 + 油位信号输入电路对地短裤标志位 + 油位信号输入电路对开路标志位 + 续航里程
        self._msg_data[3] = hex(self.__driving_mileage >> 2)
        self._msg_data[4] = hex((self.__second_row_right_seat_belt_status << (32 % 8)) |
                                (self.__oil_signal_short_to_battery << (33 % 8)) |
                                (self.__oil_signal_short_to_gnd << (34 % 8)) |
                                (self.__oil_signal_open << (35 % 8)) |
                                ((self.__driving_mileage & 0x3) << (38 % 8)))
        # 剩余油量 + 第二排座位右边安全带状态有效位
        self._msg_data[5] = hex((self.__residual_oil_volume << (40 % 8)) |
                                (self.__second_row_right_seat_belt_status_valid << (47 % 8)))
        # 报文计数器 + 校验和
        self._msg_data[6] = hex((self.__rolling_counter << (48 % 8)) |
                                (self.__checksum << (56 % 8)))
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


if __name__ == '__main__':
    pass
