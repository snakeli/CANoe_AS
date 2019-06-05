import os
import sys
import traceback




POWER_MODE_DICT = {"00":"OFF", "01":"ACC", "02":"RUN", "03":"Crank"}

def get_logs(log_folder):
    log_path = os.path.dirname(os.path.realpath(sys.argv[0])) + os.sep + log_folder
    print("Auto Sequences file path: ", log_path)

    log_list = []

    for root, directory, files in os.walk(log_path):
        for file_name in files:
            name, suf = os.path.splitext(file_name)     #文件名， 文件后缀
            if suf == ".asc":
                log_list.append(os.path.join(root, file_name))
    return log_list


def edit_log(log):
    new_log = []

    with open(log, 'r') as file_to_read:
        power_mode_flag = False
        log_lines = file_to_read.readlines()
        for log_line in log_lines:
            # log_line = log_line.strip()
            try:
                if "251             Tx" in log_line:
                    # print(log_line)
                    diagnostic = log_line.split("251             Tx")[1]
                    diagnostic = diagnostic.split()
                    diagnostic = [diagnostic[3], diagnostic[4], diagnostic[5], diagnostic[6], diagnostic[7], diagnostic[8], diagnostic[9]]
                    while diagnostic[-1] == "00":
                        del diagnostic[-1]
                    diagnostic = " ".join(diagnostic)
                    new_line = "\n// Step :  Send service " + diagnostic + "\n\n"
                    print(new_line)
                    new_log.append(new_line)

                elif "::a_Power_Mode_Value_Set = " in log_line:
                    power_mode_flag = True
                

                elif power_mode_flag and "SV: " in log_line:
                    power_mode_flag = False

                elif power_mode_flag and "10242040x" in log_line:
                    power_mode_flag = False

                    power_mode_sent = log_line.split("Tx")[1]
                    power_mode_sent = power_mode_sent.split()[2]
                    if power_mode_sent in POWER_MODE_DICT:
                        power_mode_value = POWER_MODE_DICT[power_mode_sent]
                        new_line = "\n// Step :  Place DUT into %s powermode \n\n" % power_mode_value
                        print(new_line)
                        new_log.append(new_line)

                new_log.append(log_line)

            except Exception as error:
                print(traceback.format_exc())
                break
    
    old_name = os.path.basename(log)
    new_name = "Python_" + old_name
    new_log_name = log.replace(old_name, new_name)

    with open(new_log_name, 'w') as out_file:
        out_file.writelines(new_log)


if __name__ == "__main__":
    log_list = get_logs("Logs")

    for _log in log_list:
        print("======================================================================")
        print("Start to edit log: ", _log)
        edit_log(_log)
        print("======================================================================")

