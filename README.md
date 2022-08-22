# 与RDSP板接口说明

## streamxpress

    command_dta_type = ":DTA:TYPE {} {}\r\n"
    command_dta_freq = ":DTA:FREQ {}\r\n"
    command_dta_symrate = ":DTA:SYMRATE {}\r\n"
    command_dta_bandwidth = ":DTA:BANDWIDTH {}\r\n"
    command_dta_level = ":DTA:LEVEL {}\r\n"
    command_dta_set_dvbs = ":DTA:SET_DVBS {} {} {} {}\r\n"
    command_dta_set_dvbc = ":DTA:SET_DVBC {} {} {} {}\r\n"
    command_dta_set_dvbt = ":DTA:SET_DVBT {} {} {} {}\r\n"
    command_dta_set_dvbt_contype = ":DTA:SET_DVBT_CON_TYPE \r\n"
    command_dta_file = ":DTA:FILE {} {}\r\n"
    command_dta_remux = ":DTA:REMUX \r\n"
    command_dta_tsrate = ":DTA:TSRATE {}\r\n"
    command_dta_spectral_inversion = ":DTA:SPECTRAL_INVERSION \r\n"
    command_dta_rf_enabled_on_stop = ":DTA:RF_ENABLED_ON_STOP 1\r\n"
    command_dta_relative_position = ":DTA:RELATIVE_POSITION 1\r\n"
    command_dta_total_time = ":DTA:TOTAL_TIME 1\r\n"
    command_dta_play = ":DTA:PLAY \r\n"
    command_dta_pause = ":DTA:PAUSE \r\n"
    command_dta_stop = ":DTA:STOP \r\n"

## RDS

    command_rds_power_on = ":RDS:POWER_ON \r\n"
    command_rds_power_off = ":RDS:POWER_OFF \r\n"
    command_rds_usb_pc = ":RDS:USB_PC \r\n"
    command_rds_usb_stb = ":RDS:USB_STB \r\n"
    command_rds_usb_none = ":RDS:USB_NONE \r\n"
    command_rds_rf_on = ":RDS:RF_ON \r\n"
    command_rds_rf_off = ":RDS:RF_OFF \r\n"

## RDSP

    command_rdsp_connection = ":RDSP:CONNECTION \r\n"
    command_rdsp_mcu_info = ":RDSP:MCU_INFO\r\n"
    command_rdsp_hw_data = ":RDSP:STB_HW_DATA\r\n"
    command_rdsp_diseqc_data = ":RDSP:DISEQC_DATA\r\n"
    
    command_rdsp_press_key1 = ":RDSP:PRESS_KEY1 \r\n"
    command_rdsp_press_key2 = ":RDSP:PRESS_KEY2 \r\n"
    command_rdsp_press_key3 = ":RDSP:PRESS_KEY3 \r\n"
    command_rdsp_press_key4 = ":RDSP:PRESS_KEY4 \r\n"
    command_rdsp_press_key5 = ":RDSP:PRESS_KEY5 \r\n"
    
    command_rdsp_key1_down = ":RDSP:KEY1_DOWN \r\n"
    command_rdsp_key2_down = ":RDSP:KEY2_DOWN \r\n"
    command_rdsp_key3_down = ":RDSP:KEY3_DOWN \r\n"
    command_rdsp_key4_down = ":RDSP:KEY4_DOWN \r\n"
    command_rdsp_key5_down = ":RDSP:KEY5_DOWN \r\n"
    
    command_rdsp_key1_up = ":RDSP:KEY1_UP \r\n"
    command_rdsp_key2_up = ":RDSP:KEY2_UP \r\n"
    command_rdsp_key3_up = ":RDSP:KEY3_UP \r\n"
    command_rdsp_key4_up = ":RDSP:KEY4_UP \r\n"
    command_rdsp_key5_up = ":RDSP:KEY5_UP \r\n"
    command_rdsp_all_key_up = ":RDSP:ALL_KEY_UP \r\n"

## RJ45

    command_rdsp_rj45_on = ":RDSP:RJ45_ON \r\n"
    command_rdsp_rj45_off = ":RDSP:RJ45_OFF \r\n"

## FILE

    command_doc_copy = ":DOC:COPY \r\n"
    command_doc_move = ":DOC:MOVE \r\n"
    command_doc_del = ":DOC:DEL \r\n"
    command_doc_config = ":DOC:CONFIG \r\n"

## APP

    command_app_exec = ":APP:EXEC \r\n"
    command_app_close = ":APP:CLOSE \r\n"

## 硬件连接

    linuxATServer 为window端ATserver的linux版本，使用的接口完全兼容，使用方法：
    1、RDS plus板的串口连接在linux电脑上，通常为EKT TESTER，用于EKT TESTER和RDS plus板的串口通讯
    2、RDS plus板的连接pc端的usb接口，与EKT TESTER相连，用于usb升级过程中的文件传输

## 注意事项

    1、针对首次使用linuxATServer系统，需要设置linux系统下的U盘插拔自动mount，具体方式详见#168962中的 10-usbstorage.rules
    2、启动服务命令：sample: nohup python2 -u linux_atserver.py -i 192.168.1.167 -p 8900 -ATserver_f ATServer.ini -wsdl_f
    SpRc.wsdl > linux_atserver.out 2>&1 &
    可以根据实际情况调整各参数
    3、linux_atserver_window_debug.py脚本是在window系统下调试ATserver接口使用，实际linux ATserver并未使用改文件