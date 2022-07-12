#!/usr/bin/env python
# -*- coding: utf-8 -*-
import shutil
import os

def deal_diseqc_data(str_data):
    load_h = str_data[4:6]
    load_l = str_data[6:8]
    extra_byte_h = str_data[8:10]
    extra_byte_l = str_data[10:12]

    data_num = int(load_h + load_l, 16)
    print data_num
    load_data = str_data[12:12 + data_num * 2]
    print load_data

    extra_num = int(extra_byte_h + extra_byte_l, 16)
    print extra_num
    extra_data = str_data[12 + data_num * 2:12 + data_num * 2 + extra_num * 2]
    print extra_data

    unpack_data = ""
    for i in range(extra_num):
        current_extra = extra_data[i * 2: (i + 1) * 2]
        print current_extra
        print "*" * 50
        hex_current_extra = bin(int(current_extra, 16))[2:].zfill(9)
        list_current_data = []
        new_data = ""
        if i == extra_num - 1:
            current_data = load_data[i * 7 * 2:]
            print current_data
            add_current_extra = hex_current_extra[3:][::-1]
            print add_current_extra
        else:
            current_data = load_data[(i * 7) * 2:(i + 1) * 7 * 2]
            print current_data
            add_current_extra = hex_current_extra[2:][::-1]
            print add_current_extra

        list_current_data = list(current_data)
        for index_num, j in enumerate(add_current_extra):
            if j == "1":
                list_current_data[index_num * 2] = hex(int(current_data[index_num * 2]) + 8)[2]
            new_data = "".join(list_current_data)
        print new_data
        unpack_data += new_data
    return unpack_data


def remove_file(del_file):
    """
    删除指定文件
    :param del_file: 待删除文件
    :return:
    """
    if os.path.isfile(del_file):
        os.remove(del_file)
    print(del_file + " was removed!")


def cope_file_src_dst(src_file, dst_file):
    """
    从源目录复制文件到指定目录
    :param src_file: 源文件
    :param dst_file: 指定目录文件
    :return:
    """
    shutil.copy2(src_file, dst_file)


def move_file_src_dst(src_file, dst_file):
    """
    从源目录剪切文件到指定目录
    :param src_file: 源文件
    :param dst_file: 指定目录文件
    :return:
    """
    shutil.move(src_file, dst_file)


def cope_floder_src_dst(src_file, dst_file):
    """
    从源目录复制文件夹到指定目录
    :param src_file: 源文件
    :param dst_file: 指定目录文件
    :return:
    """
    shutil.copytree(src_file, dst_file)


def del_all_file(filepath):
    """
    删除某一目录下的所有文件与文件夹
    :param filepath: 路径
    :return:
    """
    del_list = os.listdir(filepath)
    for f in del_list:
        file_path = os.path.join(filepath, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

if __name__ == '__main__':
    str_data = "818200140003030102020400000000000000601039700000000000200200008384"

    unpack_data = deal_diseqc_data(str_data)
    print str_data
    print str_data[12:]
    print unpack_data
# print load_h
# print load_l
# print extra_byte_h
# print extra_byte_l


# print str_data[12:]
# print str_data[12:-8]
# print str_data[12:-8]
