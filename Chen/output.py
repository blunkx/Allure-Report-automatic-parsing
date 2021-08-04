import csv
import os

# import sys


def verify(func_set, func_list_without_para, status_dict):
    # check that each function in func_set also exists in the func_list_without_para

    func_name_list = [
        v["func_name"] for v in func_list_without_para if v["func_name"] in func_set
    ]
    for func in func_name_list:
        try:
            status_dict[func]
        except Exception:
            print("Verify failed!")
            exit()
    if len(func_set) == len(func_name_list) and len(func_name_list) == len(status_dict):
        print("After merging parameterized function: %d" % len(func_set))


def write_output(file_name, func_list):
    if file_name == "":
        row = list(func_list[0].keys())
        del row[-1]
        print(row)
        for func in func_list:
            row = list(func.values())
            del row[-1]
            print(row)
    else:
        out = open(file_name, "w", newline="")
        row = list(func_list[0].keys())
        del row[-1]
        csv.writer(out).writerow(row)
        for func in func_list:
            row = list(func.values())
            del row[-1]
            csv.writer(out).writerow(row)
