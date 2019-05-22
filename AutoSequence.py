#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import time

def get_sequences(auto_folder):
    sequences_path = os.path.dirname(os.path.realpath(sys.argv[0])) + os.sep + auto_folder
    print("Auto Sequences file path: ", sequences_path)

    sequences_list = []

    for root, directory, files in os.walk(sequences_path):
        for file_name in files:
            name, suf = os.path.splitext(file_name)     #文件名， 文件后缀
            if suf == ".vsq":
                sequences_list.append(os.path.join(root, file_name))
    return sequences_list


def read_vsq(vsq_list):
    for vsq in vsq_list:
        print("################ Test %s" % vsq)
        # Todo: 启动CANoe

        with open(vsq, 'r') as file_to_read:
            vsq_lines = file_to_read.readlines()
            for line in vsq_lines:
                parse_vsq(vsq_lines)


def parse_vsq(vsq_content):
    line_list = line.split(",")
    if line_list[1] == "Comment":
        continue
    elif line_list[1] == "":
        continue
    elif line_list[1] == "Wait" and line_list[3] == "ms":
        print("Wait %s %s" % (line_list[2], line_list[3]))
        time.sleep(float(line_list[2])/1000)
    elif line_list[1] == "Set":
        print("Set sysvar %s %s %s, then wait %s ms" % (line_list[2], line_list[3], line_list[4], line_list[5]))
        # Todo: CANoe中设置sysvar
        time.sleep(float(line_list[5])/1000)
    elif line_list[1] == "Repeat":
        for i in range(int(line_list[2])):
            parse_vsq()


if __name__ == "__main__":
    sequences_list = get_sequences("Auto_Sequences")
    read_vsq(sequences_list)
