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
    def __enum_equipment_id_type(id_type):
        """设备编号类型"""
        type_dict = {
            0: "PDID",
            1: "VIN",
            2: "IMEI",
            3: "ICCID",
        }
        return type_dict[id_type]

    @staticmethod
    def __enum_msg_type(msg_type):
        """消息类型"""
        type_dict = {
            0: "TYPE0",
            1: "TYPE1",
            2: "REGISTER_REQUEST",
            3: "REGISTER_RESPONSE",
            4: "LOGIN",
            5: "LOGIN_RESPONSE",
            6: "HEART_BEAT_RESPONSE",
            7: "REMOTE_CONFIG_RESPONSE",
            8: "REMOTE_CONFIG_REQUEST",
            9: "REMOTE_CONFIG_RESULT",
            10: "REMOTE_CONTROL_CMD",
            11: "REMOTE_CONTROL_RESPONSE",
            12: "OTA_CMD",
            13: "OTA_CMD_RESPONSE",
            14: "OTA_CMD_CHECK_REQUEST",
            15: "OTA_CMD_CHECK_RESPONSE",
            16: "OTA_RESULT",
            17: "OTA_RESULT_RESPONSE",
            18: "REMOTE_DIAGNOSIS_RESPONSE",
            19: "REMOTE_DIAGNOSIS_RESULT",
            20: "DATAMINING",
            21: "VEHICLE_STATUS",
            22: "ALARM_SIGNAL",
            23: "ALARM_SIGNAL_RESPONSE",
            24: "PUSH_MESSAGE",
            25: "MOTOR_FIRE_SIGNAL",
            26: "COMMON_ACK",
            101: "HEART_BEAT",
            102: "LOGOUT",
            103: "REMOTE_CONFIG_QUERY_REQUEST",
            104: "REMOTE_DIAGNOSIS_REQUEST",
            105: "VEHICLE_STATUS_REQUEST",
        }
        return type_dict[msg_type]

    @staticmethod
    def __enum_common_ack_code(code):
        """通用的消息回复码"""
        code_dict = {
            0: "SUCCESS",
            1: "FAILED",
            2: "NOT_LOGIN",
            3: "MESSAGE_PARSE_ERROR",
        }
        return code_dict[code]

    @staticmethod
    def __enum_remote_config_item(item):
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
        }
        return item_dict[item]

    @staticmethod
    def __enum_remote_config_error_code(code):
        """远程配置错误码"""
        code_dict = {
            0: "UNKNOW",
        }
        return code_dict[code]

    @staticmethod
    def __enum_remote_control_cmd_type(cmd_type):
        """远程控制命令类型"""
        type_dict = {
            0: "ENGINE",
            1: "AIR_CONDITION_CTRL",
            2: "LOCK",
            3: "FIND_VEHICLE",
        }
        return type_dict[cmd_type]

    @staticmethod
    def __enum_remote_control_execute_result(result):
        """远程控制执行结果"""
        result_dict = {
            0: "FAILED",
            1: "SUCCESS",
        }
        return result_dict[result]

    @staticmethod
    def __enum_ota_cmd_result_code(code):
        """OTA升级命令执行结果码"""
        code_dict = {
            0: "UPGRADE_FAILED",
            1: "UPGRADE_SUCCESSED",
            2: "DOWNLOAD_FILE_FAILED",
            3: "OTA_IN_PROCESS",
        }
        return code_dict[code]

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
        return mode_dict[mode]

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
        return info_dict[info]

    @staticmethod
    def __enum_common_true_false_unknown(msg):
        """通用TRUE FALSE UNKNOWN"""
        msg_dict = {
            0: "FALSE",
            1: "TRUE",
            2: "UNKNOWN",
        }
        return msg_dict[msg]

    @staticmethod
    def __enum_alarm_signal_type(signal_type):
        """报警信号信息"""
        type_dict = {
            0: "AIR_BAG",
            1: "SIDE_TURN",
            2: "UNUSUAL_MOVE",
            3: "ANTI_THEFT",
            4: "VEHICLE_CRASH",
        }
        return type_dict[signal_type]

    @staticmethod
    def __enum_on_off_state(state):
        """on/off状态"""
        state_dict = {
            0: "UNKNOWN",
            1: "OFF",
            2: "ON"
        }
        return state_dict[state]

    @staticmethod
    def __enum_engine_state(state):
        """引擎状态"""
        state_dict = {
            0: "UNKNOWN",
            1: "KEYOFF",
            2: "KEYON",
            3: "CRANK",
            4: "RUNNING"
        }
        return state_dict[state]

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
        return pos_dict[pos]

    @staticmethod
    def __enum_motor_fire_mode(mode):
        """点火熄火状态"""
        mode_dict = {
            0: "IGNITION",
            1: "FLAMEOUT",
        }
        return mode_dict[mode]

    @staticmethod
    def __show_common_ack(ack_code):
        msg = "{" \
              + "ack_code:" + MqttDump.__enum_common_ack_code(ack_code.ack_code) \
              + ", code_desp:" + ack_code.code_desp \
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
              + "}"
        return msg

    @staticmethod
    def __show_remote_config_data(remote_config_data):
        msg = "{" \
              + "mqtt_server_addr:" + remote_config_data.mqtt_server_addr \
              + ", mqtt_server_topic:" + remote_config_data.mqtt_server_topic \
              + ", mqtt_key_business_server_addr:" + remote_config_data.mqtt_key_business_server_addr \
              + ", mqtt_key_business_server_topic:" + remote_config_data.mqtt_key_business_server_topic \
              + ", ecall_number:" + remote_config_data.ecall_number \
              + ", bcall_number:" + remote_config_data.bcall_number \
              + ", icall_number:" + remote_config_data.icall_number \
              + ", ecall_enable:" + str(remote_config_data.ecall_enable) \
              + ", bcall_enable:" + str(remote_config_data.bcall_enable) \
              + ", icall_enable:" + str(remote_config_data.icall_enable) \
              + ", sms_gate_number_upload:" + remote_config_data.sms_gate_number_upload \
              + ", sms_gate_number_download:" + remote_config_data.sms_gate_number_download \
              + ", datamining_upload_frequency:" + str(remote_config_data.datamining_upload_frequency) \
              + ", vehicle_status_upload_frequency:" + str(remote_config_data.vehicle_status_upload_frequency) \
              + ", ignition_blowout_upload_enable:" + str(remote_config_data.ignition_blowout_upload_enable) \
              + ", upload_alert_enable:" + str(remote_config_data.upload_alert_enable) \
              + ", datamining_enable:" + str(remote_config_data.datamining_enable) \
              + ", svt_enable:" + str(remote_config_data.svt_enable) \
              + ", eletronic_defense_enable:" + str(remote_config_data.eletronic_defense_enable) \
              + ", abnormal_move_threshold_value:" + str(remote_config_data.abnormal_move_threshold_value) \
              + "}"
        return msg

    @staticmethod
    def __show_remote_config_result(config_results):
        msg = "{" \
              + "config_item:" + MqttDump.__enum_remote_config_item(config_results.config_item) \
              + ", result:" + str(config_results.result) \
              + ", error_code:" + MqttDump.__enum_remote_config_error_code(config_results.error_code) \
              + "}"
        return msg

    @staticmethod
    def __show_air_condition_control_parameter(ac_parameter):
        msg = "{" \
              + "ac_switch:" + str(ac_parameter.ac_switch) \
              + ", ac_temperature:" + str(ac_parameter.ac_temperature) \
              + ", ac_front_defrost:" + str(ac_parameter.ac_front_defrost) \
              + ", ac_rear_defrost:" + str(ac_parameter.ac_rear_defrost) \
              + "}"
        return msg

    @staticmethod
    def __show_remote_control_response_vehice_info(vehicle_info):
        msg = "{" \
              + "air_condition_status:" + MqttDump.__enum_on_off_state(vehicle_info.air_condition_status) \
              + ", air_condition_defrost_status:" + MqttDump.__enum_on_off_state(vehicle_info.air_condition_defrost_status) \
              + ", air_condition_rear_defrost_status" + MqttDump.__enum_on_off_state(vehicle_info.air_condition_rear_defrost_status) \
              + ", air_condition_temperature:" + str(vehicle_info.air_condition_temperature) \
              + ", lock_status:" + MqttDump.__enum_on_off_state(vehicle_info.lock_status) \
              + ", engine_status:" + MqttDump.__enum_engine_state(vehicle_info.engine_status) \
              + ", hand_brake_status:" + MqttDump.__enum_on_off_state(vehicle_info.hand_break_status) \
              + ", peps_power_mode:" + MqttDump.__enum_peps_power_mode(vehicle_info.peps_power_mode) \
              + ", gear_position:" + MqttDump.__enum_gear_position(vehicle_info.gear_position) \
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
    def __show_gsensor_value(value):
        msg = "{" \
              + "x:" + str(value.x) \
              + ", y:" + str(value.y) \
              + ", z:" + str(value.z) \
              + "}"
        return msg

    @staticmethod
    def __list_common_head(common_head):
        """通用头，必填字段"""
        logging("====> CommonHead <====")
        logging("protocol_version:     " + str(common_head.protocol_version))
        logging("equipment_id_type:    " + MqttDump.__enum_equipment_id_type(common_head.equipment_id_type))
        logging("equipment_id:         " + common_head.equipment_id)
        logging("message_id:           " + str(common_head.message_id))
        logging("msg_type:             " + MqttDump.__enum_msg_type(common_head.msg_type))
        logging("message_create_time:  " + str(datetime.fromtimestamp(common_head.message_create_time)))
        logging("token:                " + common_head.token)
        logging("flag:                 " + str(common_head.flag))

    @staticmethod
    def __list_extra_common_head(common_head):
        """通用头，必填字段"""
        print("====> CommonHead <====")
        print("protocol_version:     " + str(common_head.protocol_version))
        print("equipment_id_type:    " + MqttDump.__enum_equipment_id_type(common_head.equipment_id_type))
        print("equipment_id:         " + common_head.equipment_id)
        print("message_id:           " + str(common_head.message_id))
        print("msg_type:             " + MqttDump.__enum_msg_type(common_head.msg_type))
        print("message_create_time:  " + str(datetime.fromtimestamp(common_head.message_create_time)))
        print("token:                " + common_head.token)
        print("flag:                 " + str(common_head.flag))

    @staticmethod
    def __list_msg_register_request(register_request):
        """注册请求消息（在工厂模式下） 01"""
        logging("====> MsgRegisterRequest <====")
        logging("pdid:         " + register_request.pdid)
        logging("iccid:        " + register_request.iccid)
        logging("tbox_version: " + register_request.tbox_version)

    @staticmethod
    def __list_msg_register_response(register_response):
        """注册请求应答（在工厂模式下） 02"""
        logging("====> MsgRegisterResponse <====")
        logging("res_code:   " + str(register_response.res_code))
        logging("addr:       " + register_response.addr)
        logging("ca_cer:     " + register_response.ca_cer)
        logging("custom_cer: " + register_response.custom_cer)

    @staticmethod
    def __list_msg_login(login):
        """登录请求 03"""
        logging("====> MsgLogIn <====")
        logging("pdid:        " + login.pdid)
        logging("iccid:       " + login.iccid)
        logging("vin:         " + login.vin)
        logging("version:     " + login.version)
        logging("release_tag: " + login.release_tag)

    @staticmethod
    def __list_msg_log_in_response(login_response):
        """登录回复 04"""
        logging("====> MsgLogInResponse <====")
        logging("ack_code: " + MqttDump.__show_common_ack(login_response.ack_code))
        logging("token:    " + login_response.token)

    # 链路检测 05 无消息体

    @staticmethod
    def __list_msg_heart_beat_response(heart_beat_response):
        """链路检测回复 06"""
        logging("====> MsgHeartBeatResponse <====")
        logging("ack_code: " + MqttDump.__show_common_ack(heart_beat_response.ack_code))

    # 登出 07 无消息体

    # 远程查询配置请求 08 无消息体

    @staticmethod
    def __list_msg_remote_config_response(remote_config_response):
        """远程查询配置回复 09"""
        logging("====> MsgRemoteConfigResponse <====")
        logging("ack_code:           " + MqttDump.__show_common_ack(remote_config_response.ack_code))
        logging("remote_config_data: " + MqttDump.__show_remote_config_data(remote_config_response.remote_config_data))

    @staticmethod
    def __list_msg_remote_config_request(remote_config_request):
        """远程配置请求 10"""
        logging("====> MsgRemoteConfigRequest <====")
        for item in remote_config_request.config_items:
            logging("config_items: " + MqttDump.__enum_remote_config_item(item))
        logging("config_data:  " + MqttDump.__show_remote_config_data(remote_config_request.config_data))

    @staticmethod
    def __list_msg_remote_config_result(remote_config_result):
        """远程配置回复 11"""
        print("====> MsgRemoteConfigResult <====")
        print("ack_code:       " + MqttDump.__show_common_ack(remote_config_result.ack_code))
        for result in remote_config_result.config_results:
            print("config_results: " + MqttDump.__show_remote_config_result(result))
        print("config_old:     " + MqttDump.__show_remote_config_data(remote_config_result.config_old))
        print("config_new:     " + MqttDump.__show_remote_config_data(remote_config_result.config_new))

    @staticmethod
    def __list_msg_remote_control_cmd(remote_control_cmd):
        """远程控制命令 12"""
        logging("====> MsgRemoteControlCmd <====")
        logging("cmd:              " + MqttDump.__enum_remote_control_cmd_type(remote_control_cmd.cmd))
        logging("ac_parameter:     " + MqttDump.__show_air_condition_control_parameter(remote_control_cmd.ac_parameter))
        logging("engine_parameter: " + str(remote_control_cmd.engine_parameter))
        logging("lock_parameter:   " + str(remote_control_cmd.lock_parameter))

    @staticmethod
    def __list_msg_remote_control_response(remote_control_response):
        """远程控制结果 13"""
        print("====> MsgRemoteControlResponse <====")
        print("ack_code:      " + MqttDump.__show_common_ack(remote_control_response.ack_code))
        print("excute_result: " + MqttDump.__enum_remote_control_execute_result(remote_control_response.excute_result))
        print("error_code:    " + remote_control_response.error_code)
        print("gps_info:      " + MqttDump.__show_gps_info(remote_control_response.gps_info))
        print("vehicle_info:  " + MqttDump.__show_remote_control_response_vehice_info(remote_control_response.vehicle_info))

    @staticmethod
    def __list_msg_ota_cmd(ota_cmd):
        """OTA升级命令 14"""
        logging("====> MsgOtaCmd <====")
        logging("update_target_version:      " + ota_cmd.update_target_version)
        logging("upgrade_file_download_addr: " + ota_cmd.upgrade_file_download_addr)
        logging("ota_task_id:                " + ota_cmd.ota_task_id)

    @staticmethod
    def __list_msg_ota_cmd_response(ota_cmd_response):
        """OTA升级命令回复 15"""
        logging("====> MsgOtaCmdResponse <====")
        logging("ack_code:    " + MqttDump.__show_common_ack(ota_cmd_response.ack_code))
        logging("ota_task_id: " + ota_cmd_response.ota_task_id)

    @staticmethod
    def __list_msg_ota_cmd_checksum_request(ota_cmd_check_request):
        """OTA升级文件checksum检查请求 16"""
        logging("====> MsgOtaCmdCheckSumRequest <====")
        logging("check_sum_code:             " + ota_cmd_check_request.check_sum_code)
        logging("upgrade_file_download_addr: " + ota_cmd_check_request.upgrade_file_download_addr)
        logging("ota_task_id:                " + ota_cmd_check_request.ota_task_id)

    @staticmethod
    def __list_msg_ota_cmd_checksum_response(ota_cmd_check_response):
        """OTA升级后台检查升级文件应答 17"""
        logging("====> MsgOtaCmdCheckSumResponse <====")
        logging("ack_code:         " + MqttDump.__show_common_ack(ota_cmd_check_response.ack_code))
        logging("check_sum_result: " + str(ota_cmd_check_response.check_sum_result))
        logging("ota_task_id:      " + ota_cmd_check_response.ota_task_id)

    @staticmethod
    def __list_msg_ota_result(ota_result):
        """OTA升级结果 18"""
        logging("====> MsgOtaResult <====")
        logging("before_upgrade_version: " + ota_result.before_upgrade_version)
        logging("after_upgread_version:  " + ota_result.after_upgread_version)
        logging("result:                 " + MqttDump.__enum_ota_cmd_result_code(ota_result.result))
        logging("upgrade_time:           " + str(ota_result.upgrade_time))
        logging("ota_task_id:            " + ota_result.ota_task_id)

    @staticmethod
    def __list_msg_ota_result_response(ota_result_response):
        """OTA升级结果应答 19"""
        logging("====> MsgOtaResultResponse <====")
        logging("ack_code:    " + MqttDump.__show_common_ack(ota_result_response.ack_code))
        logging("ota_task_id: " + ota_result_response.ota_task_id)

    # 远程诊断命令下发 20 无消息体

    @staticmethod
    def __list_msg_remote_diagnosis_response(remote_diagnosis_response):
        """远程诊断命令收到回复 21"""
        logging("====> MsgRemoteDiagnosisResponse <====")
        logging("ack_code: " + MqttDump.__show_common_ack(remote_diagnosis_response.ack_code))

    @staticmethod
    def __list_msg_remote_diagnosis_result(remote_diagnosis_result):
        """诊断命令结果 22"""
        logging("====> MsgRemoteDiagnosisResult <====")
        for result in remote_diagnosis_result.diagnosis_result:
            logging("diagnosis_result: " + MqttDump.__show_diagnosis_result(result))

    @staticmethod
    def __list_msg_datamining(datamining):
        """即时上报数据信息 23 高频数据"""
        logging("====> MsgDatamining <====")
        logging("current_fuel_consumption:" + str(datamining.current_fuel_consumption))
        logging("coordinate:              " + MqttDump.__show_gps_info(datamining.coordinate))
        logging("total_mileage:           " + str(datamining.total_mileage))
        logging("current_speed:           " + str(datamining.current_speed))
        logging("engine_speed:            " + str(datamining.engine_speed))
        logging("steering_angle:          " + str(datamining.steering_angle))
        logging("accelerator_pedal_angle: " + str(datamining.accelerator_pedal_angle))
        logging("brake_pedal_angle:       " + str(datamining.brake_pedal_angle))
        logging("clutch_pedal_angle:      " + str(datamining.clutch_pedal_angle))

    @staticmethod
    def __list_msg_vehicle_status(vehicle_status):
        """车辆状态上报数据 24 低频数据"""
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

    # 查询车辆状态 25 无消息体

    @staticmethod
    def __list_msg_alarm_signal(alarm_signal):
        """异动，防盗报警，车辆侧翻，气囊爆开，碰撞等信号上报 26"""
        logging("====> MsgAlarmSignal <====")
        logging("alarm_signal_type:     " + MqttDump.__enum_alarm_signal_type(alarm_signal.alarm_signal_type))
        logging("gps_info:              " + MqttDump.__show_gps_info(alarm_signal.gps_info))
        logging("side_turn_flag:        " + MqttDump.__enum_common_true_false_unknown(alarm_signal.side_turn_flag))
        logging("air_bag_exploded:      " + MqttDump.__enum_common_true_false_unknown(alarm_signal.air_bag_exploded))
        logging("unusual_move_flag:     " + MqttDump.__enum_common_true_false_unknown(alarm_signal.unusual_move_flag))
        logging("anti_theft_alarm_flag: " + MqttDump.__enum_common_true_false_unknown(alarm_signal.anti_theft_alarm_flag))
        logging("crash_info:            " + MqttDump.__enum_crash_info(alarm_signal.crash_info))
        logging("g_sensor_value:        " + MqttDump.__show_gsensor_value(alarm_signal.g_sensor_value))

    @staticmethod
    def __list_msg_alarm_signal_response(alarm_signal_response):
        """异动，防盗报警，车辆侧翻，气囊爆开，碰撞等信号上报回复 27"""
        logging("====> MsgAlarmSignalResponse <====")
        logging("ack_code: " + MqttDump.__enum_common_ack_code(alarm_signal_response.ack_code))

    @staticmethod
    def __list_msg_push_message(push_message):
        """推送消息 28"""
        logging("====> MsgPushMessage <====")
        logging("msg_type:    " + str(push_message.msg_type))
        logging("msg_content: " + str(push_message.msg_content))

    @staticmethod
    def __list_motor_fire_signal(motor_fire_signal):
        """点火熄火信号 29"""
        logging("====> MotorFireSignal <====")
        logging("fire_signal:   " + MqttDump.__enum_motor_fire_mode(motor_fire_signal.fire_signal))
        logging("total_mileage: " + str(motor_fire_signal.total_mileage))
        logging("gps_info:      " + MqttDump.__show_gps_info(motor_fire_signal.gps_info))
        logging("moter_fire_no: " + str(motor_fire_signal.moter_fire_no))

    @staticmethod
    def __list_common_ack(common_ack):
        """通用回复消息"""
        logging("====> CommonAck <====")
        logging("common_ack: " + MqttDump.__show_common_ack(common_ack))

    @staticmethod
    def dump(msgtop, log=logger.console):
        global logging
        logging = log
        # 通用头，必填字段
        if msgtop.HasField("message_head"):
            MqttDump.__list_common_head(msgtop.message_head)
        # 注册请求消息（在工厂模式下） 01
        if msgtop.HasField("register_request"):
            MqttDump.__list_msg_register_request(msgtop.register_request)
        # 注册请求应答（在工厂模式下） 02
        if msgtop.HasField("register_response"):
            MqttDump.__list_msg_register_response(msgtop.register_response)
        # 登录请求 03
        if msgtop.HasField("login"):
            MqttDump.__list_extra_common_head(msgtop.message_head)
            MqttDump.__list_msg_login(msgtop.login)
        # 登录回复 04
        if msgtop.HasField("login_response"):
            MqttDump.__list_msg_log_in_response(msgtop.login_response)
        # 链路检测 05 无消息体
        # 链路检测回复 06
        if msgtop.HasField("heart_beat_response"):
            MqttDump.__list_msg_heart_beat_response(msgtop.heart_beat_response)
        # 登出 07 无消息体
        # 远程查询配置请求 08 无消息体
        # 远程查询配置回复 09
        if msgtop.HasField("remote_config_response"):
            MqttDump.__list_msg_remote_config_response(msgtop.remote_config_response)
        # 远程配置请求 10
        if msgtop.HasField("remote_config_request"):
            MqttDump.__list_msg_remote_config_request(msgtop.remote_config_request)
        # 远程配置回复 11
        if msgtop.HasField("remote_config_result"):
            MqttDump.__list_extra_common_head(msgtop.message_head)
            MqttDump.__list_msg_remote_config_result(msgtop.remote_config_result)
        # 远程控制命令 12
        if msgtop.HasField("remote_control_cmd"):
            MqttDump.__list_msg_remote_control_cmd(msgtop.remote_control_cmd)
        # 远程控制结果 13
        if msgtop.HasField("remote_control_response"):
            MqttDump.__list_msg_remote_control_response(msgtop.remote_control_response)
        # OTA升级命令 14
        if msgtop.HasField("MsgOtaCmd"):
            MqttDump.__list_msg_ota_cmd(msgtop.ota_cmd)
        # OTA升级命令回复 15
        if msgtop.HasField("ota_cmd_response"):
            MqttDump.__list_msg_ota_cmd_response(msgtop.ota_cmd_response)
        # OTA升级文件checksum检查请求 16
        if msgtop.HasField("ota_cmd_check_request"):
            MqttDump.__list_msg_ota_cmd_checksum_request(msgtop.ota_cmd_check_request)
        # OTA升级后台检查升级文件应答 17
        if msgtop.HasField("ota_cmd_check_response"):
            MqttDump.__list_msg_ota_cmd_checksum_response(msgtop.ota_cmd_check_response)
        # OTA升级结果 18
        if msgtop.HasField("ota_result"):
            MqttDump.__list_msg_ota_result(msgtop.ota_result)
        # OTA升级结果应答 19
        if msgtop.HasField("ota_result_response"):
            MqttDump.__list_msg_ota_result_response(msgtop.ota_result_response)
        # 远程诊断命令下发 20 无消息体
        # 远程诊断命令收到回复 21
        if msgtop.HasField("remote_diagnosis_response"):
            MqttDump.__list_extra_common_head(msgtop.message_head)
            MqttDump.__list_msg_remote_diagnosis_response(msgtop.remote_diagnosis_response)
        # 诊断命令结果 22
        if msgtop.HasField("remote_diagnosis_result"):
            MqttDump.__list_msg_remote_diagnosis_result(msgtop.remote_diagnosis_result)
        # 即时上报数据信息 23 高频数据
        if msgtop.HasField("datamining"):
            MqttDump.__list_msg_datamining(msgtop.datamining)
        # 车辆状态上报数据 24 低频数据
        if msgtop.HasField("vehicle_status"):
            MqttDump.__list_msg_vehicle_status(msgtop.vehicle_status)
        # 查询车辆状态 25 无消息体
        # 异动，防盗报警，车辆侧翻，气囊爆开，碰撞等信号上报 26
        if msgtop.HasField("alarm_signal"):
            MqttDump.__list_extra_common_head(msgtop.message_head)
            MqttDump.__list_msg_alarm_signal(msgtop.alarm_signal)
        # 异动，防盗报警，车辆侧翻，气囊爆开，碰撞等信号上报回复 27
        if msgtop.HasField("alarm_signal_response"):
            MqttDump.__list_msg_alarm_signal_response(msgtop.alarm_signal_response)
        # 推送消息 28
        if msgtop.HasField("push_message"):
            MqttDump.__list_msg_push_message(msgtop.push_message)
        # 点火熄火信号 29
        if msgtop.HasField("motor_fire_signal"):
            MqttDump.__list_motor_fire_signal(msgtop.motor_fire_signal)
        # 通用回复消息
        if msgtop.HasField("common_ack"):
            MqttDump.__list_common_ack(msgtop.common_ack)
