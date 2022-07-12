#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import socket
import threading
from ekt_streamxpress_lib import StreamXpress
from ekt_rds_lib import *
from read_atserver_ini import GetATserverIni
import logging
import shutil
import re

# logging.basicConfig(level=logging.NOTSET)
# log = logging.getLogger("Linux_ATServer")

# # get local ip
# addrs = socket.getaddrinfo(socket.gethostname(), None)
# for item in addrs:
#     if str(item[-1][0])[0:3] == "192":
#         ip = str(item[-1][0])
#         print("current ip is : {}".format(ip))


log_dirs = './linux_atserver_log/'
if not os.path.exists(log_dirs):
    os.makedirs(log_dirs)

logging.basicConfig(level=logging.INFO,  # 控制台打印的日志级别
                    filename='./linux_atserver_log/{}.log'.format(time.strftime('%Y-%m-%d')),
                    filemode='a',  ##模式,有w和a,w就是写模式,每次都会重新写日志,覆盖之前的日志
                    # a是追加模式,默认如果不写的话,就是追加模式
                    format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')  # 日志格式

wsdl_path = r"./SpRc.wsdl"
com_name = 'COM4'
baud_rate = 115200
timeout = 5

streamxpress = StreamXpress(wsdl_path)
rdsp = EktRdsp(com_name, baud_rate, timeout=timeout)

ip = "192.168.1.41"
port = 8900


def is_int_number(s):
    "可以正确分辨数值型字符串"
    try:  # 如果能运行float(s)语句，返回True（字符串s是整数数）
        int(s)
        return True
    except ValueError:  # ValueError为Python的一种标准异常，表示"传入无效的参数"
        return False  # 如果引发了ValueError这种异常，不做任何事情（pass：不做任何事情，一般用做占位语句）


class Linux_ATServer():
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def response(self):
        server = self.server
        server.bind((ip, port))
        server.listen(5)
        while True:
            conn, addr = server.accept()
            print("%s connected" % str(addr))
            logging.info("%s connected" % str(addr))
            while True:
                # try:

                data = conn.recv(1024)
                print "receive data   " + repr(data)
                logging.info("receive data   " + repr(data))

                print(type(data), "-" * 50, data)
                print(time.strftime('%Y-%m-%d-%H-%M-%S'))
                if not data:
                    break

                elif data[:10] == ":DTA:TYPE ":
                    list_split_data = data.split()
                    if len(list_split_data) == 3:
                        pass
                    else:
                        conn.send("send data format err, data    {}".format(data))
                        continue
                    type_data = list_split_data[1]
                    mod = list_split_data[2]
                    # print type_data, mod
                    rec_data = streamxpress.set_device(type_data, mod)
                    logging.info("streamxpress receive data   " + repr(rec_data))
                    if rec_data.get("result") is True:
                        conn.send("{}SUCCESS".format(data[:10]))
                    else:
                        conn.send("send data format err, data    {}".format(data))

                elif data[:10] == ":DTA:FREQ ":
                    list_split_data = data.split()
                    if len(list_split_data) == 2:
                        pass
                    else:
                        conn.send("send data format err, data    {}".format(data))
                        continue
                    freq = list_split_data[1]
                    # print freq
                    rec_data = streamxpress.set_freq(freq)
                    logging.info("streamxpress receive data   " + repr(rec_data))
                    if rec_data.get("result") is True:
                        conn.send("{}SUCCESS".format(data[:10]))
                    else:
                        conn.send("send data format err, data    {}".format(data))

                elif data[:12] == ":DTA:TSRATE ":
                    list_split_data = data.split()
                    if len(list_split_data) == 2:
                        pass
                    else:
                        conn.send("send data format err, data    {}".format(data))
                        continue
                    rate = list_split_data[1]
                    # print rate
                    rec_data = streamxpress.set_tsrate(rate)
                    logging.info("streamxpress receive data   " + repr(rec_data))
                    if rec_data.get("result") is True:
                        conn.send("{}SUCCESS".format(data[:12]))
                    else:
                        conn.send("send data format err, data    {}".format(data))

                elif data[:13] == ":DTA:SYMRATE ":
                    list_split_data = data.split()
                    if len(list_split_data) == 2:
                        pass
                    else:
                        conn.send("send data format err, data    {}".format(data))
                        continue
                    rate = list_split_data[1]
                    # print rate
                    rec_data = streamxpress.set_sym_rate(rate)
                    logging.info("streamxpress receive data   " + repr(rec_data))
                    if rec_data.get("result") is True:
                        conn.send("{}SUCCESS".format(data[:13]))
                    else:
                        conn.send("send data format err, data    {}".format(data))

                elif data[:15] == ":DTA:BANDWIDTH ":
                    list_split_data = data.split()
                    if len(list_split_data) == 2:
                        pass
                    else:
                        conn.send("send data format err, data    {}".format(data))
                        continue
                    bandwidth = list_split_data[1]
                    rec_data = streamxpress.set_bandwidth(bandwidth)
                    logging.info("streamxpress receive data   " + repr(rec_data))
                    if rec_data.get("result") is True:
                        conn.send("{}SUCCESS".format(data[:15]))
                    else:
                        conn.send("send data format err, data    {}".format(data))

                elif data[:11] == ":DTA:LEVEL ":
                    list_split_data = data.split()
                    if len(list_split_data) == 2:
                        pass
                    else:
                        conn.send("send data format err, data    {}".format(data))
                        continue
                    level = list_split_data[1]
                    rec_data = streamxpress.set_output_level(level)
                    logging.info("streamxpress receive data   " + repr(rec_data))
                    if rec_data.get("result") is True:
                        conn.send("{}SUCCESS".format(data[:11]))
                    else:
                        conn.send("send data format err, data    {}".format(data))

                elif data[:14] == ":DTA:SET_DVBS ":
                    list_split_data = data.split()
                    if len(list_split_data) == 5:
                        pass
                    else:
                        conn.send("send data format err, data    {}".format(data))
                        continue
                    type_data = list_split_data[1]
                    freq = list_split_data[2]
                    symbol_rate = list_split_data[3]
                    code_rate = list_split_data[4]
                    rec_data = streamxpress.set_dvbs(type_data, freq, symbol_rate, code_rate)
                    logging.info("streamxpress receive data   " + repr(rec_data))
                    if rec_data.get("result") is True:
                        conn.send("{}SUCCESS".format(data[:14]))
                    else:
                        conn.send("send data format err, data    {}".format(data))

                elif data[:14] == ":DTA:SET_DVBS ":
                    list_split_data = data.split()
                    if len(list_split_data) == 5:
                        pass
                    else:
                        conn.send("send data format err, data    {}".format(data))
                        continue
                    type_data = list_split_data[1]
                    freq = list_split_data[2]
                    symbol_rate = list_split_data[3]
                    code_rate = list_split_data[4]
                    rec_data = streamxpress.set_dvbs(type_data, freq, symbol_rate, code_rate)
                    logging.info("streamxpress receive data   " + repr(rec_data))
                    if rec_data.get("result") is True:
                        conn.send("{}SUCCESS".format(data[:14]))
                    else:
                        conn.send("send data format err, data    {}".format(data))

                elif data[:14] == ":DTA:SET_DVBC ":
                    list_split_data = data.split()
                    if len(list_split_data) == 5:
                        pass
                    else:
                        conn.send("send data format err, data    {}".format(data))
                        continue
                    type_data = list_split_data[1]
                    freq = list_split_data[2]
                    annex = list_split_data[3]
                    symbol_rate = list_split_data[4]
                    rec_data = streamxpress.set_dvbc(type_data, freq, annex, symbol_rate)
                    logging.info("streamxpress receive data   " + repr(rec_data))
                    if rec_data.get("result") is True:
                        conn.send("{}SUCCESS".format(data[:14]))
                    else:
                        conn.send("send data format err, data    {}".format(data))

                elif data[:14] == ":DTA:SET_DVBT ":
                    list_split_data = data.split()
                    if len(list_split_data) == 5:
                        pass
                    else:
                        conn.send("send data format err, data    {}".format(data))
                        continue
                    type_data = list_split_data[1]
                    freq = list_split_data[2]
                    bandwidth = list_split_data[3]
                    code_rate = list_split_data[4]
                    rec_data = streamxpress.set_dvbt(type_data, freq, bandwidth, code_rate)
                    logging.info("streamxpress receive data   " + repr(rec_data))
                    if rec_data.get("result") is True:
                        conn.send("{}SUCCESS".format(data[:14]))
                    else:
                        conn.send("send data format err, data    {}".format(data))

                elif data[:10] == ":DTA:FILE ":
                    list_split_data = data.split()
                    if len(list_split_data) == 3:
                        pass
                    else:
                        conn.send("send data format err, data    {}".format(data))
                        continue
                    file = list_split_data[1]
                    flag = list_split_data[2]
                    rec_data = streamxpress.set_file(file, flag)
                    logging.info("streamxpress receive data   " + repr(rec_data))
                    if rec_data.get("result") is True:
                        conn.send("{}SUCCESS".format(data[:10]))
                    else:
                        conn.send("send data format err, data    {}".format(data))

                # todo Interface unavailable
                elif data[:11] == ":DTA:REMUX ":
                    list_split_data = data.split()
                    if len(list_split_data) == 2:
                        pass
                    else:
                        conn.send("send data format err, data    {}".format(data))
                        continue
                    flag = list_split_data[1]
                    rec_data = streamxpress.set_remux(flag)
                    logging.info("streamxpress receive data   " + repr(rec_data))
                    if rec_data.get("result") is True:
                        conn.send("{}SUCCESS".format(data[:11]))
                    else:
                        conn.send("send data format err, data    {}".format(data))

                elif data == ":DTA:PLAY \r\n":
                    rec_data = streamxpress.play()
                    logging.info("streamxpress receive data   " + repr(rec_data))
                    if rec_data.get("result") is True:
                        conn.send("{}SUCCESS".format(data[:10]))
                    else:
                        conn.send("send data format err, data    {}".format(data))

                elif data == ":DTA:PAUSE \r\n":
                    rec_data = streamxpress.pause()
                    logging.info("streamxpress receive data   " + repr(rec_data))
                    if rec_data.get("result") is True:
                        conn.send("{}SUCCESS".format(data[:11]))
                    else:
                        conn.send("send data format err, data    {}".format(data))

                elif data == ":DTA:STOP \r\n":
                    rec_data = streamxpress.stop()
                    logging.info("streamxpress receive data   " + repr(rec_data))
                    if rec_data.get("result") is True:
                        conn.send("{}SUCCESS".format(data[:10]))
                    else:
                        conn.send("send data format err, data    {}".format(data))

                elif data == ':DTA:RF_ENABLED_ON_STOP 1\r\n':
                    rec_data = streamxpress.rf_enabled_on_stop()
                    logging.info("streamxpress receive data   " + repr(rec_data))
                    if rec_data.get("result") is True:
                        conn.send("{}SUCCESS".format(data[:24]))
                    else:
                        conn.send("send data format err, data    {}".format(data))

                elif data == ':DTA:RF_ENABLED_ON_STOP 0\r\n':
                    rec_data = streamxpress.rf_disabled_on_stop()
                    logging.info("streamxpress receive data   " + repr(rec_data))
                    if rec_data.get("result") is True:
                        conn.send("{}SUCCESS".format(data[:24]))
                    else:
                        conn.send("send data format err, data    {}".format(data))

                elif data == ":DTA:TOTAL_TIME 1\r\n":
                    rec_data = streamxpress.get_stream_total_time()
                    logging.info("streamxpress receive data   " + repr(rec_data))
                    if rec_data.get("result") is True:
                        conn.send("{}{}".format(data[:16], rec_data.get("TimeLoopEnd")))
                    else:
                        conn.send("send data format err, data    {}".format(data))

                elif data == ":DTA:RELATIVE_POSITION 1\r\n":
                    rec_data = streamxpress.get_stream_relative_position()
                    logging.info("streamxpress receive data   " + repr(rec_data))
                    if rec_data.get("result") is True:
                        conn.send("{}{}".format(data[:23], rec_data.get("PosRel")))
                    else:
                        conn.send("send data format err, data    {}".format(data))

                elif data == ":DTA:SET_DVBT_CON_TYPE QPSK\r\n":
                    rec_data = streamxpress.set_dvbt_constellation_type_qpsk()
                    logging.info("streamxpress receive data   " + repr(rec_data))
                    if rec_data.get("result") is True:
                        conn.send("{}SUCCESS".format(data[:23]))
                    else:
                        conn.send("send data format err, data    {}".format(data))

                elif data == ":DTA:SET_DVBT_CON_TYPE 16-QAM\r\n":
                    rec_data = streamxpress.set_dvbt_constellation_type_16qam()
                    logging.info("streamxpress receive data   " + repr(rec_data))
                    if rec_data.get("result") is True:
                        conn.send("{}SUCCESS".format(data[:23]))
                    else:
                        conn.send("send data format err, data    {}".format(data))

                elif data == ":DTA:SET_DVBT_CON_TYPE 64-QAM\r\n":
                    rec_data = streamxpress.set_dvbt_constellation_type_64qam()
                    logging.info("streamxpress receive data   " + repr(rec_data))
                    if rec_data.get("result") is True:
                        conn.send("{}SUCCESS".format(data[:23]))
                    else:
                        conn.send("send data format err, data    {}".format(data))

                elif data == ":RDS:POWER_ON \r\n":
                    rdsp.send_rec_serial(cmd_power_on)
                    conn.send("{}SUCCESS".format(data[:14]))

                elif data == ":RDS:POWER_OFF \r\n":
                    rdsp.send_rec_serial(cmd_power_off)
                    conn.send("{}SUCCESS".format(data[:15]))

                elif data == ":RDS:USB_PC \r\n":
                    rdsp.send_rec_serial(cmd_usb_pc)
                    conn.send("{}SUCCESS".format(data[:12]))

                elif data == ":RDS:USB_STB \r\n":
                    rdsp.send_rec_serial(cmd_usb_stb)
                    conn.send("{}SUCCESS".format(data[:13]))

                elif data == ":RDS:USB_NONE \r\n":
                    rdsp.send_rec_serial(cmd_usb_none)
                    conn.send("{}SUCCESS".format(data[:14]))

                elif data == ":RDSP:PRESS_KEY1 \r\n":
                    rdsp.send_rec_serial(cmd_click_key_1)
                    conn.send("{}SUCCESS".format(data[:17]))

                elif data == ":RDSP:PRESS_KEY2 \r\n":
                    rdsp.send_rec_serial(cmd_click_key_2)
                    conn.send("{}SUCCESS".format(data[:17]))

                elif data == ":RDSP:PRESS_KEY3 \r\n":
                    rdsp.send_rec_serial(cmd_click_key_3)
                    conn.send("{}SUCCESS".format(data[:17]))

                elif data == ":RDSP:PRESS_KEY4 \r\n":
                    rdsp.send_rec_serial(cmd_click_key_4)
                    conn.send("{}SUCCESS".format(data[:17]))

                elif data == ":RDSP:PRESS_KEY5 \r\n":
                    rdsp.send_rec_serial(cmd_click_key_5)
                    conn.send("{}SUCCESS".format(data[:17]))

                elif data == ":RDSP:KEY1_UP \r\n":
                    rdsp.send_rec_serial(cmd_key_1_up)
                    conn.send("{}SUCCESS".format(data[:14]))

                elif data == ":RDSP:KEY2_UP \r\n":
                    rdsp.send_rec_serial(cmd_key_2_up)
                    conn.send("{}SUCCESS".format(data[:14]))

                elif data == ":RDSP:KEY3_UP \r\n":
                    rdsp.send_rec_serial(cmd_key_3_up)
                    conn.send("{}SUCCESS".format(data[:14]))

                elif data == ":RDSP:KEY4_UP \r\n":
                    rdsp.send_rec_serial(cmd_key_4_up)
                    conn.send("{}SUCCESS".format(data[:14]))

                elif data == ":RDSP:KEY5_UP \r\n":
                    rdsp.send_rec_serial(cmd_key_5_up)
                    conn.send("{}SUCCESS".format(data[:14]))

                elif data == ":RDSP:ALL_KEY_UP \r\n":
                    rdsp.send_rec_serial(cmd_key_all_up)
                    conn.send("{}SUCCESS".format(data[:17]))

                elif data == ":RDSP:KEY1_DOWN \r\n":
                    rdsp.send_rec_serial(cmd_key_1_down)
                    conn.send("{}SUCCESS".format(data[:16]))

                elif data == ":RDSP:KEY2_DOWN \r\n":
                    rdsp.send_rec_serial(cmd_key_2_down)
                    conn.send("{}SUCCESS".format(data[:16]))

                elif data == ":RDSP:KEY3_DOWN \r\n":
                    rdsp.send_rec_serial(cmd_key_3_down)
                    conn.send("{}SUCCESS".format(data[:16]))

                elif data == ":RDSP:KEY4_DOWN \r\n":
                    rdsp.send_rec_serial(cmd_key_4_down)
                    conn.send("{}SUCCESS".format(data[:16]))

                elif data == ":RDSP:KEY5_DOWN \r\n":
                    rdsp.send_rec_serial(cmd_key_5_down)
                    conn.send("{}SUCCESS".format(data[:16]))

                elif data == ":RDSP:RJ45_ON \r\n":
                    rdsp.send_rec_serial(cmd_ethernet_connect)
                    conn.send("{}SUCCESS".format(data[:14]))

                elif data == ":RDSP:RJ45_OFF \r\n":
                    rdsp.send_rec_serial(cmd_ethernet_disconnect)
                    conn.send("{}SUCCESS".format(data[:15]))

                elif data == ":RDS:RF_ON \r\n":
                    rdsp.send_rec_serial(cmd_rf_connect)
                    conn.send("{}SUCCESS".format(data[:11]))

                elif data == ":RDS:RF_OFF \r\n":
                    rdsp.send_rec_serial(cmd_rf_disconnect)
                    conn.send("{}SUCCESS".format(data[:12]))

                elif data == ':RDSP:STB_HW_DATA\r\n':
                    index_data = str(binascii.hexlify(":RDSP:STB_HW_DATA"))
                    # print index_data
                    res = rdsp.send_rec_serial(cmd_get_all_status)
                    send_data = index_data + res[12:76]
                    # print send_data
                    send_data = send_data.upper()
                    text_list = re.findall(".{2}", send_data)
                    hex_text = " ".join(text_list)
                    # print(hex_text)
                    str_text = bytearray.fromhex(hex_text)
                    conn.send(str_text)

                elif data == ':RDSP:MCU_INFO\r\n':
                    index_data = str(binascii.hexlify(":RDSP:MCU_INFO"))
                    res = rdsp.send_rec_serial(cmd_get_mcu_info)
                    send_data = index_data + res[16:66]
                    # print send_data
                    send_data = send_data.upper()
                    text_list = re.findall(".{2}", send_data)
                    hex_text = " ".join(text_list)
                    # print(hex_text)
                    str_text = bytearray.fromhex(hex_text)
                    conn.send(str_text)

                elif data == ':RDSP:DISEQC_DATA\r\n':
                    index_data = str(binascii.hexlify(":RDSP:DISEQC_DATA"))
                    res = rdsp.send_rec_serial_diseqc(cmd_get_diseqc_data)
                    print res

                    unpack_data = deal_diseqc_data(res)
                    print res
                    print res[12:]
                    print unpack_data
                    print index_data
                    str_text = bytearray.fromhex(index_data + unpack_data)
                    conn.send(str_text)

                elif data == ":DOC:CONFIG \r\n":
                    path = r'./ATServer.ini'
                    atserver_ini = GetATserverIni(path)
                    all_config = atserver_ini.get_all_config()
                    conn.send("{}SUCCESS {}".format(data[:12], all_config))


















                # elif "set_udisk_images" in dict_data.keys():
                #     file_name = dict_data.get("set_data")
                #
                #     src_floder = r"I:\file_path\{}".format(file_name)
                #     dst_floder = r"I:\images"
                #     """
                #     1.判断文件夹是否存在,存在则删除该文件夹
                #     2.复制文件夹
                #     """
                #     if os.path.exists(dst_floder):
                #         shutil.rmtree(dst_floder)
                #     cope_floder_src_dst(src_floder, dst_floder)
                #     del conn

                else:
                    print(data)
                    print("unknown message")
                    del conn

                # except:
                #     break


if __name__ == '__main__':
    cfg = Linux_ATServer()
    t = threading.Thread(target=cfg.response)
    t.setDaemon(True)
    t.start()
    try:
        print('Enter "Ctrl + C" to exit ')
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        print("program exited")
        sys.exit(0)
