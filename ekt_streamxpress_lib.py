# encoding:utf-8
from zeep import Client


class StreamXpress(object):
    """
    streamxpress
    """
    def __init__(self, wsdl_path):
        """
        init
        :param wsdl_path: wsdl path
        """
        client = Client(wsdl_path)
        self.client = client
        self.client.service.OpenSession()

    def set_device(self, type_data, mod):
        """
        :param type_data: the type of dectek card, like 115, 107
        :param mod:
            MOD_DTMB = 3
            MOD_DVBS = 5
            MOD_DVBS2 = 6
            MOD_DVBT = 7
            MOD_DVBT2 = 8
            MOD_ISDBT = 12
            MOD_J83A = 13  # J.83 annex A (DVB-C)
            MOD_J83B = 14  # J.83 annex B ("American QAM")
        :return:
        """
        rec_sacn_port = self.client.service.ScanPorts()
        list_item = rec_sacn_port.PortDescs.item
        dict_type_port = {}
        for item in list_item:
            serial = int(item.Serial)
            TypeNumber = item.TypeNumber
            Port = item.Port
            dict_type_port[TypeNumber] = [serial, Port]
        list_serial_port = dict_type_port.get(int(type_data))
        if list_serial_port:
            rec_selectport = self.client.service.SelectPort(list_serial_port[0], list_serial_port[1], int(mod))
            if rec_selectport.SpRcResult == 0:
                return {"result": True, "rec_selectport": rec_selectport}
            else:
                return {"result": False, "rec_selectport": rec_selectport}
        else:
            return {"result": False, "dict_type_port": dict_type_port}

    def set_freq(self, freq):
        """
        :param freq: modulation carrier frequency in KHz
        :return:
        """
        rec_get_rfpars = self.client.service.GetRfPars()
        RfPars = rec_get_rfpars.RfPars
        RfPars.Frequency = int(freq) * 1000
        # print RfPars
        rec_data = self.client.service.SetRfPars(RfPars)
        if rec_data == 0:
            return {"result": True, "rec_data": rec_data}
        else:
            return {"result": False, "rec_data": rec_data}

    def set_tsrate(self, rate):
        """
        :param rate: modulation carrier ts rate in bps
        :return:
        """
        rec_data = self.client.service.SetTsRate(int(rate))
        if rec_data == 0:
            return {"result": True, "rec_data": rec_data}
        else:
            return {"result": False, "rec_data": rec_data}

    def set_sym_rate(self, rate):
        """
        :param rate: symbol rate in Kbd. like 6875 or 27500
        :return:
        """
        rec_get_modpars = self.client.service.GetModPars()
        ModPars = rec_get_modpars.ModPars
        ModPars.SymRate = int(rate) * 1000
        # print ModPars
        rec_data = self.client.service.SetModPars(ModPars)
        if rec_data == 0:
            return {"result": True, "rec_data": rec_data}
        else:
            return {"result": False, "rec_data": rec_data}

    def set_bandwidth(self, bandwidth):
        """
        :param bandwidth:
            DTA_5MHZ    bandwidth:1
            DTA_6MHZ    bandwidth:2
            DTA_7MHZ    bandwidth:3
            DTA_8MHZ    bandwidth:4
        :return:
        """
        dict_bandwidth_bin = {
            1: ['0', '0', '1'],
            2: ['0', '1', '0'],
            3: ['0', '1', '1'],
            4: ['1', '0', '0'],
        }
        bin_list = dict_bandwidth_bin.get(int(bandwidth))
        if bin_list:
            pass
        else:
            return {"result": False, "bandwidth": bandwidth}
        rec_get_modpars = self.client.service.GetModPars()
        ModPars = rec_get_modpars.ModPars
        # print ModPars

        # set ParXtra1
        # print bin(ModPars.ParXtra1)
        list_ParXtra1 = list(bin(ModPars.ParXtra1))
        list_ParXtra1[-3:] = bin_list
        # print list_ParXtra1
        int_ParXtra1 = int(''.join(list_ParXtra1), 2)
        # print int_ParXtra1
        ModPars.ParXtra1 = int_ParXtra1
        # print ModPars
        rec_data = self.client.service.SetModPars(ModPars)
        if rec_data == 0:
            return {"result": True, "rec_data": rec_data}
        else:
            return {"result": False, "rec_data": rec_data}

    def set_output_level(self, dbm):
        """
        :param dbm:
        QAM : -35.0~0 dBm
        OFDM, ISDB-T : -38.0~-3 dBm
        :return:
        """
        rec_get_rfpars = self.client.service.GetRfPars()
        RfPars = rec_get_rfpars.RfPars
        RfPars.Level = float(dbm)
        # print RfPars
        rec_data = self.client.service.SetRfPars(RfPars)
        if rec_data == 0:
            return {"result": True, "rec_data": rec_data}
        else:
            return {"result": False, "rec_data": rec_data}

    def set_dvbs(self, type_data, freq, symbol_rate, code_rate):
        """
        init the DVBS/DVBS2 modulation
        :param freq: RF output frequency(Hz)
        :param type_data: modulation type, like following:
            DTA_DVBS_QPSK
            DTA_DVBS2_QPSK
            DTA_DVBS2_8PSK
        :param symbol_rate: symbol rate in bd
        :param code_rate:
            DTA_1_2
            DTA_2_3
            DTA_3_4
            DTA_4_5
            DTA_5_6
            DTA_6_7
            DTA_7_8
        """
        self.set_freq(float(freq))
        rec_get_modpars = self.client.service.GetModPars()
        ModPars = rec_get_modpars.ModPars
        ModPars.SymRate = int(symbol_rate) * 1000
        ModPars.ModType = int(type_data)
        ModPars.ParXtra0 = int(code_rate)
        # print ModPars
        rec_data = self.client.service.SetModPars(ModPars)
        if rec_data == 0:
            return {"result": True, "rec_data": rec_data}
        else:
            return {"result": False, "rec_data": rec_data}

    def set_dvbc(self, type_data, freq, annex, symbol_rate):
        """
        init the QAM modulation
        the parameters refer to the play_dvbt function
        :param type_data: modulation type, like following:
            DTA_QAM4
            DTA_QAM16
            DTA_QAM32
            DTA_QAM64
            DTA_QAM128
            DTA_QAM256
        :param freq: RF output frequency(KHz)
        :param annex:
        DTA_J83_A (DVB-C)
        DTA_J83_B (QAM-B)
        DTA_J83_C (QAM-C)
        :param symbol_rate: symbol rate in Kbd
        """
        self.set_freq(float(freq))
        rec_get_modpars = self.client.service.GetModPars()
        ModPars = rec_get_modpars.ModPars
        ModPars.SymRate = int(symbol_rate) * 1000
        ModPars.ModType = int(type_data)
        ModPars.ParXtra0 = int(annex)
        # print ModPars
        rec_data = self.client.service.SetModPars(ModPars)
        if rec_data == 0:
            return {"result": True, "rec_data": rec_data}
        else:
            return {"result": False, "rec_data": rec_data}

    def set_dvbt(self, type_data, freq, bandwidth, code_rate):
        """
        init the DVBT/DVBT2/DTMB/ISDB/ modulation
        :param type_data: modulation type, like following:
            DTA_DVBT
            DTA_DVBT2
        :param freq: modulation carrier frequency in KHz
        :param bandwidth:
            DTA_5MHZ    bandwidth:1
            DTA_6MHZ    bandwidth:2
            DTA_7MHZ    bandwidth:3
            DTA_8MHZ    bandwidth:4
        :param code_rate: Convolutional rate
            DTA_1_2
            DTA_2_3
            DTA_3_4
            DTA_5_6
            DTA_7_8
        :return:
        """
        dict_bandwidth_bin = {
            1: ['0', '0', '1'],
            2: ['0', '1', '0'],
            3: ['0', '1', '1'],
            4: ['1', '0', '0'],
        }
        bin_list = dict_bandwidth_bin.get(int(bandwidth))
        if bin_list:
            pass
        else:
            return {"result": False, "bandwidth": bandwidth}
        self.set_freq(float(freq))
        rec_get_modpars = self.client.service.GetModPars()
        ModPars = rec_get_modpars.ModPars
        # print ModPars
        ModPars.ParXtra0 = int(code_rate)
        ModPars.ModType = int(type_data)

        # set ParXtra1
        # print bin(ModPars.ParXtra1)
        list_ParXtra1 = list(bin(ModPars.ParXtra1))
        list_ParXtra1[-3:] = bin_list
        # print list_ParXtra1
        int_ParXtra1 = int(''.join(list_ParXtra1), 2)
        # print int_ParXtra1
        ModPars.ParXtra1 = int_ParXtra1
        rec_data = self.client.service.SetModPars(ModPars)
        if rec_data == 0:
            return {"result": True, "rec_data": rec_data}
        else:
            return {"result": False, "rec_data": rec_data}

    def set_file(self, file, flag=-1):
        """
        select the file of stream
        :param file: the name of stream
        :param flag: -1 = looping,
                     0  = once,
        :return:
        """
        if flag == 0:
            self.client.service.SetLoopFlags(0)
        else:
            self.client.service.SetLoopFlags(8)
        rec_data = self.client.service.OpenFile(file)
        if rec_data == 0:
            return {"result": True, "rec_data": rec_data}
        else:
            return {"result": False, "rec_data": rec_data}

    def set_remux(self, flag):
        """
        set remux for insert the null package.
        :param flag:
            DTA_FALSE
            DTA_TRUE
        """
        # todo Interface unavailable
        rec_data = self.client.service.GetAsiPars()
        print rec_data
        AsiPars = rec_data.AsiPars
        AsiPars.Remux = True
        rec_data = self.client.service.SetAsiPars(AsiPars)
        if rec_data == 0:
            return {"result": True, "rec_data": rec_data}
        else:
            return {"result": False, "rec_data": rec_data}

    def play(self):
        """
        play the stream
        """
        rec_data = self.client.service.SetPlayoutState(1)
        if rec_data == 0:
            return {"result": True, "rec_data": rec_data}
        else:
            return {"result": False, "rec_data": rec_data}

    def pause(self):
        """
        pause the stream
        """
        rec_data = self.client.service.SetPlayoutState(0)
        if rec_data == 0:
            return {"result": True, "rec_data": rec_data}
        else:
            return {"result": False, "rec_data": rec_data}

    def stop(self):
        """
        stop play the stream
        """
        rec_data = self.client.service.SetPlayoutState(2)
        if rec_data == 0:
            return {"result": True, "rec_data": rec_data}
        else:
            return {"result": False, "rec_data": rec_data}

    def rf_enabled_on_stop(self):
        """
        rf enabled on stop
        """
        rec_get_rfpars = self.client.service.GetRfPars()
        RfPars = rec_get_rfpars.RfPars
        RfPars.RfEnabledOnStop = True
        # print RfPars
        rec_data = self.client.service.SetRfPars(RfPars)
        if rec_data == 0:
            return {"result": True, "rec_data": rec_data}
        else:
            return {"result": False, "rec_data": rec_data}

    def rf_disabled_on_stop(self):
        """
        rf disabled on stop
        """
        rec_get_rfpars = self.client.service.GetRfPars()
        RfPars = rec_get_rfpars.RfPars
        RfPars.RfEnabledOnStop = False
        # print RfPars
        rec_data = self.client.service.SetRfPars(RfPars)
        if rec_data == 0:
            return {"result": True, "rec_data": rec_data}
        else:
            return {"result": False, "rec_data": rec_data}

    def get_stream_total_time(self):
        """
        get stream total time
        """
        rec_data = self.client.service.GetPlayoutInfo()
        # print rec_get_playoutinfo
        TimeLoopEnd = round(rec_data.PlayoutInfo.TimeLoopEnd, 6)
        if rec_data.SpRcResult == 0:
            return {"result": True, "TimeLoopEnd": TimeLoopEnd}
        else:
            return {"result": False, "rec_data": rec_data}

    def get_stream_relative_position(self):
        """
        get stream relative position
        """
        rec_data = self.client.service.GetPlayoutStatus()
        # print rec_get_playoutstatus
        PosRel = round(rec_data.PlayoutStatus.PosRel, 6)
        if rec_data.SpRcResult == 0:
            return {"result": True, "PosRel": PosRel}
        else:
            return {"result": False, "rec_data": rec_data}

    def set_dvbt_constellation_type_qpsk(self):
        """
        set dvbt constellation type qpsk
        """
        rec_get_modpars = self.client.service.GetModPars()
        # print rec_get_modpars
        ModPars = rec_get_modpars.ModPars
        # print ModPars
        list_ParXtra1 = list(bin(ModPars.ParXtra1))
        list_ParXtra1[-6:-3] = ['0', '1', '0']
        # print list_ParXtra1
        int_ParXtra1 = int(''.join(list_ParXtra1), 2)
        # print int_ParXtra1
        ModPars.ParXtra1 = int_ParXtra1
        rec_data = self.client.service.SetModPars(ModPars)
        if rec_data == 0:
            return {"result": True, "rec_data": rec_data}
        else:
            return {"result": False, "rec_data": rec_data}

    def set_dvbt_constellation_type_16qam(self):
        """
        set dvbt constellation type 16qam
        """
        rec_get_modpars = self.client.service.GetModPars()
        # print rec_get_modpars
        ModPars = rec_get_modpars.ModPars
        # print bin(ModPars.ParXtra1)
        list_ParXtra1 = list(bin(ModPars.ParXtra1))
        list_ParXtra1[-6:-3] = ['1', '0', '0']
        # print list_ParXtra1
        int_ParXtra1 = int(''.join(list_ParXtra1), 2)
        # print int_ParXtra1
        ModPars.ParXtra1 = int_ParXtra1
        rec_data = self.client.service.SetModPars(ModPars)
        if rec_data == 0:
            return {"result": True, "rec_data": rec_data}
        else:
            return {"result": False, "rec_data": rec_data}

    def set_dvbt_constellation_type_64qam(self):
        """
        set dvbt constellation type 64qam
        """
        rec_get_modpars = self.client.service.GetModPars()
        # print rec_get_modpars
        ModPars = rec_get_modpars.ModPars
        # print bin(ModPars.ParXtra1)
        list_ParXtra1 = list(bin(ModPars.ParXtra1))
        list_ParXtra1[-6:-3] = ['1', '1', '0']
        # print list_ParXtra1
        int_ParXtra1 = int(''.join(list_ParXtra1), 2)
        # print int_ParXtra1
        ModPars.ParXtra1 = int_ParXtra1
        rec_data = self.client.service.SetModPars(ModPars)
        if rec_data == 0:
            return {"result": True, "rec_data": rec_data}
        else:
            return {"result": False, "rec_data": rec_data}

    def __del__(self):
        self.client.service.CloseSession()


if __name__ == '__main__':
    streamxpress = StreamXpress('E:\ivan_code\linux_atserver\SpRc.wsdl')
    # res = streamxpress.set_dat_type(107, 5)
    # res = streamxpress.set_freq(1622000)
    # res = streamxpress.rf_enabled_on_stop()
    # res = streamxpress.rf_disabled_on_stop()
    # res = streamxpress.set_output_level(-10)
    # res = streamxpress.set_tsrate(16000000)
    # res = streamxpress.set_sym_rate(505)
    # res = streamxpress.set_dvbs(0, 1722000, symbol_rate=33000, code_rate=0)
    # res = streamxpress.set_dvbs(33, 1622000, symbol_rate=34000, code_rate=1)
    # res = streamxpress.set_dvbc(6, 788000, 2, symbol_rate=6855)
    res = streamxpress.set_dvbt(9, 788000, 3, 2)
    # res = streamxpress.set_file(r"X:\ivan\autotest\smoke_test\QE_dvb_subtitle.ts", -1)
    # res = streamxpress.set_remux(-1)
    # res = streamxpress.play()
    # res = streamxpress.pause()
    # res = streamxpress.stop()
    # res = streamxpress.get_stream_total_time()
    # res = streamxpress.get_stream_relative_position()
    # res = streamxpress.set_dvbt_constellation_type_qpsk()
    # res = streamxpress.set_dvbt_constellation_type_16qam()
    # res = streamxpress.set_dvbt_constellation_type_64qam()
    # res = streamxpress.set_bandwidth(3)

    print res
