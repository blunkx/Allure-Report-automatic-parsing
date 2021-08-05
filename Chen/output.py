"""
The module include methods to verify and output CSV.
Method list:
    verify
    write_output
"""
import csv
import sys


def verify(func_list, status_dict, para_dict, func_list_without_para):
    """
    Check that each function in func_set also exists in the func_list_without_para
    If the number is correct, then print the number of functions after merging.
    In contrast, if the number is not correct, throw an exception.
    Args:
        func_list(list)
        status_dict(dict)
        para_dict(dict)
        func_list_without_para(list)
    Return:
        None
    """
    func_set = {v["func_name"] for v in func_list}
    func_name_list = [
        v["func_name"] for v in func_list_without_para if v["func_name"] in func_set
    ]
    for func in func_name_list:
        if func in para_dict and func in status_dict:
            continue
        print("Verify failed!")
        sys.exit()
    if len(func_set) == len(func_name_list) and len(func_name_list) == len(status_dict):
        print("After merging parameterized function: %d" % len(func_set))


def write_output(file_path, func_list):
    """
    Argst:
        file_path(str)
        function_list(list)
    Returns:
        None
    If there is no file_path, print all data.
    Otherwise output the data to CSV files.
    """
    if file_path == "":
        row = list(func_list[0].keys())
        del row[-1]
        print(row)
        for func in func_list:
            row = list(func.values())
            del row[-1]
            print(row)
    else:
        with open(file_path, "w", newline="") as out:
            row = list(func_list[0].keys())
            del row[-1]
            csv.writer(out).writerow(row)
            for func in func_list:
                row = list(func.values())
                del row[-1]
                csv.writer(out).writerow(row)
