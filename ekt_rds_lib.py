#!/usr/bin/env python
# -*- coding: utf-8 -*-
import serial
import binascii, time

cmd_power_off = '81 82 00 04 00 00 02 00 50 00 00 00 83 84'  # power off
cmd_power_on = '81 82 00 04 00 00 02 00 60 00 00 00 83 84'  # power on

cmd_usb_pc = '81 82 00 04 00 00 02 00 44 00 00 00 83 84'  # usb_pc
cmd_usb_stb = '81 82 00 04 00 00 02 00 48 00 00 00 83 84'  # usb_stb
cmd_usb_none = '81 82 00 04 00 00 02 00 4C 00 00 00 83 84'  # usb_none

cmd_click_key_1 = '81 82 00 04 00 00 02 01 00 00 00 00 83 84'  # click key 1
cmd_click_key_2 = '81 82 00 04 00 00 02 02 00 00 00 00 83 84'  # click key 2
cmd_click_key_3 = '81 82 00 04 00 00 02 03 00 00 00 00 83 84'  # click key 3
cmd_click_key_4 = '81 82 00 04 00 00 02 04 00 00 00 00 83 84'  # click key 4
cmd_click_key_5 = '81 82 00 04 00 00 02 05 00 00 00 00 83 84'  # click key 5

cmd_key_1_up = '81 82 00 04 00 00 02 49 00 00 00 00 83 84'  # key 1 up
cmd_key_2_up = '81 82 00 04 00 00 02 4A 00 00 00 00 83 84'  # key 2 up
cmd_key_3_up = '81 82 00 04 00 00 02 4B 00 00 00 00 83 84'  # key 3 up
cmd_key_4_up = '81 82 00 04 00 00 02 4C 00 00 00 00 83 84'  # key 4 up
cmd_key_5_up = '81 82 00 04 00 00 02 4D 00 00 00 00 83 84'  # key 5 up
cmd_key_all_up = '81 82 00 04 00 00 02 48 00 00 00 00 83 84'  # key all up

cmd_key_1_down = '81 82 00 04 00 00 02 41 00 00 00 00 83 84'  # key 1 down
cmd_key_2_down = '81 82 00 04 00 00 02 42 00 00 00 00 83 84'  # key 2 down
cmd_key_3_down = '81 82 00 04 00 00 02 43 00 00 00 00 83 84'  # key 3 down
cmd_key_4_down = '81 82 00 04 00 00 02 44 00 00 00 00 83 84'  # key 4 down
cmd_key_5_down = '81 82 00 04 00 00 02 45 00 00 00 00 83 84'  # key 5 down

cmd_rf_disconnect = '81 82 00 04 00 00 02 00 41 00 00 00 83 84'  # rf_disconnect
cmd_rf_connect = '81 82 00 04 00 00 02 00 42 00 00 00 83 84'  # rf_connect

cmd_ethernet_disconnect = '81 82 00 04 00 00 02 10 00 00 00 00 83 84'  # ethernet_disconnect
cmd_ethernet_connect = '81 82 00 04 00 00 02 20 00 00 00 00 83 84'  # ethernet_connect

cmd_get_all_status = '81 82 00 04 00 00 01 04 00 00 00 00 83 84'  # get_all_status
cmd_get_mcu_info = '81 82 00 04 00 00 00 00 00 00 00 00 83 84'  # get_all_status
cmd_get_diseqc_data = '81 82 00 04 00 00 01 01 00 00 00 00 83 84'  # get_all_status


class Ekt_Rdsp():
    def __init__(self, com_name, baud_rate, timeout):
        com = serial.Serial(com_name, baud_rate, timeout=timeout)
        self.com = com
        res = self.com.isOpen()

    def send_rec_serial(self, input_cmd):
        # hex_cmd = bytes.fromhex(input_cmd)    # python3
        hex_cmd = bytearray.fromhex(input_cmd)  # python2
        # print(hex_cmd)

        self.com.write(hex_cmd)

        # Stop and wait for the data
        # time.sleep(1)
        time.sleep(0.5)
        count = self.com.inWaiting()
        # print count
        rec_data = b''
        # receive data
        if count == 0:
            print('no data receive')
        if count > 0:
            rec_data = self.com.read(count)
            # print rec_data
            rec_data = str(binascii.b2a_hex(rec_data))
            # print rec_data

        self.com.flushInput()  # 清除缓存区数据。当代码在循环中执行时，不加这句代码会造成count累加
        return rec_data

    def send_rec_serial_diseqc(self, input_cmd):
        # hex_cmd = bytes.fromhex(input_cmd)    # python3
        hex_cmd = bytearray.fromhex(input_cmd)  # python2
        # print(hex_cmd)

        self.com.write(hex_cmd)

        start_time = time.time()
        while True:
            # Stop and wait for the data
            time.sleep(0.5)
            count = self.com.inWaiting()
            rec_data = self.com.read(count)
            if count == 0:
                continue
            else:
                rec_data = str(binascii.b2a_hex(rec_data))
                # print rec_data
                if rec_data[-4:] == b"8384" and rec_data[:4] == b"8182":
                    # print "*"*50
                    # print rec_data
                    break
            # timeout 300s
            if time.time() - start_time > 300:
                break
        self.com.flushInput()  # 清除缓存区数据。当代码在循环中执行时，不加这句代码会造成count累加
        return rec_data

    def __del__(self):
        # 关闭串口
        self.com.close()


if __name__ == '__main__':
    # com = serial.Serial('COM4', 115200, timeout=5)
    rdsp = Ekt_Rdsp('COM4', 115200, timeout=5)
    # rdsp.send_rec_serial(cmd_power_off)
    res_data = rdsp.send_rec_serial_diseqc(cmd_get_diseqc_data)
    print res_data
    # print res_data[12:]

    # print type(res_data)
    # print len(res_data)
