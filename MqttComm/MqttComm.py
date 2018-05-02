#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Copyright (C) 2015-2018 Shenzhen Auto-link world Information Technology Co., Ltd.
  All Rights Reserved

  Name: MqttComm.py
  Purpose:

  Created By:    Clive Lau <liuxusheng@auto-link.com.cn>
  Created Date:  2018-01-11

  Changelog:
  Date         Desc
  2018-01-11   Created by Clive Lau
"""

# Builtin libraries
import os
import time
import random
import platform
import threading

# Third-party libraries
from robot.api import logger
import paho.mqtt.client as mqtt

# Customized libraries
# import Config as CONFIG
from Protobuf import tbox_pb2
from MqttDump import MqttDump
from Resource.DFSKVehicleStatus import DoorStatus
from Resource.DFSKVehicleStatus import WindowStatus
from Resource.DFSKVehicleStatus import RoofStatus
from Resource.DFSKVehicleStatus import DefrostSwitch
from Resource.DFSKVehicleStatus import EngineStatus
from Resource.DFSKVehicleStatus import TyrePressureStatus
from Resource.DFSKVehicleStatus import LockStatus
from Resource.DFSKVehicleStatus import HandbrakeStatus
from Resource.DFSKVehicleStatus import DefrostStatus
from Resource.DFSKVehicleStatus import WiperStatus
from Resource.DFSKVehicleStatus import AcStatus
from Resource.DFSKVehicleStatus import GearStatus
from Resource.DFSKVehicleStatus import PepsStatus


# MQTT Server Settings
MQTT_MAJOR_SERVER = "test.mosquitto.org"
# MQTT_MINOR_SERVER = "14.21.42.158"
MQTT_MINOR_SERVER = "192.168.3.8"
# MQTT_MAJOR_ENCRYPTION = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Encryption/mosquitto.org.crt')
# MQTT_MINOR_ENCRYPTION = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Encryption/autolink_tbox.crt')
MQTT_SERVER_PORT = 8883
MQTT_USER = ""
MQTT_PWD = ""

IS_WINDOWS = platform.system() == 'Windows'
if IS_WINDOWS:
    MQTT_MAJOR_ENCRYPTION = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Encryption\mosquitto.org.crt')
    MQTT_MINOR_ENCRYPTION = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Encryption\\autolink_tbox.crt')
else:
    MQTT_MAJOR_ENCRYPTION = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Encryption/mosquitto.org.crt')
    MQTT_MINOR_ENCRYPTION = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Encryption/autolink_tbox.crt')


# MQTT Topic Settings
MQTT_WILL_TOPIC = "all/will"
MQTT_REPORT_TOPIC = "device/gate/report"
MQTT_BUSINESS_TOPIC = "device/gate/business"
MQTT_DEVICE_TOPIC_PREFIX = "gate/per/device/"
MQTT_DEVICE_TOPIC_SUFFIX = "/order"


class MqttComm(object):
    """"""

    IPADDRS = {'mosquitto.org': 'test.mosquitto.org', 'auto-link.com.cn': '192.168.3.8'}

    def __init__(self, expected_device, server):
        # LogTag
        self._tag = self.__class__.__name__ + ' '
        logger.info(self._tag + "__init__ called")
        # Message head parameter
        self._protocol_version = 0
        self._did_type = tbox_pb2.PDID
        self._msg_id = 1
        self._token = "token-" + expected_device
        self._task_id = 'task-' + str(int(time.time())) + ''.join(str(random.choice(range(10))) for _ in range(5))
        # MQTT parameter
        self._mqttc = None
        self._expected_device = expected_device
        self._server = MqttComm.IPADDRS[server]
        self._is_connected = False
        self._msgtop = None
        self._handle_topic_dict = {
            MQTT_WILL_TOPIC:     self.__handle_topic_will,
            MQTT_REPORT_TOPIC:   self.__handle_topic_report,
            MQTT_BUSINESS_TOPIC: self.__handle_topic_business,
        }
        self._handle_report_dict = {
            tbox_pb2.DATAMINING:           self.__on_response_datamining,
            tbox_pb2.VEHICLE_STATUS:       self.__on_response_vehicle_status,
        }
        self._handle_business_dict = {
            tbox_pb2.LOGIN_REQ:            self.__on_response_login,
            tbox_pb2.HEART_BEAT_REQ:       self.__on_response_heartbeat,
            tbox_pb2.CONFIG_QUERY_REQ:     self.__on_response_config_query,
            tbox_pb2.CONFIG_RESP:          self.__on_response_config,
            tbox_pb2.CONTROL_RESP:         self.__on_response_control,
            tbox_pb2.OTA_CMD_RESP:         self.__on_response_ota_cmd,
            tbox_pb2.OTA_CHECKSUM_REQ:     self.__on_request_ota_checksum,
            tbox_pb2.OTA_RESULT_REPORT:    self.__on_response_ota_result,
            tbox_pb2.DIAGNOSIS_RESPONSE:   self.__on_response_diagnosis,
            tbox_pb2.ALARM_REPORT:         self.__on_response_alarm_signal,
            tbox_pb2.MOTOR_FIRE_REPORT:    self.__on_response_motor_fire_signal,
            tbox_pb2.TRACKING_DATA_REPORT: self.__on_response_tracking_data,
        }
        # Sync parameter
        self._event = threading.Event()
        self._result = False
        # Threading parameter
        self._parse_thread = None
        # CAN msg parameter
        self._can_msg_type = None
        self._can_config_item = None
        self._can_config_data = None

    def __del__(self):
        logger.info(self._tag + "__del__ called")

    def on_create(self):
        logger.info(self._tag + "on_create called")
        # MsgTop
        self._msgtop = tbox_pb2.MsgTop()
        # MQTT onCreate
        self._mqttc = mqtt.Client()
        encryption = MQTT_MAJOR_ENCRYPTION if self._server == MQTT_MAJOR_SERVER else MQTT_MINOR_ENCRYPTION
        if encryption != '':
            try:
                self._mqttc.tls_set(encryption)
                self._mqttc.tls_insecure_set(True)
            except Exception, e:
                raise MqttCommError("Exception on set MQTT TLS: " + str(e) + '(' + encryption + ')')
        if MQTT_USER != '':
            self._mqttc.username_pw_set(MQTT_USER, MQTT_PWD)
        self._mqttc.on_connect = self.__on_connect
        self._mqttc.on_message = self.__on_message
        try:
            self._mqttc.connect(self._server, MQTT_SERVER_PORT)
            self._mqttc.loop_start()
        except Exception, e:
            raise MqttCommError("Exception on connect MQTT Server: " + str(e))

    def on_destroy(self):
        logger.info(self._tag + "on_destroy called")
        # MQTT onDestroy
        if self._mqttc is None:
            return
        self._mqttc.unsubscribe(MQTT_WILL_TOPIC)
        self._mqttc.unsubscribe(MQTT_REPORT_TOPIC)
        self._mqttc.unsubscribe(MQTT_BUSINESS_TOPIC)
        self._mqttc.loop_stop(True)
        self._mqttc.disconnect()
        logger.info(self._tag + "on_destroy end")

    @property
    def is_connected(self):
        logger.console(self._tag + "is connected: " + str(self._is_connected))
        return self._is_connected

    def __on_connect(self, client, userdata, flags, rc):
        logger.console("\n" + self._tag + "Connected with result:" + mqtt.connack_string(rc))
        client.subscribe(MQTT_WILL_TOPIC, qos=1)
        client.subscribe(MQTT_REPORT_TOPIC, qos=1)
        client.subscribe(MQTT_BUSINESS_TOPIC, qos=1)

    def __on_message(self, client, userdata, msg):
        self._parse_thread = threading.Thread(target=self.__parse_thread, args=(client, userdata, msg,), name='on_parse')
        self._parse_thread.daemon = True
        self._parse_thread.start()
        self._parse_thread.join()

    def __parse_thread(self, client, userdata, msg):
        logger.console((self._tag + "__parse_thread called"))
        self._handle_topic_dict[msg.topic](client, userdata, msg)

    def __handle_topic_will(self, client, userdata, msg):
        logger.console(self._tag + "__handle_topic_will called")
        logger.console(self._tag + msg.payload)
        if self._expected_device == msg.payload:
            logger.warn("Entry WILL Topic: " + msg.payload)
            self._is_connected = False

    def __handle_topic_report(self, client, userdata, msg):
        logger.console(self._tag + "==> handle_topic_report")
        msgtop = tbox_pb2.MsgTop()
        msgtop.ParseFromString(msg.payload)
        if self.__is_valid_device(msgtop):
            # set parameter
            if not self._is_connected:
                self._protocol_version = msgtop.message_head.protocol_version
                self._did_type = msgtop.message_head.did_type
                self._msg_id = msgtop.message_head.message_id
                self._token = msgtop.message_head.token
                self._task_id = msgtop.message_head.task_id
                self._is_connected = True
            MqttDump.dump(msgtop)
            handle = self._handle_report_dict.get(msgtop.message_head.msg_type, None)
            if handle is not None:
                handle(client, userdata, msgtop)
        logger.console(self._tag + "handle_topic_report <===")

    def __handle_topic_business(self, client, userdata, msg):
        logger.console(self._tag + "===> handle_topic_business")
        msgtop = tbox_pb2.MsgTop()
        msgtop.ParseFromString(msg.payload)
        if self.__is_valid_device(msgtop):
            # set parameter
            if not self._is_connected:
                self._protocol_version = msgtop.message_head.protocol_version
                self._did_type = msgtop.message_head.did_type
                self._msg_id = msgtop.message_head.message_id
                self._token = msgtop.message_head.token
                self._task_id = msgtop.message_head.task_id
                self._is_connected = True
            MqttDump.dump(msgtop)
            handle = self._handle_business_dict.get(msgtop.message_head.msg_type, None)
            if handle is not None:
                handle(client, userdata, msgtop)
        logger.console(self._tag + "handle_topic_business <===")

    def __on_response_datamining(self, client, userdata, msgtop):
        self._msgtop.datamining.CopyFrom(msgtop.datamining)

    def __on_response_vehicle_status(self, client, userdata, msgtop):
        self._msgtop.vehicle_status.CopyFrom(msgtop.vehicle_status)

    def __on_response_alarm_signal(self, client, userdata, msgtop):
        self._msgtop.alarm_signal.CopyFrom(msgtop.alarm_signal)

    def __on_response_motor_fire_signal(self, client, userdata, msgtop):
        self._msgtop.motor_fire_signal.CopyFrom(msgtop.motor_fire_signal)

    def __on_response_tracking_data(self, client, userdata, msgtop):
        self._msgtop.tracking_data.CopyFrom(msgtop.tracking_data)

    def __inc_msg_id(self):
        self._msg_id = (self._msg_id + 1) % 0xFFFF
        if self._msg_id == 0:
            self._msg_id = 1
        return self._msg_id

    def __is_valid_device(self, msgtop):
        logger.console(self._tag + "is_valid_device called, DevId:" + msgtop.message_head.device_id)
        if msgtop.message_head.device_id == self._expected_device:
            logger.console(self._tag + "=====================New Message=====================")
            return True
        return False

    def __fill_message_head(self, msgtop, msg_id, msg_type, flag=False):
        msgtop.message_head.protocol_version = self._protocol_version
        msgtop.message_head.did_type = self._did_type
        msgtop.message_head.device_id = self._expected_device
        msgtop.message_head.message_id = msg_id
        msgtop.message_head.msg_type = msg_type
        msgtop.message_head.msg_c_time = int(time.time())
        msgtop.message_head.token = self._token
        msgtop.message_head.flag = flag
        msgtop.message_head.task_id = self._task_id

    def __on_response_login(self, client, userdata, msgtop):
        """ MsgLoginResp """
        logger.console(self._tag + "===> on_response_login")
        # set parameter
        if not self._is_connected:
            self._protocol_version = msgtop.message_head.protocol_version
            self._did_type = msgtop.message_head.did_type
            self._msg_id = msgtop.message_head.message_id
            self._token = "token-" + self._expected_device
            self._is_connected = True
        publish_msg = tbox_pb2.MsgTop()
        # message_head
        self.__fill_message_head(publish_msg, self._msg_id, tbox_pb2.LOGIN_RESP)
        # login_response
        publish_msg.login_response.ack.status = True
        publish_msg.login_response.ack.code = "Succeed to login"
        publish_msg.login_response.token = self._token
        # publish
        client.publish(MQTT_DEVICE_TOPIC_PREFIX + self._expected_device + MQTT_DEVICE_TOPIC_SUFFIX,
                       publish_msg.SerializeToString())
        MqttDump.dump(publish_msg)
        logger.console(self._tag + "on_response_login <===")

    ################################################################################
    def __on_response_heartbeat(self, client, userdata, msgtop):
        """ MsgHeartBeatResp """
        logger.console(self._tag + "===> on_response_heartbeat")
        publish_msg = tbox_pb2.MsgTop()
        # message_head
        self.__fill_message_head(publish_msg, self._msg_id, tbox_pb2.HEARTBEAT_RESP)
        # heartbeat_response
        publish_msg.heart_beat_response.ack.status = True
        publish_msg.heart_beat_response.ack.code = "Succeed to response heartbeat"
        # publish
        client.publish(MQTT_DEVICE_TOPIC_PREFIX + self._expected_device + MQTT_DEVICE_TOPIC_SUFFIX,
                       publish_msg.SerializeToString())
        MqttDump.dump(publish_msg)
        logger.console(self._tag + "on_response_heartbeat <===")

    ################################################################################
    def __on_response_config_query(self, client, userdata, msgtop):
        """ MsgConfQueryResp """
        logger.console(self._tag + "===> on_response_config_query")
        publish_msg = tbox_pb2.MsgTop()
        # message_head
        self.__fill_message_head(publish_msg, self._msg_id, tbox_pb2.CONFIG_QUERY_RESP)
        # config_query_response
        publish_msg.config_query_response.ack.status = True
        publish_msg.config_query_response.ack.code = "Succeed to response config query"
        publish_msg.config_query_response.qconfig_data.CopyFrom(self._msgtop.config_query_response.qconfig_data)
        # publish
        client.publish(MQTT_DEVICE_TOPIC_PREFIX + self._expected_device + MQTT_DEVICE_TOPIC_SUFFIX,
                       publish_msg.SerializeToString())
        MqttDump.dump(publish_msg)
        logger.console(self._tag + "on_response_config_query <===")

    ################################################################################
    def _on_request_mqtt_server_addr(self, msgtop, data):
        msgtop.config_request.config_items.append(tbox_pb2.MQTT_SERVER_ADDR)
        msgtop.config_request.rconfig_data.mqtt_server_addr = data

    def _on_request_mqtt_server_topic(self, msgtop, data):
        msgtop.config_request.config_items.append(tbox_pb2.MQTT_SERVER_TOPIC)
        msgtop.config_request.rconfig_data.mqtt_server_topic = data

    def _on_request_mqtt_key_business_server_addr(self, msgtop, data):
        msgtop.config_request.config_items.append(tbox_pb2.MQTT_KEY_BUSINESS_SERVER_ADDR)
        msgtop.config_request.rconfig_data.mqtt_key_business_server_addr = data

    def _on_request_mqtt_key_business_server_topic(self, msgtop, data):
        msgtop.config_request.config_items.append(tbox_pb2.MQTT_KEY_BUSINESS_SERVER_TOPIC)
        msgtop.config_request.rconfig_data.mqtt_key_business_server_topic = data

    def _on_request_ecall_number(self, msgtop, data):
        msgtop.config_request.config_items.append(tbox_pb2.ECALL_NUMBER)
        msgtop.config_request.rconfig_data.ecall_number = data

    def _on_request_bcall_number(self, msgtop, data):
        msgtop.config_request.config_items.append(tbox_pb2.BCALL_NUMBER)
        msgtop.config_request.rconfig_data.bcall_number = data

    def _on_request_icall_number(self, msgtop, data):
        msgtop.config_request.config_items.append(tbox_pb2.ICALL_NUMBER)
        msgtop.config_request.rconfig_data.icall_number = data

    def _on_request_ecall_enable(self, msgtop, data):
        msgtop.config_request.config_items.append(tbox_pb2.ECALL_ENABLE)
        msgtop.config_request.rconfig_data.ecall_enable = True if data.lower() == 'true' else False

    def _on_request_bcall_enable(self, msgtop, data):
        msgtop.config_request.config_items.append(tbox_pb2.BCALL_ENABLE)
        msgtop.config_request.rconfig_data.bcall_enable = True if data.lower() == 'true' else False

    def _on_request_icall_enable(self, msgtop, data):
        msgtop.config_request.config_items.append(tbox_pb2.ICALL_ENABLE)
        msgtop.config_request.rconfig_data.icall_enable = True if data.lower() == 'true' else False

    def _on_request_sms_gate_number_upload(self, msgtop, data):
        msgtop.config_request.config_items.append(tbox_pb2.SMS_GATE_NUMBER_UPLOAD)
        msgtop.config_request.rconfig_data.sms_gate_number_upload = data

    def _on_request_sms_gate_number_download(self, msgtop, data):
        msgtop.config_request.config_items.append(tbox_pb2.SMS_GATE_NUMBER_DOWNLOAD)
        msgtop.config_request.rconfig_data.sms_gate_number_download = data

    def _on_request_datamining_upload_freq(self, msgtop, data):
        msgtop.config_request.config_items.append(tbox_pb2.DATAMINING_UPLOAD_FREQUENCY)
        msgtop.config_request.rconfig_data.datamining_upload_frequency = int(data)

    def _on_request_vehicle_status_upload_freq(self, msgtop, data):
        msgtop.config_request.config_items.append(tbox_pb2.VEHICLE_STATUS_UPLOAD_FREQUENCY)
        msgtop.config_request.rconfig_data.vehicle_status_upload_frequency = int(data)

    def _on_request_ignition_blowout_upload_enable(self, msgtop, data):
        msgtop.config_request.config_items.append(tbox_pb2.IGNITION_BLOWOUT_UPLOAD_ENABLE)
        msgtop.config_request.rconfig_data.ignition_blowout_upload_enable = True if data.lower() == 'true' else False

    def _on_request_upload_alert_enable(self, msgtop, data):
        msgtop.config_request.config_items.append(tbox_pb2.UPLOAD_ALERT_ENABLE)
        msgtop.config_request.rconfig_data.upload_alert_enable = True if data.lower() == 'true' else False

    def _on_request_datamining_enable(self, msgtop, data):
        msgtop.config_request.config_items.append(tbox_pb2.DATAMING_ENABLE)
        msgtop.config_request.rconfig_data.datamining_enable = True if data.lower() == 'true' else False

    def _on_request_svt_enable(self, msgtop, data):
        msgtop.config_request.config_items.append(tbox_pb2.SVT_ENABLE)
        msgtop.config_request.rconfig_data.upload_alert_enable = True if data.lower() == 'true' else False

    def _on_request_eletronic_defense_enable(self, msgtop, data):
        msgtop.config_request.config_items.append(tbox_pb2.ELETRONIC_DEFENSE_ENABLE)
        msgtop.config_request.rconfig_data.eletronic_defense_enable = True if data.lower() == 'true' else False

    def _on_request_abnormal_move_threshold_value(self, msgtop, data):
        msgtop.config_request.config_items.append(tbox_pb2.ABNORMAL_MOVE_THRESHOLD_VALUE)
        msgtop.config_request.rconfig_data.abnormal_move_threshold_value = int(data)

    def _on_request_tracking_data_freq(self, msgtop, data):
        msgtop.config_request.config_items.append(tbox_pb2.TRACKING_DATA_FREQUENCY)
        msgtop.config_request.rconfig_data.tracking_data_frequency = int(data)

    def on_request_config(self, item, data, timeout):
        """ MsgConfReq """
        logger.info(self._tag + "===> on_request_config")
        config_item_req_dict = {
            'MQTT_SERVER_ADDR_REQ':                self._on_request_mqtt_server_addr,
            'MQTT_SERVER_TOPIC_REQ':               self._on_request_mqtt_server_topic,
            'MQTT_KEY_BUSINESS_SERVER_ADDR_REQ':   self._on_request_mqtt_key_business_server_addr,
            'MQTT_KEY_BUSINESS_SERVER_TOPIC_REQ':  self._on_request_mqtt_key_business_server_topic,
            'ECALL_NUMBER_REQ':                    self._on_request_ecall_number,
            'BCALL_NUMBER_REQ':                    self._on_request_bcall_number,
            'ICALL_NUMBER_REQ':                    self._on_request_icall_number,
            'ECALL_ENABLE_REQ':                    self._on_request_ecall_enable,
            'BCALL_ENABLE_REQ':                    self._on_request_bcall_enable,
            'ICALL_ENABLE_REQ':                    self._on_request_icall_enable,
            'SMS_GATE_NUMBER_UPLOAD_REQ':          self._on_request_sms_gate_number_upload,
            'SMS_GATE_NUMBER_DOWNLOAD_REQ':        self._on_request_sms_gate_number_download,
            'DATAMINING_UPLOAD_FREQUENCY_REQ':     self._on_request_datamining_upload_freq,
            'VEHICLE_STATUS_UPLOAD_FREQUENCY_REQ': self._on_request_vehicle_status_upload_freq,
            'IGNITION_BLOWOUT_UPLOAD_ENABLE_REQ':  self._on_request_ignition_blowout_upload_enable,
            'UPLOAD_ALERT_ENABLE_REQ':             self._on_request_upload_alert_enable,
            'DATAMING_ENABLE_REQ':                 self._on_request_datamining_enable,
            'SVT_ENABLE_REQ':                      self._on_request_svt_enable,
            'ELETRONIC_DEFENSE_ENABLE_REQ':        self._on_request_eletronic_defense_enable,
            'ABNORMAL_MOVE_THRESHOLD_VALUE_REQ':   self._on_request_abnormal_move_threshold_value,
            'TRACKING_DATA_FREQUENCY_REQ':         self._on_request_tracking_data_freq,
        }
        self._result = False
        publish_msg = tbox_pb2.MsgTop()
        # message_head
        self.__fill_message_head(publish_msg, self.__inc_msg_id(), tbox_pb2.CONFIG_REQ)
        # remote_config_request
        config_item_req_dict[item](publish_msg, data)
        # publish
        self._mqttc.publish(MQTT_DEVICE_TOPIC_PREFIX + self._expected_device + MQTT_DEVICE_TOPIC_SUFFIX, publish_msg.SerializeToString())
        MqttDump.dump(publish_msg, logger.info)
        logger.info(self._tag + "on_request_config <===")

    def __on_response_config(self, client, userdata, msgtop):
        """ MsgConfResp """
        logger.console(self._tag + "===> on_response_config")
        if self._msg_id != msgtop.message_head.message_id:
            logger.warn(self._tag + "on_response_config: Not expected msg_id")
            return
        if msgtop.HasField("config_response"):
            self._msgtop.config_response.CopyFrom(msgtop.config_response)
        logger.console(self._tag + "on_response_config <===")

    ################################################################################
    def __set_control_item(self, msgtop, item, data):
        if item == tbox_pb2.ENGINE:
            msgtop.remote_control_cmd.engine_parameter = data
        elif item == tbox_pb2.AIR_CONDITION_CTRL:
            msgtop.remote_control_cmd.ac_parameter.ac_switch = data
            # msgtop.remote_control_cmd.ac_parameter.ac_temperature = data
            # msgtop.remote_control_cmd.ac_parameter.ac_front_defrost = data
            # msgtop.remote_control_cmd.ac_parameter.ac_rear_defrost = data
        elif item == tbox_pb2.LOCK:
            msgtop.remote_control_cmd.lock_parameter = data
        elif item == tbox_pb2.FIND_VEHICLE:
            pass
        else:
            raise MqttCommError("Invalid Remote Control Item")

    def on_request_control(self, item, data, timeout):
        """ MsgControlReq """
        logger.info(self._tag + "===> on_request_control")
        convert_control_item_dict = {
            'ENGINE':             tbox_pb2.ENGINE,
            'AIR_CONDITION_CTRL': tbox_pb2.AIR_CONDITION_CTRL,
            'LOCK':               tbox_pb2.LOCK,
            'FIND_VEHICLE':       tbox_pb2.FIND_VEHICLE,
        }
        config_item = convert_control_item_dict[item]
        self._result = False
        publish_msg = tbox_pb2.MsgTop()
        # message_head
        self.__fill_message_head(publish_msg, self.__inc_msg_id(), tbox_pb2.CONTROL_CMD)
        # remote_control_request
        publish_msg.remote_control_cmd.cmd = config_item
        self.__set_control_item(publish_msg, config_item, data)
        # publish
        self._mqttc.publish(MQTT_DEVICE_TOPIC_PREFIX + self._expected_device + MQTT_DEVICE_TOPIC_SUFFIX, publish_msg.SerializeToString())
        MqttDump.dump(publish_msg, logger.info)
        logger.info(self._tag + "on_request_control <===")
        # wait_event
        self._event.wait(int(timeout))
        if not self._event.isSet() or not self._result:
            logger.error(self._tag + "Exception on remote_control_request: Timeout to wait event")
        self._event.clear()
        return self._result

    def __on_response_control(self, client, userdata, msgtop):
        """ MsgControlResp """
        logger.console(self._tag + "===> on_response_remote_control")
        if self._msg_id != msgtop.message_head.message_id:
            logger.warn(self._tag + "on_response_remote_control: Not expected msg_id")
            return
        if msgtop.HasField("remote_control_response"):
            self._result = msgtop.remote_control_response.excute_result
            self._event.set()
        logger.console(self._tag + "on_response_remote_control <===")

    ################################################################################
    def on_request_ota_cmd(self, version, addr, timeout):
        """ MsgOtaCmd """
        logger.info(self._tag + "===> on_request_ota_cmd")
        publish_msg = tbox_pb2.MsgTop()
        # message_head
        self.__fill_message_head(publish_msg, self.__inc_msg_id(), tbox_pb2.OTA_CMD_REQ)
        # remote_ota_request
        publish_msg.ota_cmd.update_target_version = version
        publish_msg.ota_cmd.upgrade_file_download_addr = addr
        publish_msg.ota_cmd.ota_task_id = 'task-' + str(publish_msg.message_head.msg_c_time) + ''.join(str(random.choice(range(10))) for _ in range(5))
        # publish
        self._mqttc.publish(MQTT_DEVICE_TOPIC_PREFIX + self._expected_device + MQTT_DEVICE_TOPIC_SUFFIX,
                            publish_msg.SerializeToString())
        MqttDump.dump(publish_msg, logger.info)
        logger.info(self._tag + "on_request_ota_cmd <===")

    def __on_response_ota_cmd(self, client, userdata, msgtop):
        """ MsgOtaCmdResponse """
        logger.console(self._tag + "===> on_response_ota_cmd")
        if self._msg_id != msgtop.message_head.message_id:
            logger.warn(self._tag + "on_response_ota_cmd: Not expected msg_id")
            return
        if msgtop.HasField("config_response"):
            self._result = msgtop.ota_cmd_response.ack.status
        logger.console(self._tag + "on_response_ota_cmd <===")

    def __on_request_ota_checksum(self, client, userdata, msgtop):
        """ MsgOtaCmdCheckSumRequest """
        logger.console(self._tag + "===> on_request_ota_checksum")
        # publish_msg = tbox_pb2.MsgTop()
        # # message_head
        # self.__fill_message_head(publish_msg, msgtop.message_head.message_id, tbox_pb2.OTA_CMD_CHECK_RESPONSE)
        # # login_response
        # publish_msg.ota_cmd_check_response.ack_code.ack_code = tbox_pb2.SUCCESS
        # publish_msg.ota_cmd_check_response.ack_code.code_desp = "Succeed to request ota checksum"
        # publish_msg.ota_cmd_check_response.check_sum_result = True
        # publish_msg.ota_cmd_check_response.ota_task_id = msgtop.ota_cmd_check_request.ota_task_id
        # # publish
        # client.publish(MQTT_DEVICE_TOPIC_PREFIX + self._expected_device + MQTT_DEVICE_TOPIC_SUFFIX,
        #                publish_msg.SerializeToString())
        # MqttDump.dump(publish_msg)
        logger.console(self._tag + "on_request_ota_checksum <===")

    def on_response_ota_checksum(self, client, userdata, msgtop):
        """ MsgOtaCmdCheckSumResponse """
        logger.console(self._tag + "===> on_response_ota_checksum")
        publish_msg = tbox_pb2.MsgTop()
        # message_head
        self.__fill_message_head(publish_msg, msgtop.message_head.message_id, tbox_pb2.OTA_CHECKSUM_RESP)
        # login_response
        publish_msg.ota_cmd_check_response.ack.status = True
        publish_msg.ota_cmd_check_response.ack.code = "Succeed to response ota checksum"
        publish_msg.ota_cmd_check_response.ota_task_id = msgtop.ota_cmd_check_request.ota_task_id
        # publish
        client.publish(MQTT_DEVICE_TOPIC_PREFIX + self._expected_device + MQTT_DEVICE_TOPIC_SUFFIX,
                       publish_msg.SerializeToString())
        MqttDump.dump(publish_msg)
        logger.console(self._tag + "on_response_ota_checksum <===")

    def __on_response_ota_result(self, client, userdata, msgtop):
        """ MsgOtaResult """
        logger.console(self._tag + "===> on_response_ota_result")
        if self._msg_id != msgtop.message_head.message_id:
            logger.warn(self._tag + "on_response_ota_result: Not expected msg_id")
            return
        if msgtop.HasField("ota_result"):
            self._msgtop.ota_result.CopyFrom(msgtop.ota_result)
        MqttDump.dump(msgtop)
        logger.console(self._tag + "on_response_ota_result <===")

    ################################################################################
    def on_request_diagnosis(self, timeout):
        logger.info(self._tag + "===> on_request_diagnosis")
        self._result = False
        publish_msg = tbox_pb2.MsgTop()
        # message_head
        self.__fill_message_head(publish_msg, self.__inc_msg_id(), tbox_pb2.DIAGNOSIS_REQ)
        # publish
        self._mqttc.publish(MQTT_DEVICE_TOPIC_PREFIX + self._expected_device + MQTT_DEVICE_TOPIC_SUFFIX, publish_msg.SerializeToString())
        MqttDump.dump(publish_msg, logger.info)
        logger.info(self._tag + "on_request_diagnosis <===")
        # wait_event
        self._event.wait(int(timeout))
        if not self._event.isSet() or not self._result:
            logger.error(self._tag + "Exception on remote_diagnosis_request: Timeout to wait event")
        self._event.clear()
        return self._result

    def __on_response_diagnosis(self, client, userdata, msgtop):
        """ on_response_diagnosis """
        logger.console(self._tag + "===> on_response_diagnosis")
        if self._msg_id != msgtop.message_head.message_id:
            logger.warn(self._tag + "on_response_diagnosis: Not expected msg_id")
            return
        if msgtop.HasField("remote_diagnosis_response"):
            self._result = msgtop.diagnosis_response.ack.status
            self._event.set()
        logger.console(self._tag + "on_response_diagnosis <===")

    ################################################################################
    def on_push_message(self, timeout):
        logger.info(self._tag + "===> on_push_message")
        self._result = False
        publish_msg = tbox_pb2.MsgTop()
        # message_head
        self.__fill_message_head(publish_msg, self.__inc_msg_id(), tbox_pb2.PUSH_MESSAGE)
        # publish
        self._mqttc.publish(MQTT_DEVICE_TOPIC_PREFIX + self._expected_device + MQTT_DEVICE_TOPIC_SUFFIX, publish_msg.SerializeToString())
        MqttDump.dump(publish_msg, logger.info)
        logger.info(self._tag + "on_push_message <===")

    ################################################################################
    def on_request_tsp_data(self, item, timeout):
        """
            ################################################################################
            'AC_REQ' 空调开关状态
            'FRONT_DEFROST_REQ' 空调前除霜开关状态
            'REAR_DEFROST_REQ' 空调后除霜开关状态
            'AC_TEMPERATURE_REQ' 空调温度
            'LOCK_DOOR_REQ' 驾驶员左前门锁开关状态
            'ENGINE_REQ' 发动机状态
            'WIPER_REQ' 雨刷开关状态
            'HANDBRAKE_REQ' 手刹状态
            'FRONT_DEFROST_STS' 前除霜状态
            'PEPS_POWER_REQ' PEPS电源状态
            'GEAR_POS_REQ' 档位
            'LF_TIRE_PRESSURE_REQ' 左前胎压
            'LR_TIRE_PRESSURE_REQ' 左后胎压
            'RF_TIRE_PRESSURE_REQ' 右前胎压
            'RR_TIRE_PRESSURE_REQ' 右后胎压
            'BATTERY_VOLTAGE_REQ' 蓄电池电压
            'FUEL_LEVEL_REQ' 剩余油量
            'REMAIN_MILEAGE_REQ' 剩余里程
            'BELT_REQ' 是否系安全带
            'FRONT_FOG_LAMP_REQ' 近光灯状态
            'REAR_FOG_LAMP_REQ' 远光灯状态
            'G_VALUE_REQ' G值
            'LIGHT_INTENSITY_REQ' 光照强度
            'CURR_FUEL_CONSUMPTION_REQ' 瞬时油耗
            'CURR_SPEED_REQ' 当前速度
            'ENGINE_SPEED_REQ' 当前转速
            'STEERING_ANGLE_REQ' 方向盘转角，左为正，右为负
            'ACCELERATOR_PEDAL_ANGLE_REQ' 油门脚踏板角度
            'BRAKE_PEDAL_ANGLE_REQ' 刹车板角度
            'CLUTCH_PEDAL_ANGLE_REQ' 离合器角度
            'TOTAL_MILEAGE_REQ' 总里程
            # 车辆位置
            # 当前追踪状态
            'AVERAGE_FUEL_CONSUMPTION_REQ' 平均油耗
        """
        logger.info(self._tag + "on_request_can_data called")
        data_dict = {
            ################################################################################
            # mqtt server IP地址+端口号
            'CONFIG_MQTT_SERVER_ADDR_RESP':                self._msgtop.config_response.config_new.mqtt_server_addr,
            # mqtt topic
            'CONFIG_MQTT_SERVER_TOPIC_RESP':               self._msgtop.config_response.config_new.mqtt_server_topic,
            # 核心紧急业务mqtt server IP地址 + 端口号
            'CONFIG_MQTT_KEY_BUSINESS_SERVER_ADDR_RESP':   self._msgtop.config_response.config_new.mqtt_key_business_server_addr,
            # 核心紧急业务mqtt topic
            'CONFIG_MQTT_KEY_BUSINESS_SERVER_TOPIC_RESP':  self._msgtop.config_response.config_new.mqtt_key_business_server_topic,
            # E-call号码
            'CONFIG_ECALL_NUMBER_RESP':                    self._msgtop.config_response.config_new.ecall_number,
            # B-call号码
            'CONFIG_BCALL_NUMBER_RESP':                    self._msgtop.config_response.config_new.bcall_number,
            # I-call号码
            'CONFIG_ICALL_NUMBER_RESP':                    self._msgtop.config_response.config_new.icall_number,
            # E-call使能
            'CONFIG_ECALL_ENABLE_RESP':                    str(self._msgtop.config_response.config_new.ecall_enable),
            # B-call使能
            'CONFIG_BCALL_ENABLE_RESP':                    str(self._msgtop.config_response.config_new.bcall_enable),
            # I-call使能
            'CONFIG_ICALL_ENABLE_RESP':                    str(self._msgtop.config_response.config_new.icall_enable),
            # 上行短消息网关
            'CONFIG_SMS_GATE_NUMBER_UPLOAD_RESP':          self._msgtop.config_response.config_new.sms_gate_number_upload,
            # 下行短消息网关
            'CONFIG_SMS_GATE_NUMBER_DOWNLOAD_RESP':        self._msgtop.config_response.config_new.sms_gate_number_download,
            # Datamining上传频率
            'CONFIG_DATAMINING_UPLOAD_FREQUENCY_RESP':     str(self._msgtop.config_response.config_new.datamining_upload_frequency),
            # 车身状态上报频率
            'CONFIG_VEHICLE_STATUS_UPLOAD_FREQUENCY_RESP': str(self._msgtop.config_response.config_new.vehicle_status_upload_frequency),
            # 点火熄火上传状态使能
            'CONFIG_IGNITION_BLOWOUT_UPLOAD_ENABLE_RESP':  str(self._msgtop.config_response.config_new.ignition_blowout_upload_enable),
            # 上报告警信息使能
            'CONFIG_UPLOAD_ALERT_ENABLE_RESP':             str(self._msgtop.config_response.config_new.upload_alert_enable),
            # Datamining使能
            'CONFIG_DATAMING_ENABLE_RESP':                 str(self._msgtop.config_response.config_new.datamining_enable),
            # 追踪功能使能
            'CONFIG_SVT_ENABLE_RESP':                      str(self._msgtop.config_response.config_new.svt_enable),
            # 电子围栏功能使能
            'CONFIG_ELETRONIC_DEFENSE_ENABLE_RESP':        str(self._msgtop.config_response.config_new.eletronic_defense_enable),
            # 异动拖车G-SERNOR触发阈值,单位：0.5G, 取值范围（1-32）
            'CONFIG_ABNORMAL_MOVE_THRESHOLD_VALUE_RESP':   str(self._msgtop.config_response.config_new.abnormal_move_threshold_value),
            # 远程追踪上报频率	5s
            'CONFIG_TRACKING_DATA_FREQUENCY_RESP':         str(self._msgtop.config_response.config_new.tracking_data_frequency),
            ################################################################################
            # 左前门开关状态
            'VEHICLE_LF_DOOR_RESP':    DoorStatus.TspStatus(self._msgtop.vehicle_status.lf_door_status).name,
            # 右前门开关状态
            'VEHICLE_RF_DOOR_RESP':    DoorStatus.TspStatus(self._msgtop.vehicle_status.rf_door_status).name,
            # 左后门开关状态
            'VEHICLE_LR_DOOR_RESP':    DoorStatus.TspStatus(self._msgtop.vehicle_status.lr_door_status).name,
            # 右后门开关状态
            'VEHICLE_RR_DOOR_RESP':    DoorStatus.TspStatus(self._msgtop.vehicle_status.rr_door_status).name,
            # 后尾箱开关状态
            'VEHICLE_TRUNK_DOOR_RESP': DoorStatus.TspStatus(self._msgtop.vehicle_status.trunk_door_status).name,
            # 左前窗开关状态
            'VEHICLE_LF_WINDOW_RESP': WindowStatus.TspStatus(self._msgtop.vehicle_status.lf_window_status).name,
            # 右前窗开关状态
            'VEHICLE_RF_WINDOW_RESP': WindowStatus.TspStatus(self._msgtop.vehicle_status.rf_window_status).name,
            # 左后窗开关状态
            'VEHICLE_LR_WINDOW_RESP': WindowStatus.TspStatus(self._msgtop.vehicle_status.lr_window_status).name,
            # 右后窗开关状态
            'VEHICLE_RR_WINDOW_RESP': WindowStatus.TspStatus(self._msgtop.vehicle_status.rr_window_status).name,
            # 天窗开关状态
            'VEHICLE_ROOF_WINDOW_RESP': RoofStatus.TspStatus(self._msgtop.vehicle_status.roof_window_status).name,
            # 空调开关状态
            'VEHICLE_AC_RESP':             AcStatus.TspStatus(self._msgtop.vehicle_status.air_condition_status).name,
            # 空调前除霜开关状态
            'VEHICLE_FRONT_DEFROST_RESP':  DefrostSwitch.TspStatus(self._msgtop.vehicle_status.air_condition_defrost_status).name,
            # 空调后除霜开关状态
            'VEHICLE_REAR_DEFROST_RESP':   DefrostSwitch.TspStatus(self._msgtop.vehicle_status.air_condition_rear_defrost_status).name,
            # 空调温度
            'VEHICLE_AC_TEMPERATURE_RESP': str(self._msgtop.vehicle_status.air_condition_temperature),
            # 驾驶员左前门锁开关状态
            'VEHICLE_LOCK_DOOR_RESP': LockStatus.TspStatus(self._msgtop.vehicle_status.lock_status).name,
            # 发动机状态
            'VEHICLE_ENGINE_RESP': EngineStatus.TspStatus(self._msgtop.vehicle_status.engine_status).name,
            # 雨刷开关状态
            'VEHICLE_WIPER_RESP': WiperStatus.TspStatus(self._msgtop.vehicle_status.wiper_Status).name,
            # 手刹状态
            'VEHICLE_HANDBRAKE_RESP': HandbrakeStatus.TspStatus(self._msgtop.vehicle_status.hand_break_status).name,
            # 前除霜状态
            'VEHICLE_FRONT_DEFROST_STS': "",
            # PEPS电源状态
            'VEHICLE_PEPS_POWER_RESP': PepsStatus.TspStatus(self._msgtop.vehicle_status.peps_power_mode).name,
            # 档位
            'VEHICLE_GEAR_POS_RESP': GearStatus.TspStatus(self._msgtop.vehicle_status.gear_position).name,
            # 左前胎压
            'VEHICLE_LF_TIRE_PRESSURE_RESP': TyrePressureStatus.TspStatus(int(self._msgtop.vehicle_status.lf_tire_pressure)).name,
            # 右前胎压
            'VEHICLE_RF_TIRE_PRESSURE_RESP': TyrePressureStatus.TspStatus(int(self._msgtop.vehicle_status.rf_tire_pressure)).name,
            # 左后胎压
            'VEHICLE_LR_TIRE_PRESSURE_RESP': TyrePressureStatus.TspStatus(int(self._msgtop.vehicle_status.lr_tire_pressure)).name,
            # 右后胎压
            'VEHICLE_RR_TIRE_PRESSURE_RESP': TyrePressureStatus.TspStatus(int(self._msgtop.vehicle_status.rr_tire_pressure)).name,
            # 蓄电池电压(TBox未上传)
            'VEHICLE_BATTERY_VOLTAGE_RESP': "",
            # 剩余油量
            'VEHICLE_FUEL_LEVEL_RESP': str(self._msgtop.vehicle_status.fuel_level),
            # 剩余里程
            'VEHICLE_REMAIN_MILEAGE_RESP': str(int(self._msgtop.vehicle_status.remain_mileage)),
            # 是否系安全带(TBox未上传)
            'VEHICLE_BELT_RESP': "",
            # 近光灯状态(TBox未上传)
            'VEHICLE_FRONT_FOG_LAMP_RESP': "",
            # 远光灯状态(TBox未上传)
            'VEHICLE_REAR_FOG_LAMP_RESP': "",
            # G值(TBox未上传)
            'VEHICLE_G_VALUE_RESP': "",
            # 光照强度(TBox未上传)
            'VEHICLE_LIGHT_INTENSITY_RESP': str(self._msgtop.vehicle_status.light_intensity),
            # 瞬时油耗
            'VEHICLE_CURR_FUEL_CONSUMPTION_RESP': str(self._msgtop.vehicle_status.current_fuel_consumption),
            # 当前速度
            'VEHICLE_CURR_SPEED_RESP': str(self._msgtop.vehicle_status.current_speed),
            # 当前转速
            'VEHICLE_ENGINE_SPEED_RESP': str(self._msgtop.vehicle_status.engine_speed),
            # 方向盘转角，左为正，右为负
            'VEHICLE_STEERING_ANGLE_RESP': str(self._msgtop.vehicle_status.steering_angle),
            # 油门脚踏板角度
            'VEHICLE_ACCELERATOR_PEDAL_ANGLE_RESP': str(self._msgtop.vehicle_status.accelerator_pedal_angle),
            # 刹车板角度(TBox未上传)
            'VEHICLE_BRAKE_PEDAL_ANGLE_RESP': str(self._msgtop.vehicle_status.brake_pedal_angle),
            # 离合器角度(TBox未上传)
            'VEHICLE_CLUTCH_PEDAL_ANGLE_RESP': str(self._msgtop.vehicle_status.clutch_pedal_angle),
            # 总里程
            'VEHICLE_TOTAL_MILEAGE_RESP': str(self._msgtop.vehicle_status.total_mileage),
            # 车辆位置
            # 当前追踪状态
            # 平均油耗
            'VEHICLE_AVERAGE_FUEL_CONSUMPTION_RESP': str(self._msgtop.vehicle_status.average_fuel_consumption),
        }
        return unicode(data_dict[item])


class MqttCommError(Exception):
    pass


if __name__ == '__main__':
    pass
