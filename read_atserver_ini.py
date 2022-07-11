#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser

config = configparser.ConfigParser()
path = r'D:\Loren_projects\DCA4715pATX_test_package\ATServer.ini'
config.read(path)


def get_config_data(section, item):
    try:
        value = config.get(section, item)
    except:
        value = ""
    return value


CD5PATH = get_config_data("V5LOADER", "CD5_PATH")
TSPATH = get_config_data("V5LOADER", "TS_PATH")
USBPATH = get_config_data("V5LOADER", "USB_PATH")
LOADFILE = get_config_data("V5LOADER", "LOAD_FILE")
CLEANFILE = get_config_data("V5LOADER", "CLEAN_FILE")
PID = get_config_data("V5LOADER", "PID")

OTATYPE = get_config_data("OTA", "TYPE")
OTAFREQ = get_config_data("OTA", "FREQ")
OTASYMBOLRATE = get_config_data("OTA", "SYMBOL_RATE")
OTAANNEX = get_config_data("OTA", "ANNEX")
OTACODERATE = get_config_data("OTA", "CODE_RATE")
OTABANDWIDTH = get_config_data("OTA", "BANDWIDTH")

OTHER_PARAM_1 = get_config_data("OTHER", "PARAM_1")
OTHER_PARAM_2 = get_config_data("OTHER", "PARAM_1")
OTHER_PARAM_3 = get_config_data("OTHER", "PARAM_1")

print CD5PATH
print TSPATH
print USBPATH
print LOADFILE
print CLEANFILE
print PID
print OTATYPE
print OTAFREQ
print OTASYMBOLRATE
print OTAANNEX
print OTACODERATE
print OTABANDWIDTH

print OTHER_PARAM_1
print OTHER_PARAM_2
print OTHER_PARAM_3
