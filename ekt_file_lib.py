#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser


class EktFile():
    """
    get ATServer.ini data
    """

    def __init__(self, path):
        """
        init
        :param path: ATServer.ini path
        """
        self.config = configparser.ConfigParser()
        self.config.read(path)

    def get_config_data(self, section, item):
        """
        get config data
        :param section:section name,example  V5LOADER、OTA、OTHER
        :param item: item name
        :return: item value
        """
        try:
            value = self.config.get(section, item)
        except:
            value = ""
        return value

    def get_all_config(self):
        """
        get all config
        :return: all config data
        """
        CD5PATH = self.get_config_data("V5LOADER", "CD5_PATH")
        TSPATH = self.get_config_data("V5LOADER", "TS_PATH")
        USBPATH = self.get_config_data("V5LOADER", "USB_PATH")
        LOADFILE = self.get_config_data("V5LOADER", "LOAD_FILE")
        CLEANFILE = self.get_config_data("V5LOADER", "CLEAN_FILE")
        PID = self.get_config_data("V5LOADER", "PID")

        OTATYPE = self.get_config_data("OTA", "TYPE")
        OTAFREQ = self.get_config_data("OTA", "FREQ")
        OTASYMBOLRATE = self.get_config_data("OTA", "SYMBOL_RATE")
        OTAANNEX = self.get_config_data("OTA", "ANNEX")
        OTACODERATE = self.get_config_data("OTA", "CODE_RATE")
        OTABANDWIDTH = self.get_config_data("OTA", "BANDWIDTH")

        OTHER_PARAM_1 = self.get_config_data("OTHER", "PARAM_1")
        OTHER_PARAM_2 = self.get_config_data("OTHER", "PARAM_1")
        OTHER_PARAM_3 = self.get_config_data("OTHER", "PARAM_1")

        # print CD5PATH
        # print TSPATH
        # print USBPATH
        # print LOADFILE
        # print CLEANFILE
        # print PID
        # print OTATYPE
        # print OTAFREQ
        # print OTASYMBOLRATE
        # print OTAANNEX
        # print OTACODERATE
        # print OTABANDWIDTH
        # print OTHER_PARAM_1
        # print OTHER_PARAM_2
        # print OTHER_PARAM_3
        all_config = r"#CD5PATH={}#TSPATH={}#USBPATH={}#LOADFILE={}#CLEANFILE={}#PID={}#OTATYPE={}#OTAFREQ={}#OTASYMBOLRATE={}#OTAANNEX={}#OTACODERATE={}#OTABANDWIDTH={}#OTHER_PARAM_1={}#OTHER_PARAM_2={}#OTHER_PARAM_3={}".format(
            CD5PATH, TSPATH, USBPATH, LOADFILE, CLEANFILE, PID, OTATYPE, OTAFREQ, OTASYMBOLRATE, OTAANNEX, OTACODERATE,
            OTABANDWIDTH, OTHER_PARAM_1, OTHER_PARAM_2, OTHER_PARAM_3)
        return all_config


if __name__ == '__main__':
    path = r'D:\Loren_projects\DCA4715pATX_test_package\ATServer.ini'
    atserver_ini = EktFile(path)
    all_config = atserver_ini.get_all_config()
    print all_config
