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


class VSQ:
    def __init__(self, vsq_file_list):
        self.vsq_list = vsq_file_list
        self.vsq_lines = []

    

    def read_vsq(self):
        for vsq in self.vsq_list:
            print("################ Test %s" % vsq)
            # Todo: 启动CANoe

            with open(vsq, 'r') as file_to_read:
                self.vsq_lines = file_to_read.readlines()
                while self.vsq_lines:
                    self.parse_vsq(False, 0)

    def parse_vsq(self, repeat_indecator, index):
        line = self.vsq_lines[index].strip()
        if not repeat_indecator:
            del self.vsq_lines[index]
        line_list = line.split(",")
        # print(line_list)
        if line_list[0] == "":
            return 1
        elif line_list[1] == "Comment":
            return 1
        elif line_list[1] == "":
            return 1
        elif line_list[1] == "Wait" and line_list[3] == "ms":
            print("Wait %s %s" % (line_list[2], line_list[3]))
            time.sleep(float(line_list[2])/1000)
        elif line_list[1] == "Set":
            print("Set sysvar %s %s %s, then wait %s ms" % (line_list[2], line_list[3], line_list[4], line_list[5]))
            # Todo: CANoe中设置sysvar
            time.sleep(float(line_list[5])/1000)
        elif line_list[1] == "Repeat":
            repeat_times = int(line_list[2])
            print("Repeat %s times" % repeat_times)
            for i in range(repeat_times):
                if i == (repeat_times - 1):
                    repeat_indecator = False
                else:
                    repeat_indecator = True
                print("Repeat index: %d" % i)
                content_index = 0
                repeat_index = self.parse_vsq(repeat_indecator, content_index)
                while repeat_index != 0:
                    if repeat_indecator:
                        content_index += 1
                    repeat_index = self.parse_vsq(repeat_indecator, content_index)


        elif line_list[1] == "Repeat End":
            print("Repeat End")
            return 0

        else:
            print("************************", line, "*******************")
            return 1

if __name__ == "__main__":
    sequences_list = get_sequences("Auto_Sequences")
    vsq_operator = VSQ(sequences_list)
    vsq_operator.read_vsq()
