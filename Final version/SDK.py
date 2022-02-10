import os
import json
import re
import csv
import sys


def read_csv(file_name):
    """
    If the file is not exist, throw an exception.
    Args:
        file_name(str): file name to read
    Returns:
        list(csv.reader(input_file, delimiter=","))(list): two dimentional list from csv
    """
    # csv_path = os.getcwd() + "/allure-report/data/" + file_name
    csv_path = file_name

    try:
        with open(csv_path) as input_file:
            return list(csv.reader(input_file, delimiter=","))
    except Exception:
        print("Failed to open!")
        sys.exit()


def sort_func_list(func_list):
    """
    First sort all functions by name, then by suite, and finally by file name.
    Args:
        func_list(list): lsit of all functions
    Returns:
        func_list(list): list after sorting
    """
    func_list = sorted(func_list, key=lambda k: k["func_name"])
    func_list = sorted(func_list, key=lambda k: k["suite"])
    func_list = sorted(func_list, key=lambda k: k["file_name"])
    return func_list


suite_csv = read_csv("suites.csv")
suite_csv.pop(0)
result = list()
for row in suite_csv:
    suite = row[4]
    file_name = row[4] + "/" + row[5] + ".py"
    topo_marker = ""
    func_name = file_name + "::" + row[9]
    func_dict = {
        "suite": suite,
        "file_name": file_name,
        "topo_marker": topo_marker,
        "func_name": func_name,
        "status": row[0],
    }
    result.append(func_dict)
result = sort_func_list(result)
file_path = "test.csv"
with open(file_path, "w", newline="") as out:
    row = list(result[0].keys())
    # del row[-1]
    csv.writer(out).writerow(row)
    for func in result:
        row = list(func.values())
        # del row[-1]
        csv.writer(out).writerow(row)
# Status	Start Time	Stop Time	Duration in ms	Parent Suite	Suite	Sub Suite	Test Class	Test Method    Name    Description
# 0         1           2           3               4               5       6           7           8              9       10

# suite = parent_suite
# file_name = parent_suite + suite + .py
# topo_marker = ?
# func_name = file_name + :: + name
# status
