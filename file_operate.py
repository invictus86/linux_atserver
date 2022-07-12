#!/usr/bin/env python
# -*- coding: utf-8 -*-
import shutil
import os


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
    # src_file = r"D:\9615\burn_file\unsigned_application_file\EKCleanSPCBKey.CD5"
    # dst_file = r"F:\EKCleanSPCBKey.CD5"
    # cope_file_src_dst(src_file, dst_file)
    # path_file = r"D:\9615\burn_file\current_burn_file"
    # man_file = serach_man_file(path_file)
    # print(man_file)
    #
    # dev_file = serach_dev_file(path_file)
    # print(dev_file)
    move_file_src_dst(r"F:\1\SERIAL.BIN", r"F:\2")
    # filepath = "F:"
    # del_all_file(filepath)
    # cope_file_src_dst(r"D:\flash_samples_7005\Flash samples\u\fuse_tool_vmx_1.05_read", r"F:fuse_tool_vmx_1.05_read")
    # cope_file_src_dst(r"D:\flash_samples_7005\Flash samples\u\fuse_tool_vmx_v1.3", r"F:fuse_tool_vmx_v1.3")
    # cope_file_src_dst(r"D:\flash_samples_7005\Flash samples\u\hdcp_wr_wpkey", r"F:hdcp_wr_wpkey")
    # cope_file_src_dst(r"D:\flash_samples_7005\Flash samples\u\product_sabbat_dual.abs", r"F:product_sabbat_dual.abs")
