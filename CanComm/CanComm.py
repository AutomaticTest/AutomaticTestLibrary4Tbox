#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
  Copyright (C) 2015-2017 Shenzhen Auto-link world Information Technology Co., Ltd.
  All Rights Reserved

  Name: CanComm.py
  Purpose:

  Created By:    Clive Lau <liuxusheng@auto-link.com.cn>
  Created Date:  2018-01-03

  Changelog:
  Date         Desc
  2018-01-03   Created by Clive Lau
"""

# Builtin libraries
import platform
import threading

# Third-party libraries
from PCANBasic import *
from robot.api import logger

# Customized libraries
from CanProtoDFSK import *
from TimerRepeater.TimerRepeater import TimerRepeater
from Resource.DFSKVehicleStatus import EngineStatus
from Resource.DFSKVehicleStatus import DoorStatus
from Resource.DFSKVehicleStatus import LockStatus
from Resource.DFSKVehicleStatus import HandbrakeStatus
from Resource.DFSKVehicleStatus import DefrostStatus
from Resource.DFSKVehicleStatus import WiperStatus
from Resource.DFSKVehicleStatus import AcStatus
from Resource.DFSKVehicleStatus import GearStatus
from Resource.DFSKVehicleStatus import PepsStatus


IS_WINDOWS = platform.system() == 'Windows'
if IS_WINDOWS:
###*#################################################################################
### Checks if the Windows-Event functionality can be used, by loading               #
### the respective module                                                           #
###                                                                                 #
### Win32 library for Window32 Events handling                                      #
### Module is part of "Python for Win32 Extensions"                                 #
### Web: http://starship.python.net/‾skippy/                                        #
#####################################################################################
    try:
        import win32event
        WINDOWS_EVENT_SUPPORT = True
    except ImportError:
        WINDOWS_EVENT_SUPPORT = False
else:
    WINDOWS_EVENT_SUPPORT = False


class CanComm(object):
    """"""

    CHANNELS = {'PCAN_USBBUS01': PCAN_USBBUS1, 'PCAN_USBBUS02': PCAN_USBBUS2,
                'PCAN_USBBUS03': PCAN_USBBUS3, 'PCAN_USBBUS04': PCAN_USBBUS4,
                'PCAN_USBBUS05': PCAN_USBBUS5, 'PCAN_USBBUS06': PCAN_USBBUS6,
                'PCAN_USBBUS07': PCAN_USBBUS7, 'PCAN_USBBUS08': PCAN_USBBUS8,
                'PCAN_USBBUS09': PCAN_USBBUS9, 'PCAN_USBBUS10': PCAN_USBBUS10,
                'PCAN_USBBUS11': PCAN_USBBUS11, 'PCAN_USBBUS12': PCAN_USBBUS12,
                'PCAN_USBBUS13': PCAN_USBBUS13, 'PCAN_USBBUS14': PCAN_USBBUS14,
                'PCAN_USBBUS15': PCAN_USBBUS15, 'PCAN_USBBUS16': PCAN_USBBUS16}
    BAUDRATES = {'1 MBit/sec': PCAN_BAUD_1M, '800 kBit/sec': PCAN_BAUD_800K,
                 '500 kBit/sec': PCAN_BAUD_500K, '250 kBit/sec': PCAN_BAUD_250K,
                 '125 kBit/sec': PCAN_BAUD_125K, '100 kBit/sec': PCAN_BAUD_100K,
                 '95,238 kBit/sec': PCAN_BAUD_95K, '83,333 kBit/sec': PCAN_BAUD_83K,
                 '50 kBit/sec': PCAN_BAUD_50K, '47,619 kBit/sec': PCAN_BAUD_47K,
                 '33,333 kBit/sec': PCAN_BAUD_33K, '20 kBit/sec': PCAN_BAUD_20K,
                 '10 kBit/sec': PCAN_BAUD_10K, '5 kBit/sec': PCAN_BAUD_5K}
    HWTYPES = {'ISA-82C200': PCAN_TYPE_ISA, 'ISA-SJA1000': PCAN_TYPE_ISA_SJA,
               'ISA-PHYTEC': PCAN_TYPE_ISA_PHYTEC, 'DNG-82C200': PCAN_TYPE_DNG,
               'DNG-82C200 EPP': PCAN_TYPE_DNG_EPP, 'DNG-SJA1000': PCAN_TYPE_DNG_SJA,
               'DNG-SJA1000 EPP': PCAN_TYPE_DNG_SJA_EPP}
    IOPORTS = {'0100': 0x100, '0120': 0x120, '0140': 0x140, '0200': 0x200, '0220': 0x220, '0240': 0x240,
               '0260': 0x260, '0278': 0x278, '0280': 0x280, '02A0': 0x2A0, '02C0': 0x2C0, '02E0': 0x2E0,
               '02E8': 0x2E8, '02F8': 0x2F8, '0300': 0x300, '0320': 0x320, '0340': 0x340, '0360': 0x360,
               '0378': 0x378, '0380': 0x380, '03BC': 0x3BC, '03E0': 0x3E0, '03E8': 0x3E8, '03F8': 0x3F8}
    INTERRUPTS = {'3': 3, '4': 4, '5': 5, '7': 7, '9': 9, '10': 10, '11': 11, '12': 12, '15': 15}

    def __init__(self, channel, baudrate):
        self._tag = self.__class__.__name__ + ' '
        logger.info(self._tag + "__init__ called")
        # PCAN Setting
        self._pcanbasic = PCANBasic()
        self._channel = CanComm.CHANNELS[channel]
        self._baudrate = CanComm.BAUDRATES[baudrate]
        if platform.system() == 'Windows':
            self._hwtype = CanComm.HWTYPES['ISA-82C200']
            self._ioport = CanComm.IOPORTS['0100']
            self._interrupt = CanComm.INTERRUPTS['3']
        else:
            self._hwtype = CanComm.HWTYPES['ISA-82C200']
            self._ioport = CanComm.IOPORTS['0100']
            self._interrupt = CanComm.INTERRUPTS['11']
        # CanMsg Setting
        self._tbox011 = None
        self._sas300 = None
        self._ems302 = None
        self._ems303 = None
        self._abs330 = None
        self._ems360 = None
        self._bcm350 = None
        self._bcm365 = None
        self._ic380 = None
        self._ac378 = None
        self._peps341 = None
        self._tcu328 = None
        self._bcm401 = None
        # Timer Setting
        # self._tmr_read = None
        # Threading Setting
        self._lock = threading.RLock()
        self._alive = False
        self._transmitter_thread = None
        self._transmit_by_cycle = []

    def on_create(self):
        logger.info(self._tag + "on_create called")
        self._tbox011 = Tbox011()
        self._sas300 = Sas300()
        self._ems302 = Ems302()
        self._ems303 = Ems303()
        self._abs330 = Abs330()
        self._ems360 = Ems360()
        self._bcm350 = Bcm350()
        self._bcm365 = Bcm365()
        self._ic380 = Ic380()
        self._ac378 = Ac378()
        self._peps341 = Peps341()
        self._tcu328 = Tcu328()
        self._bcm401 = Bcm401()
        self.register_transmitter(self._sas300)
        self.register_transmitter(self._ems302)
        self.register_transmitter(self._ems303)
        self.register_transmitter(self._abs330)
        self.register_transmitter(self._ems360)
        self.register_transmitter(self._bcm350)
        self.register_transmitter(self._bcm365)
        self.register_transmitter(self._ic380)
        self.register_transmitter(self._ac378)
        self.register_transmitter(self._peps341)
        self.register_transmitter(self._tcu328)
        self.register_transmitter(self._bcm401)
        result = self._pcanbasic.Initialize(self._channel, self._baudrate, self._hwtype, self._ioport, self._interrupt)
        if result != PCAN_ERROR_OK and result != PCAN_ERROR_CAUTION:
                raise CanCommError("Initialize: " + self.__get_formated_error(result))
        result = self._pcanbasic.Reset(self._channel)
        if result != PCAN_ERROR_OK:
            self._pcanbasic.Uninitialize(self._channel)
            raise CanCommError("Reset: " + self.__get_formated_error(result))
        self.start()

    def on_destroy(self):
        logger.info(self._tag + "on_destroy called")
        self.stop()
        self.join()
        if self._pcanbasic is not None:
            self._pcanbasic.Uninitialize(self._channel)
        logger.info(self._tag + "on_destroy end")

    def __get_formated_error(self, error):
        sts_return = self._pcanbasic.GetErrorText(error, 0)
        if sts_return[0] != PCAN_ERROR_OK:
            return "An error occurred. Error-code's text ({0:X}h) couldn't be retrieved".format(error)
        else:
            return sts_return[1]

    def __set_config_data(self, canobj, item, data):
        logger.console(item + ':')
        logger.console(canobj.encode())
        if item == 'LEFT_FRONT_DOOR_STS':
            logger.console("LEFT_FRONT_DOOR_STS")
            canobj.driver_door_status = DoorStatus.CanStatus[data]
        elif item == 'RIGHT_FRONT_DOOR_STS':
            logger.console("RIGHT_FRONT_DOOR_STS")
            canobj.passenger_door_status = DoorStatus.CanStatus[data]
        elif item == 'LEFT_REAR_DOOR_STS':
            logger.console("LEFT_REAR_DOOR_STS")
            canobj.left_rear_door_status = DoorStatus.CanStatus[data]
        elif item == 'RIGHT_REAR_DOOR_STS':
            logger.console("RIGHT_REAR_DOOR_STS")
            canobj.right_rear_door_status = DoorStatus.CanStatus[data]
        elif item == 'TRUNK_DOOR_STS':
            logger.console("TRUNK_DOOR_STS")
            canobj.tailgate_status = DoorStatus.CanStatus[data]
        elif item == 'AC_STS':
            logger.console("AC_STS")
            canobj.on_off_state = AcStatus.CanStatus[data]
        elif item == 'FRONT_DEFROST_STS':
            logger.console("FRONT_DEFROST_STS")
            canobj.defrost_mode = DefrostStatus.CanStatus[data]
        elif item == 'REAR_DEFROST_STS':
            logger.console("REAR_DEFROST_STS")
            canobj.rear_defrost_status = DefrostStatus.CanStatus[data]
        elif item == 'AC_TEMPERATURE':
            logger.console("AC_TEMPERATURE")
            canobj.set_temperature = float(data)
        elif item == 'DOOR_LOCK_STS':
            logger.console("DOOR_LOCK_STS")
            canobj.driver_door_lock_status = LockStatus.CanStatus[data]
        elif item == 'ENGINE_STS':
            logger.console("ENGINE_STS")
            canobj.engine_status = EngineStatus.CanStatus[data]
        elif item == 'WIPER_STS':
            logger.console("WIPER_STS")
            canobj.wiper_status = WiperStatus.CanStatus[data]
        elif item == 'HANDBRAKE_STS':
            logger.console("HANDBRAKE_STS")
            canobj.handbrake_signal = HandbrakeStatus.CanStatus[data]
        elif item == 'PEPS_STS':
            logger.console("PEPS_STS")
            canobj.power_mode = PepsStatus.CanStatus[data]
        elif item == 'GEAR_STS':
            logger.console("GEAR_STS")
            canobj.gear_position_status = GearStatus.CanStatus[data]
        else:
            raise CanCommError("Invalid CAN Config Item")
        logger.console(canobj.encode())

    def on_request(self, item, data):
        logger.info(self._tag + "on_request called")
        convert_config_item_dict = {
            # 即时上报数据信息
            'FUEL_CONSUMPTION':        self._ems360,
            'TOTAL_MILEAGE':           self._ic380,
            # 'CURRENT_SPEED':        ,
            'ENGINE_SPEED':            self._ems302,
            'STEERING_ANGLE':          self._sas300,
            'ACCELERATOR_PEDAL_ANGLE': self._ems302,
            # 'BRAKE_PEDAL_ANGLE': ,
            # 'CLUTCH_PEDAL_ANGLE': ,
            # 车辆状态上报数据
            'LEFT_FRONT_DOOR_STS':  self._bcm350,
            'RIGHT_FRONT_DOOR_STS': self._bcm350,
            'LEFT_REAR_DOOR_STS':   self._bcm350,
            'RIGHT_REAR_DOOR_STS':  self._bcm350,
            'TRUNK_DOOR_STS':       self._bcm350,
            'AC_STS':               self._ac378,
            'FRONT_DEFROST_STS':    self._ac378,
            'REAR_DEFROST_STS':     self._bcm365,
            'AC_TEMPERATURE':       self._ac378,
            'DOOR_LOCK_STS':        self._bcm350,
            'ENGINE_STS':           self._ems303,
            'WIPER_STS':            self._bcm365,
            'HANDBRAKE_STS':        self._bcm350,
            'PEPS_STS':             self._peps341,
            'GEAR_STS':             self._tcu328,
        }
        self.__set_config_data(convert_config_item_dict[item], item, data)
        return True

    # def process_message(self, msg):
    #     logger.console('entry process message')
    #     with self._lock:
    #         # Split the arguments. [0] TPCANMsg, [1] TPCANTimestamp
    #         # logger.console('ID:' + hex(msg.ID))
    #         # logger.console('LEN:' + str(msg.LEN))
    #         # for i in range(8 if (msg.LEN > 8) else msg.LEN):
    #         #     logger.console(str(msg.DATA[i]))
    #         # logger.console('MSGTYPE' + str(msg.MSGTYPE))
    #         if msg.ID == 0x11:
    #             logger.console('ID == 0x11')
    #             for i in range(8 if (msg.LEN > 8) else msg.LEN):
    #                 logger.console(str(msg.DATA[i]))
    #             # self._tbox011.decode(msg.DATA)
    #             # logger.console(self._tbox011.encode())

    # def read_msg(self):
    #     result = self._pcanbasic.Read(self._channel)
    #     if result[0] == PCAN_ERROR_OK:
    #         self.process_message(result[1])
    #     return result[0]
    #
    # def __tmr_read(self):
    #     sts_result = PCAN_ERROR_OK
    #     while not (sts_result & PCAN_ERROR_QRCVEMPTY):
    #         sts_result = self.read_msg()
    #         if sts_result == PCAN_ERROR_ILLOPERATION:
    #             break

    def write_msg(self, basic):
        msg = TPCANMsg()
        msg.ID = basic.get_id()
        msg.LEN = basic.get_length()
        msg.MSGTYPE = PCAN_MESSAGE_STANDARD
        data = basic.encode()
        for i in range(msg.LEN):
            msg.DATA[i] = int(data[i], 16)
        result = self._pcanbasic.Write(self._channel, msg)
        if result != PCAN_ERROR_OK:
            logger.console("write_msg: " + self.__get_formated_error(result))

    def __add_transmitter_with_cycle(self, basic):
        for msg in self._transmit_by_cycle:
            if msg.get_name() == basic.get_name():
                return
        self._transmit_by_cycle.append(basic)

    def __remove_transmitter_with_cycle(self, basic):
        for msg in self._transmit_by_cycle:
            if msg.get_name() == basic.get_name():
                self._transmit_by_cycle.remove(msg)
                break

    def register_transmitter(self, basic):
        if basic.get_signal_type() == EnumMsgSignalType.Cycle:
            self.__add_transmitter_with_cycle(basic)

    def unregister_transmitter(self, basic):
        if basic.get_signal_type() == EnumMsgSignalType.Cycle:
            self.__remove_transmitter_with_cycle(basic)

    def __transmitter_with_cycle(self):
        try:
            while self._alive:
                current_utc = time.time()
                for msg in self._transmit_by_cycle:
                    expected_utc = msg.get_expected_utc()
                    if expected_utc <= current_utc:
                        # logger.console(msg.get_name() + ", utc_dvalue:" + str(current_utc - expected_utc))
                        self.write_msg(msg)
                        msg.set_expected_utc(current_utc)
                        time.sleep(0.1)
        except Exception, e:
            logger.error(self._tag + "Exception on transmit_by_cycle_mode:" + str(e))
            self._alive = False

    def start(self):
        """start worker threads"""
        self._alive = True
        # enter console->serial loop
        self._transmitter_thread = threading.Thread(target=self.__transmitter_with_cycle, name='cycle_transmitter')
        self._transmitter_thread.daemon = True
        self._transmitter_thread.start()
        # self._tmr_read = TimerRepeater("TimerRead", 0.05, self.__tmr_read)
        # self._tmr_read.start()

    def stop(self):
        """set flag to stop worker threads"""
        self._alive = False

    def join(self):
        """wait for worker threads to terminate"""
        if self._transmitter_thread is not None:
            self._transmitter_thread.join()


class CanCommError(Exception):
    pass


if __name__ == '__main__':
    pass
    pcan = CanComm('PCAN_USBBUS01', '500 kBit/sec', 'ISA-82C200', '02A0', '11')
    if not pcan.on_create():
        print("Error on initialize")
    try:
        while True:
            message = raw_input("Type command:")
            command_set = message.split('_')
            if command_set[0] == 'engine':
                print('ENGINE_SPEED')
                pcan.on_request('ENGINE_SPEED', command_set[1])
            elif command_set[0] == 'lf':
                print('LEFT_FRONT_DOOR_STS')
                pcan.on_request('LEFT_FRONT_DOOR_STS', command_set[1])
            elif command_set[0] == 'rf':
                print('RIGHT_FRONT_DOOR_STS')
                pcan.on_request('RIGHT_FRONT_DOOR_STS', command_set[1])
            elif command_set[0] == 'lr':
                print('LEFT_REAR_DOOR_STS')
                pcan.on_request('LEFT_REAR_DOOR_STS', command_set[1])
            elif command_set[0] == 'rr':
                print('RIGHT_REAR_DOOR_STS')
                pcan.on_request('RIGHT_REAR_DOOR_STS', command_set[1])
            elif command_set[0] == 'trunkdoor':
                print('TRUNK_DOOR_STS')
                pcan.on_request('TRUNK_DOOR_STS', command_set[1])
            elif command_set[0] == 'doorlock':
                print('DOOR_LOCK_STS')
                pcan.on_request('DOOR_LOCK_STS', command_set[1])
            elif command_set[0] == 'handbrake':
                print('HANDBRAKE_STS')
                pcan.on_request('HANDBRAKE_STS', command_set[1])
            elif command_set[0] == 'ac':
                print('AC_STS')
                pcan.on_request('AC_STS', command_set[1])
            elif command_set[0] == 'frontdefrost':
                print('FRONT_DEFROST_STS')
                pcan.on_request('FRONT_DEFROST_STS', command_set[1])
            elif command_set[0] == 'reardefrost':
                print('REAR_DEFROST_STS')
                pcan.on_request('REAR_DEFROST_STS', command_set[1])
            elif command_set[0] == 'settemp':
                print('AC_TEMPERATURE')
                pcan.on_request('AC_TEMPERATURE', command_set[1])
            elif command_set[0] == 'enginests':
                print('ENGINE_STS')
                pcan.on_request('ENGINE_STS', command_set[1])
            elif command_set[0] == 'wiper':
                print('WIPER_STS')
                pcan.on_request('WIPER_STS', command_set[1])
            elif command_set[0] == 'gear':
                print('GEAR_STS')
                pcan.on_request('GEAR_STS', command_set[1])
            elif command_set[0] == 'peps':
                print('PEPS_STS')
                pcan.on_request('PEPS_STS', command_set[1])
    except KeyboardInterrupt:
        print("entry KeyboardInterrupt")
        pcan.on_destroy()
