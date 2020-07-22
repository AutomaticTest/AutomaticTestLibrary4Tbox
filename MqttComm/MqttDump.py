#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Copyright (C) 2015-2018 Shenzhen Auto-link world Information Technology Co., Ltd.
  All Rights Reserved

  Name: MqttDump.py
  Purpose:

  Created By:    Clive Lau <liuxusheng@auto-link.com.cn>
  Created Date:  2018-01-11

  Changelog:
  Date         Desc
  2018-01-11   Created by Clive Lau
"""

# Builtin libraries
from datetime import datetime

# Third-party libraries
from robot.api import logger

# Customized libraries


logging = logger.console


class MqttDump(object):
    logging = None

    @staticmethod
    def __enum_did_type(id_type):
        """设备编号类型"""
        type_dict = {
            0: "PDID",
            1: "VIN",
            2: "IMEI",
            3: "ICCID",
        }
        return type_dict.get(id_type, 'InvalidParam')

    @staticmethod
    def __enum_msg_type(msg_type):
        """消息类型"""
        type_dict = {
            0:  "TYPE0",
            1:  "TYPE1",
            2:  "ACK",
            3:  "REG_REQ",
            4:  "REG_RESP",
            5:  "LOGIN_REQ",
            6:  "LOGIN_RESP",
            7:  "HEARTBEAT_RESP",
            8:  "CONFIG_QUERY_RESP",
            9:  "CONFIG_REQ",
            10: "CONFIG_RESP",
            11: "CONTROL_CMD",
            12: "CONTROL_RESP",
            13: "OTA_CMD_REQ",
            14: "OTA_CMD_RESP",
            15: "OTA_CHECKSUM_REQ",
            16: "OTA_CHECKSUM_RESP",
            17: "OTA_RESULT_REPORT",
            18: "DIAGNOSIS_RESPONSE",
            19: "DATAMINING",
            20: "VEHICLE_STATUS",
            21: "ALARM_REPORT",
            22: "PUSH_MESSAGE",
            23: "MOTOR_FIRE_REPORT",
            24: "TRACKING_DATA_REPORT",
            101: "HEART_BEAT_REQ",
            102: "LOGOUT_REQ",
            103: "CONFIG_QUERY_REQ",
            104: "DIAGNOSIS_REQ",
            105: "VEHICLE_STATUS_REQ",
        }
        return type_dict.get(msg_type, 'InvalidParam')

    @staticmethod
    def __enum_common_ack_code(code):
        """通用的消息回复码"""
        code_dict = {
            0: "SUCCESS",
            1: "FAILED",
            2: "NOT_LOGIN",
            3: "MESSAGE_PARSE_ERROR",
        }
        return code_dict.get(code, 'InvalidParam')

    @staticmethod
    def __enum_config_item(item):
        """远程配置项枚举"""
        item_dict = {
            0: "MQTT_SERVER_ADDR",
            1: "MQTT_SERVER_TOPIC",
            2: "MQTT_KEY_BUSINESS_SERVER_ADDR",
            3: "MQTT_KEY_BUSINESS_SERVER_TOPIC",
            4: "ECALL_NUMBER",
            5: "BCALL_NUMBER",
            6: "ICALL_NUMBER",
            7: "ECALL_ENABLE",
            8: "BCALL_ENABLE",
            9: "ICALL_ENABLE",
            10: "SMS_GATE_NUMBER_UPLOAD",
            11: "SMS_GATE_NUMBER_DOWNLOAD",
            12: "DATAMINING_UPLOAD_FREQUENCY",
            13: "VEHICLE_STATUS_UPLOAD_FREQUENCY",
            14: "IGNITION_BLOWOUT_UPLOAD_ENABLE",
            15: "UPLOAD_ALERT_ENABLE",
            16: "DATAMING_ENABLE",
            17: "SVT_ENABLE",
            18: "ELETRONIC_DEFENSE_ENABLE",
            19: "ABNORMAL_MOVE_THRESHOLD_VALUE",
            20: "TRACKING_DATA_FREQUENCY",
        }
        return item_dict.get(item, 'InvalidParam')

    @staticmethod
    def __enum_remote_config_error_code(code):
        """远程配置错误码"""
        code_dict = {
            0: "UNKNOW",
        }
        return code_dict.get(code, 'InvalidParam')

    @staticmethod
    def __enum_control_type(cmd_type):
        """远程控制命令类型"""
        type_dict = {
            0: "ENGINE",
            1: "AIR_CONDITION_CTRL",
            2: "LOCK",
            3: "FIND_VEHICLE",
            4: "WINDOWS",
            5: "SEAT",
            6: "TRACK",
        }
        return type_dict.get(cmd_type, 'InvalidParam')

    @staticmethod
    def __enum_windows_type(window_type):
        """车窗类型"""
        type_dict = {
            0: "WINDOW",
            1: "ROOF",
        }
        return type_dict.get(window_type, 'InvalidParam')

    @staticmethod
    def __enum_windows_param(window_param):
        """车窗参数"""
        param_dict = {
            0: "WUNKNOW",
            1: "WSTOP",
            2: "RISE",
            3: "FALL",
        }
        return param_dict.get(window_param, 'InvalidParam')

    @staticmethod
    def __enum_roof_param(roof_param):
        """天窗参数"""
        param_dict = {
            0: "RUNKNOW",
            1: "OPEN",
            2: "CLOSE",
            3: "RSTOP",
            4: "UP",
        }
        return param_dict.get(roof_param, 'InvalidParam')

    @staticmethod
    def __enum_seat_level(level):
        """座位参数"""
        level_dict = {
            0: "SCLOSE",
            1: "LEVEL1",
            2: "LEVEL2",
            3: "LEVEL3",
            4: "LEVEL_INVALID",
        }
        return level_dict.get(level, 'InvalidParam')

    @staticmethod
    def __enum_remote_control_execute_result(result):
        """远程控制执行结果"""
        result_dict = {
            0: "FAILED",
            1: "SUCCESS",
        }
        return result_dict.get(result, 'InvalidParam')

    @staticmethod
    def __enum_ota_cmd_result_code(code):
        """OTA升级命令执行结果码"""
        code_dict = {
            0: "UPGRADE_FAILED",
            1: "UPGRADE_SUCCESSED",
            2: "DOWNLOAD_FILE_FAILED",
            3: "OTA_IN_PROCESS",
        }
        return code_dict.get(code, 'InvalidParam')

    @staticmethod
    def __enum_peps_power_mode(mode):
        """PEPS电源模式"""
        mode_dict = {
            0: "DEFAULT",
            1: "OFF",
            2: "ACC",
            3: "ON",
            4: "START",
            5: "INVALID"
        }
        return mode_dict.get(mode, 'InvalidParam')

    @staticmethod
    def __enum_crash_info(info):
        """碰撞信息"""
        info_dict = {
            0: "NONE_CRASH",
            1: "UNKNOWN_CRASH",
            2: "HEAD_CRASH",
            3: "LEFT_SIDE_CRASH",
            4: "RIGHT_SIDE_CRASH",
            5: "TAIL_CRASH",
            6: "PEDESTRIAN",
            7: "MUTI_CRASH",
        }
        return info_dict.get(info, 'InvalidParam')

    @staticmethod
    def __enum_common_true_false_unknown(msg):
        """通用TRUE FALSE UNKNOWN"""
        msg_dict = {
            0: "FALSE",
            1: "TRUE",
            2: "UNKNOWN",
        }
        return msg_dict.get(msg, 'InvalidParam')

    @staticmethod
    def __enum_alarm_signal_type(signal_type):
        """报警信号信息"""
        type_dict = {
            0: "AIR_BAG",
            1: "SIDE_TURN",
            2: "UNUSUAL_MOVE",
            3: "ANTI_THEFT",
            4: "VEHICLE_CRASH",
            5: "WINDOW_ABNORMAL",
        }
        return type_dict.get(signal_type, 'InvalidParam')

    @staticmethod
    def __enum_on_off_state(state):
        """on/off状态"""
        state_dict = {
            0: "UNKNOWN",
            1: "OFF",
            2: "ON"
        }
        return state_dict.get(state, 'InvalidParam')

    @staticmethod
    def __enum_engine_state(state):
        """发动机状态"""
        state_dict = {
            0: "UNKNOWN",
            1: "KEYOFF",
            2: "KEYON",
            3: "CRANK",
            4: "RUNNING"
        }
        return state_dict.get(state, 'InvalidParam')

    @staticmethod
    def __enum_gear_position(pos):
        """变速箱档位"""
        pos_dict = {
            0: "P",
            1: "R",
            2: "N",
            3: "D",
            4: "MANUAL_1",
            5: "MANUAL_2",
            6: "MANUAL_3",
            7: "MANUAL_4",
            8: "MANUAL_5",
            9: "MANUAL_6",
            10: "MANUAL_7",
            11: "MANUAL_8",
            12: "S",
            13: "UNKNOW",
            14: "Z1",
            15: "Z2",
            16: "Z3",
            17: "Invalid"
        }
        return pos_dict.get(pos, 'InvalidParam')

    @staticmethod
    def __enum_motor_fire_mode(mode):
        """点火熄火状态"""
        mode_dict = {
            0: "IGNITION",
            1: "FLAMEOUT",
        }
        return mode_dict.get(mode, 'InvalidParam')

    @staticmethod
    def __show_msg_ack(ack):
        msg = "{" \
              + "status:" + str(ack.status) \
              + ", code:" + ack.code \
              + "}"
        return msg

    @staticmethod
    def __show_gps_info(gps_info):
        msg = "{" \
              + "longtitude:" + str(gps_info.longtitude) \
              + ", latitude:" + str(gps_info.latitude) \
              + ", altitude:" + str(gps_info.altitude) \
              + ", gps_heading:" + str(gps_info.gps_heading) \
              + ", gps_speed:" + str(gps_info.gps_speed) \
              + ", satellite_number:" + str(gps_info.satellite_number) \
              + ", valid:" + str(gps_info.valid) \
              + ", gps_time:" + str(datetime.fromtimestamp(gps_info.gps_time)) \
              + "}"
        return msg

    @staticmethod
    def __show_config_data(config_data):
        msg = "{" \
              + "mqtt_server_addr:" + config_data.mqtt_server_addr \
              + ", mqtt_server_topic:" + config_data.mqtt_server_topic \
              + ", mqtt_key_business_server_addr:" + config_data.mqtt_key_business_server_addr \
              + ", mqtt_key_business_server_topic:" + config_data.mqtt_key_business_server_topic \
              + ", ecall_number:" + config_data.ecall_number \
              + ", bcall_number:" + config_data.bcall_number \
              + ", icall_number:" + config_data.icall_number \
              + ", ecall_enable:" + str(config_data.ecall_enable) \
              + ", bcall_enable:" + str(config_data.bcall_enable) \
              + ", icall_enable:" + str(config_data.icall_enable) \
              + ", sms_gate_number_upload:" + config_data.sms_gate_number_upload \
              + ", sms_gate_number_download:" + config_data.sms_gate_number_download \
              + ", datamining_upload_frequency:" + str(config_data.datamining_upload_frequency) \
              + ", vehicle_status_upload_frequency:" + str(config_data.vehicle_status_upload_frequency) \
              + ", ignition_blowout_upload_enable:" + str(config_data.ignition_blowout_upload_enable) \
              + ", upload_alert_enable:" + str(config_data.upload_alert_enable) \
              + ", datamining_enable:" + str(config_data.datamining_enable) \
              + ", svt_enable:" + str(config_data.svt_enable) \
              + ", eletronic_defense_enable:" + str(config_data.eletronic_defense_enable) \
              + ", abnormal_move_threshold_value:" + str(config_data.abnormal_move_threshold_value) \
              + "}"
        return msg

    @staticmethod
    def __show_config_result(config_result):
        msg = "{" \
              + "config_item:" + MqttDump.__enum_config_item(config_result.config_item) \
              + ", result:" + str(config_result.result) \
              + "}"
        return msg

    @staticmethod
    def __show_air_parameter(air_param):
        msg = "{" \
              + "ac_switch:" + str(air_param.ac_switch) \
              + ", ac_temperature:" + str(air_param.ac_temperature) \
              + ", ac_front_defrost:" + str(air_param.ac_front_defrost) \
              + ", ac_rear_defrost:" + str(air_param.ac_rear_defrost) \
              + "}"
        return msg

    @staticmethod
    def __show_window_parameter(window_param):
        msg = "{" \
              + "type:" + MqttDump.__enum_windows_type(window_param.type) \
              + ", window_param:" + MqttDump.__enum_windows_param(window_param.windw_param) \
              + ", roof_param:" + MqttDump.__enum_roof_param(window_param.roof_param) \
              + "}"
        return msg

    @staticmethod
    def __show_seat_parameter(seat_param):
        msg = "{" \
              + "main:" + MqttDump.__enum_seat_level(seat_param.main) \
              + ", subordinate:" + MqttDump.__enum_seat_level(seat_param.subordinate) \
              + "}"
        return msg

    @staticmethod
    def __show_vehicle_status(vehicle_status):
        msg = "{" \
              + "lf_door_status:" + MqttDump.__enum_on_off_state(vehicle_status.lf_door_status) \
              + ", lr_door_status:" + MqttDump.__enum_on_off_state(vehicle_status.lr_door_status) \
              + ", rf_door_status:" + MqttDump.__enum_on_off_state(vehicle_status.rf_door_status) \
              + ", rr_door_status:" + MqttDump.__enum_on_off_state(vehicle_status.rr_door_status) \
              + ", trunk_door_status:" + MqttDump.__enum_on_off_state(vehicle_status.trunk_door_status) \
              + ", lf_window_status:" + MqttDump.__enum_on_off_state(vehicle_status.lf_window_status) \
              + ", lr_window_status:" + MqttDump.__enum_on_off_state(vehicle_status.lr_window_status) \
              + ", rf_window_status:" + MqttDump.__enum_on_off_state(vehicle_status.rf_window_status) \
              + ", rr_window_status:" + MqttDump.__enum_on_off_state(vehicle_status.rr_window_status) \
              + ", roof_window_status:" + MqttDump.__enum_on_off_state(vehicle_status.roof_window_status) \
              + ", air_condition_status:" + MqttDump.__enum_on_off_state(vehicle_status.air_condition_status) \
              + ", air_condition_defrost_status:" + MqttDump.__enum_on_off_state(vehicle_status.air_condition_defrost_status) \
              + ", air_condition_rear_defrost_status:" + MqttDump.__enum_on_off_state(vehicle_status.air_condition_rear_defrost_status) \
              + ", air_condition_temperature:" + str(vehicle_status.air_condition_temperature) \
              + ", lock_status:" + MqttDump.__enum_on_off_state(vehicle_status.lock_status) \
              + ", engine_status:" + MqttDump.__enum_engine_state(vehicle_status.engine_status) \
              + ", wiper_Status:" + MqttDump.__enum_on_off_state(vehicle_status.wiper_Status) \
              + ", hand_break_status:" + MqttDump.__enum_on_off_state(vehicle_status.hand_break_status) \
              + ", defrost_mode:" + MqttDump.__enum_on_off_state(vehicle_status.defrost_mode) \
              + ", peps_power_mode:" + MqttDump.__enum_peps_power_mode(vehicle_status.peps_power_mode) \
              + ", gear_position:" + MqttDump.__enum_gear_position(vehicle_status.gear_position) \
              + ", lf_tire_pressure:" + str(vehicle_status.lf_tire_pressure) \
              + ", lr_tire_pressure:" + str(vehicle_status.lr_tire_pressure) \
              + ", rf_tire_pressure:" + str(vehicle_status.rf_tire_pressure) \
              + ", rr_tire_pressure:" + str(vehicle_status.rr_tire_pressure) \
              + ", battery_voltage:" + str(vehicle_status.battery_voltage) \
              + ", fuel_level:" + str(vehicle_status.fuel_level) \
              + ", remain_mileage:" + str(vehicle_status.remain_mileage) \
              + ", belt:" + MqttDump.__enum_on_off_state(vehicle_status.belt) \
              + ", front_light:" + MqttDump.__enum_on_off_state(vehicle_status.front_light) \
              + ", hight_light:" + MqttDump.__enum_on_off_state(vehicle_status.hight_light) \
              + ", light_intensity:" + str(vehicle_status.light_intensity) \
              + ", current_fuel_consumption:" + str(vehicle_status.current_fuel_consumption) \
              + ", current_speed:" + str(vehicle_status.current_speed) \
              + ", engine_speed:" + str(vehicle_status.engine_speed) \
              + ", steering_angle:" + str(vehicle_status.steering_angle) \
              + ", accelerator_pedal_angle:" + str(vehicle_status.accelerator_pedal_angle) \
              + ", brake_pedal_angle:" + str(vehicle_status.brake_pedal_angle) \
              + ", clutch_pedal_angle:" + str(vehicle_status.clutch_pedal_angle) \
              + ", total_mileage:" + str(vehicle_status.total_mileage) \
              + ", gps_info:" + MqttDump.__show_gps_info(vehicle_status.gps_info) \
              + ", track_status:" + MqttDump.__enum_on_off_state(vehicle_status.track_status) \
              + ", average_fuel_consumption:" + str(vehicle_status.average_fuel_consumption) \
              + "}"
        return msg

    @staticmethod
    def __show_diagnosis_result(result):
        msg = "{" \
              + "ecu_id:" + str(result.ecu_id) \
              + ", dtcs:" + str(result.dtcs) \
              + "}"
        return msg

    @staticmethod
    def __show_g_value(value):
        msg = "{" \
              + "gvalue:" + str(value.gvalue) \
              + ", current_speed:" + str(value.current_speed) \
              + ", engine_speed:" + str(value.engine_speed) \
              + ", gvalue_time:" + str(datetime.fromtimestamp(value.gvalue_time)) \
              + ", gps_info:" + MqttDump.__show_gps_info(value.gps_info) \
              + ", gvalue_valid:" + str(value.gvalue_valid) \
              + "}"
        return msg

    @staticmethod
    def __show_gsensor_value(value):
        msg = "{" \
              + "x:" + str(value.x) \
              + ", y:" + str(value.y) \
              + ", z:" + str(value.z) \
              + "}"
        return msg

    @staticmethod
    def __show_window_info(value):
        msg = "{" \
              + "roof_window:" + MqttDump.__enum_common_true_false_unknown(value.roof_window) \
              + ", lf_window:" + MqttDump.__enum_common_true_false_unknown(value.lf_window) \
              + ", lr_window:" + MqttDump.__enum_common_true_false_unknown(value.lr_window) \
              + ", rf_window:" + MqttDump.__enum_common_true_false_unknown(value.rf_window) \
              + ", rr_window:" + MqttDump.__enum_common_true_false_unknown(value.rr_window) \
              + "}"
        return msg

    @staticmethod
    def __list_msg_head(msg_head):
        """通用头，必填字段 01"""
        logging("====> MsgHead <====")
        logging("protocol_version:     " + str(msg_head.protocol_version))
        logging("did_type:             " + MqttDump.__enum_did_type(msg_head.did_type))
        logging("device_id:            " + msg_head.device_id)
        logging("message_id:           " + str(msg_head.message_id))
        logging("msg_type:             " + MqttDump.__enum_msg_type(msg_head.msg_type))
        logging("msg_c_time:           " + str(datetime.fromtimestamp(msg_head.msg_c_time)))
        logging("token:                " + msg_head.token)
        logging("flag:                 " + str(msg_head.flag))
        logging("task_id:              " + str(msg_head.task_id))

    @staticmethod
    def __list_msg_ack(msg_ack):
        """通用回复消息 02"""
        logging("====> MsgAck <====")
        logging("status: " + str(msg_ack.status))
        logging("code:   " + msg_ack.code)

    @staticmethod
    def __list_msg_register_request(register_request):
        """注册请求 03"""
        logging("====> MsgRegReq <====")
        logging("pdid:         " + register_request.pdid)
        logging("iccid:        " + register_request.iccid)
        logging("tbox_version: " + register_request.tbox_version)

    @staticmethod
    def __list_msg_register_response(register_response):
        """注册回复 04"""
        logging("====> MsgRegisterResponse <====")
        logging("res_code:   " + str(register_response.res_code))
        logging("addr:       " + register_response.addr)
        logging("ca_cer:     " + register_response.ca_cer)
        logging("custom_cer: " + register_response.custom_cer)

    @staticmethod
    def __list_msg_login_request(login_request):
        """登录请求 05"""
        logging("====> MsgLoginRequest <====")
        logging("pdid:        " + login_request.pdid)
        logging("iccid:       " + login_request.iccid)
        logging("vin:         " + login_request.vin)
        logging("version:     " + login_request.version)
        logging("release_tag: " + login_request.release_tag)

    @staticmethod
    def __list_msg_login_response(login_response):
        """登录回复 06"""
        logging("====> MsgLoginResponse <====")
        logging("ack:   " + MqttDump.__show_msg_ack(login_response.ack))
        logging("token: " + login_response.token)

    @staticmethod
    def __list_msg_heartbeat_response(heartbeat_response):
        """心跳 07"""
        logging("====> MsgHeartbeatResponse <====")
        logging("ack: " + MqttDump.__show_msg_ack(heartbeat_response.ack))

    @staticmethod
    def __list_msg_config_query_response(config_query_response):
        """远程查询应答 08"""
        logging("====> MsgConfigQueryResponse <====")
        logging("ack:         " + MqttDump.__show_msg_ack(config_query_response.ack))
        logging("config_data: " + MqttDump.__show_config_data(config_query_response.qconfig_data))

    @staticmethod
    def __list_msg_config_request(config_request):
        """远程配置下发 09"""
        logging("====> MsgRemoteConfigRequest <====")
        for item in config_request.config_items:
            logging("config_items: " + MqttDump.__enum_config_item(item))
        logging("rconfig_data:  " + MqttDump.__show_config_data(config_request.rconfig_data))

    @staticmethod
    def __list_msg_config_response(config_response):
        """远程配置应答 10"""
        logging("====> MsgConfigResponse <====")
        logging("ack:       " + MqttDump.__show_msg_ack(config_response.ack))
        for result in config_response.config_results:
            logging("config_results: " + MqttDump.__show_config_result(result))
        logging("config_old:     " + MqttDump.__show_config_data(config_response.config_old))
        logging("config_new:     " + MqttDump.__show_config_data(config_response.config_new))

    @staticmethod
    def __list_msg_control_request(control_request):
        """远程控制命令下发 11"""
        logging("====> MsgControlRequest <====")
        logging("cmd_type:     " + MqttDump.__enum_control_type(control_request.cmd_type))
        logging("air_param:    " + MqttDump.__show_air_parameter(control_request.air_param))
        logging("engine_param: " + str(control_request.engine_param))
        logging("lock_param:   " + str(control_request.lock_param))
        logging("window_param: " + MqttDump.__show_window_parameter(control_request.window_param))
        logging("seat_param:   " + MqttDump.__show_seat_parameter(control_request.seat_param))
        logging("track_signal: " + str(control_request.track_signal))

    @staticmethod
    def __list_msg_control_response(control_response):
        """远程控制结果应答 12"""
        print("====> MsgControlResponse <====")
        print("ack:            " + MqttDump.__show_msg_ack(control_response.ack))
        print("vehicle_status: " + MqttDump.__show_vehicle_status(control_response.vehicle_status))

    @staticmethod
    def __list_msg_ota_cmd(ota_cmd):
        """OTA升级命令下发 13"""
        logging("====> MsgOtaCmd <====")
        logging("update_target_version:      " + ota_cmd.update_target_version)
        logging("upgrade_file_download_addr: " + ota_cmd.upgrade_file_download_addr)
        logging("ota_task_id:                " + ota_cmd.ota_task_id)

    @staticmethod
    def __list_msg_ota_cmd_response(ota_cmd_response):
        """OTA升级命令应答 14"""
        logging("====> MsgOtaCmdResponse <====")
        logging("ack:         " + MqttDump.__show_msg_ack(ota_cmd_response.ack))
        logging("ota_task_id: " + ota_cmd_response.ota_task_id)

    @staticmethod
    def __list_msg_ota_cmd_checksum_request(ota_cmd_check_request):
        """OTA文件检验请求 15"""
        logging("====> MsgOtaCmdChecksumRequest <====")
        logging("check_sum_code:             " + ota_cmd_check_request.check_sum_code)
        logging("upgrade_file_download_addr: " + ota_cmd_check_request.upgrade_file_download_addr)
        logging("ota_task_id:                " + ota_cmd_check_request.ota_task_id)

    @staticmethod
    def __list_msg_ota_cmd_checksum_response(ota_cmd_check_response):
        """OTA文件校验应答 16"""
        logging("====> MsgOtaCmdChecksumResponse <====")
        logging("ack:              " + MqttDump.__show_msg_ack(ota_cmd_check_response.ack))
        logging("check_sum_result: " + str(ota_cmd_check_response.check_sum_result))
        logging("ota_task_id:      " + ota_cmd_check_response.ota_task_id)

    @staticmethod
    def __list_msg_ota_result(ota_result):
        """OTA升级结果上报 17"""
        logging("====> MsgOtaResult <====")
        logging("before_upgrade_version: " + ota_result.before_upgrade_version)
        logging("after_upgread_version:  " + ota_result.after_upgread_version)
        logging("result:                 " + MqttDump.__enum_ota_cmd_result_code(ota_result.result))
        logging("upgrade_time:           " + str(datetime.fromtimestamp(ota_result.upgrade_time)))
        logging("ota_task_id:            " + ota_result.ota_task_id)

    @staticmethod
    def __list_msg_diagnosis_response(diagnosis_response):
        """远程诊断结果应答 18"""
        logging("====> MsgDiagnosisResponse <====")
        logging("ack: " + MqttDump.__show_msg_ack(diagnosis_response.ack))
        for result in diagnosis_response.diagnosis_result:
            MqttDump.__show_diagnosis_result(result)

    @staticmethod
    def __list_msg_datamining(datamining):
        """数据采集上报 19"""
        logging("====> MsgDatamining <====")
        logging("None")

    @staticmethod
    def __list_msg_vehicle_status(vehicle_status):
        """车辆状态上报 20"""
        logging("====> MsgVehicleStatus <====")
        logging("lf_door_status:                    " + MqttDump.__enum_on_off_state(vehicle_status.lf_door_status))
        logging("lr_door_status:                    " + MqttDump.__enum_on_off_state(vehicle_status.lr_door_status))
        logging("rf_door_status:                    " + MqttDump.__enum_on_off_state(vehicle_status.rf_door_status))
        logging("rr_door_status:                    " + MqttDump.__enum_on_off_state(vehicle_status.rr_door_status))
        logging("trunk_door_status:                 " + MqttDump.__enum_on_off_state(vehicle_status.trunk_door_status))
        logging("lf_window_status:                  " + MqttDump.__enum_on_off_state(vehicle_status.lf_window_status))
        logging("lr_window_status:                  " + MqttDump.__enum_on_off_state(vehicle_status.lr_window_status))
        logging("rf_window_status:                  " + MqttDump.__enum_on_off_state(vehicle_status.rf_window_status))
        logging("rr_window_status:                  " + MqttDump.__enum_on_off_state(vehicle_status.rr_window_status))
        logging("roof_window_status:                " + MqttDump.__enum_on_off_state(vehicle_status.roof_window_status))
        logging("air_condition_status:              " + MqttDump.__enum_on_off_state(vehicle_status.air_condition_status))
        logging("air_condition_defrost_status:      " + MqttDump.__enum_on_off_state(vehicle_status.air_condition_defrost_status))
        logging("air_condition_rear_defrost_status: " + MqttDump.__enum_on_off_state(vehicle_status.air_condition_rear_defrost_status))
        logging("air_condition_temperature:         " + str(vehicle_status.air_condition_temperature))
        logging("lock_status:                       " + MqttDump.__enum_on_off_state(vehicle_status.lock_status))
        logging("engine_status:                     " + MqttDump.__enum_engine_state(vehicle_status.engine_status))
        logging("wiper_Status:                      " + MqttDump.__enum_on_off_state(vehicle_status.wiper_Status))
        logging("hand_break_status:                 " + MqttDump.__enum_on_off_state(vehicle_status.hand_break_status))
        logging("defrost_mode:                      " + MqttDump.__enum_on_off_state(vehicle_status.defrost_mode))
        logging("peps_power_mode:                   " + MqttDump.__enum_peps_power_mode(vehicle_status.peps_power_mode))
        logging("gear_position:                     " + MqttDump.__enum_gear_position(vehicle_status.gear_position))
        logging("lf_tire_pressure:                  " + str(vehicle_status.lf_tire_pressure))
        logging("lr_tire_pressure:                  " + str(vehicle_status.lr_tire_pressure))
        logging("rf_tire_pressure:                  " + str(vehicle_status.rf_tire_pressure))
        logging("rr_tire_pressure:                  " + str(vehicle_status.rr_tire_pressure))
        logging("battery_voltage:                   " + str(vehicle_status.battery_voltage))
        logging("fuel_level:                        " + str(vehicle_status.fuel_level))
        logging("remain_mileage:                    " + str(vehicle_status.remain_mileage))
        logging("belt:                              " + MqttDump.__enum_on_off_state(vehicle_status.belt))
        logging("front_light:                       " + MqttDump.__enum_on_off_state(vehicle_status.front_light))
        logging("hight_light:                       " + MqttDump.__enum_on_off_state(vehicle_status.hight_light))
        for value in vehicle_status.g_value:
            logging("g_value:                           " + MqttDump.__show_g_value(value))
        logging("light_intensity:                   " + str(vehicle_status.light_intensity))
        logging("current_fuel_consumption:          " + str(vehicle_status.current_fuel_consumption))
        logging("current_speed:                     " + str(vehicle_status.current_speed))
        logging("engine_speed:                      " + str(vehicle_status.engine_speed))
        logging("steering_angle:                    " + str(vehicle_status.steering_angle))
        logging("accelerator_pedal_angle:           " + str(vehicle_status.accelerator_pedal_angle))
        logging("brake_pedal_angle:                 " + str(vehicle_status.brake_pedal_angle))
        logging("clutch_pedal_angle:                " + str(vehicle_status.clutch_pedal_angle))
        logging("total_mileage:                     " + str(vehicle_status.total_mileage))
        logging("gps_info:                          " + MqttDump.__show_gps_info(vehicle_status.gps_info))
        logging("track_status:                      " + MqttDump.__enum_on_off_state(vehicle_status.track_status))
        logging("average_fuel_consumption:          " + str(vehicle_status.average_fuel_consumption))

    @staticmethod
    def __list_msg_alarm_signal(alarm_signal):
        """报警信息上报 21"""
        logging("====> MsgAlarmSignal <====")
        logging("alarm_type:            " + MqttDump.__enum_alarm_signal_type(alarm_signal.alarm_type))
        logging("gps_info:              " + MqttDump.__show_gps_info(alarm_signal.gps_info))
        logging("side_turn_flag:        " + MqttDump.__enum_common_true_false_unknown(alarm_signal.side_turn_flag))
        logging("air_bag_exploded:      " + MqttDump.__enum_common_true_false_unknown(alarm_signal.air_bag_exploded))
        logging("unusual_move_flag:     " + MqttDump.__enum_common_true_false_unknown(alarm_signal.unusual_move_flag))
        logging("anti_theft_alarm_flag: " + MqttDump.__enum_common_true_false_unknown(alarm_signal.anti_theft_alarm_flag))
        logging("crash_info:            " + MqttDump.__enum_crash_info(alarm_signal.crash_info))
        logging("g_sensor_value:        " + MqttDump.__show_gsensor_value(alarm_signal.g_sensor_value))
        logging("window_info:           " + MqttDump.__show_window_info(alarm_signal.window_info))

    @staticmethod
    def __list_msg_push_message(push_message):
        """推送消息下发 22"""
        logging("====> MsgPushMessage <====")
        logging("msg_type:    " + str(push_message.msg_type))
        logging("msg_content: " + str(push_message.msg_content))

    @staticmethod
    def __list_motor_fire_signal(motor_fire_signal):
        """点火熄火上报 23"""
        logging("====> MotorFireSignal <====")
        logging("mode:          " + MqttDump.__enum_motor_fire_mode(motor_fire_signal.mode))
        logging("total_mileage: " + str(motor_fire_signal.total_mileage))
        logging("gps_info:      " + MqttDump.__show_gps_info(motor_fire_signal.gps_info))
        logging("moter_fire_no: " + str(motor_fire_signal.moter_fire_no))

    @staticmethod
    def __list_tracking_data(tracking_data):
        """追踪数据上报 24"""
        logging("====> TrackingData <====")
        logging("gps_info:      " + MqttDump.__show_gps_info(tracking_data.gps))

    @staticmethod
    def dump(msgtop, log=logger.console):
        global logging
        logging = log
        # 通用头，必填字段 01
        if msgtop.HasField("message_head"):
            MqttDump.__list_msg_head(msgtop.message_head)
        # 通用回复消息 02
        if msgtop.HasField("ack"):
            MqttDump.__list_msg_ack(msgtop.ack)
        # 注册请求 03
        if msgtop.HasField("register_request"):
            MqttDump.__list_msg_register_request(msgtop.register_request)
        # 注册回复 04
        if msgtop.HasField("register_response"):
            MqttDump.__list_msg_register_response(msgtop.register_response)
        # 登录请求 05
        if msgtop.HasField("login_request"):
            MqttDump.__list_msg_login_request(msgtop.login_request)
        # 登录回复 06
        if msgtop.HasField("login_response"):
            MqttDump.__list_msg_login_response(msgtop.login_response)
        # 心跳 07
        if msgtop.HasField("heart_beat_response"):
            MqttDump.__list_msg_heartbeat_response(msgtop.heart_beat_response)
        # 远程查询应答 08
        if msgtop.HasField("config_query_response"):
            MqttDump.__list_msg_config_query_response(msgtop.config_query_response)
        # 远程配置下发 09
        if msgtop.HasField("config_request"):
            MqttDump.__list_msg_config_request(msgtop.config_request)
        # 远程配置应答 10
        if msgtop.HasField("config_response"):
            MqttDump.__list_msg_config_response(msgtop.config_response)
        # 远程控制命令下发 11
        if msgtop.HasField("control_cmd"):
            MqttDump.__list_msg_control_request(msgtop.control_cmd)
        # 远程控制结果应答 12
        if msgtop.HasField("control_response"):
            MqttDump.__list_msg_control_response(msgtop.control_response)
        # OTA升级命令下发 13
        if msgtop.HasField("ota_cmd"):
            MqttDump.__list_msg_ota_cmd(msgtop.ota_cmd)
        # OTA升级命令应答 14
        if msgtop.HasField("ota_cmd_response"):
            MqttDump.__list_msg_ota_cmd_response(msgtop.ota_cmd_response)
        # OTA文件校验请求 15
        if msgtop.HasField("ota_cmd_check_request"):
            MqttDump.__list_msg_ota_cmd_checksum_request(msgtop.ota_cmd_check_request)
        # OTA文件校验回复 16
        if msgtop.HasField("ota_cmd_check_response"):
            MqttDump.__list_msg_ota_cmd_checksum_response(msgtop.ota_cmd_check_response)
        # OTA升级结果上报 17
        if msgtop.HasField("ota_result"):
            MqttDump.__list_msg_ota_result(msgtop.ota_result)
        # 远程诊断结果应答 18
        if msgtop.HasField("diagnosis_response"):
            MqttDump.__list_msg_diagnosis_response(msgtop.diagnosis_response)
        # 数据采集上报 19
        if msgtop.HasField("datamining"):
            MqttDump.__list_msg_datamining(msgtop.datamining)
        # 车辆状态上报 20
        if msgtop.HasField("vehicle_status"):
            MqttDump.__list_msg_vehicle_status(msgtop.vehicle_status)
        # 报警信息上报 21
        if msgtop.HasField("alarm_signal"):
            MqttDump.__list_msg_alarm_signal(msgtop.alarm_signal)
        # 推送消息下发 22
        if msgtop.HasField("push_message"):
            MqttDump.__list_msg_push_message(msgtop.push_message)
        # 点火熄火上报 23
        if msgtop.HasField("motor_fire_signal"):
            MqttDump.__list_motor_fire_signal(msgtop.motor_fire_signal)
        # 追踪数据上报 24
        if msgtop.HasField("tracking_data"):
            MqttDump.__list_tracking_data(msgtop.tracking_data)
