#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import time
import traceback
from Python_CANoe import CANoe


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

def rename_log(log_folder, rename_name):
    filenames = os.listdir(log_folder)
    _name = []
    _time = []

    for filename in filenames:
        if filename[-4:] == '.asc':
            c_time = os.path.getctime(log_folder + os.sep + filename)

            _name.append(log_folder + os.sep + filename)
            _time.append(c_time)
    newest_log = _name[_time.index(max(_time))]
    os.rename(newest_log, log_folder + os.sep + rename_name + "_" + os.path.basename(newest_log))


class VSQ:
    def __init__(self, vsq_file_list):
        self.vsq_list = vsq_file_list
        self.vsq_lines = []
        self.can_app = CANoe()

        self.can_app.open_simulation("C:\\Data\\Users\\li_j11\\Profil\\Desktop\\Temp\\new CG2474\\20_20_137_new\\CG2474_0517.cfg")
        self.log_folder = "C:\\Data\\Users\\li_j11\\Profil\\Desktop\\Temp\\new CG2474\\Logging"

    def read_vsq(self):
        for vsq in self.vsq_list:
            print("################ Test %s" % vsq)

            # print(os.path.basename(vsq))
            # return
            # Todo: 启动CANoe
            self.can_app.start_Measurement()

            with open(vsq, 'r') as file_to_read:
                self.vsq_lines = file_to_read.readlines()
                while self.vsq_lines:
                    try:
                        self.parse_vsq(False, 0)
                    except Exception as error:
                        print(traceback.format_exc())
                        self.can_app.stop_Measurement()
                        break
            
            # Stop measurement and rename log file
            self.can_app.stop_Measurement()
            time.sleep(10)
            rename_name = os.path.basename(vsq).replace(".vsq", "")
            rename_log(self.log_folder, rename_name)


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
            sys_var = line_list[2].split("::")
            ns_name = sys_var[1]
            sysvar_name = sys_var[2]
            set_value = line_list[4]

            value_type = sys_var[-1]
            if value_type == "Integer":
                set_value = int(set_value)
            elif value_type == "Float":
                set_value = float(set_value)
            # print(ns_name, sysvar_name, set_value)
            self.can_app.set_SysVar(ns_name, sysvar_name, set_value)
            
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
            raise Exception("Invalid commad: %s" % line)
            

if __name__ == "__main__":
    sequences_list = get_sequences("Auto_Sequences")
    vsq_operator = VSQ(sequences_list)
    vsq_operator.read_vsq()
