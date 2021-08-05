"""
The module include methods needed to parse the allure-report.
Method list:
    read_json
    read_csv
    check_path
    create_func_dict
    sort_func_list
    create_func_list
    merge_para_func
"""
import os
import json
import re
import csv
import sys


def read_json(file_name):
    """
    If the file is not exist, throw an exception.
    Args:
        file_name(str): file name to read
    Returns:
        json.load(input_file)(dict): Data read from json
    """
    json_path = os.getcwd() + "/allure-report/data/" + file_name
    try:
        with open(json_path) as input_file:
            return json.load(input_file)
    except Exception:
        print("Failed to open!")
        sys.exit()


def read_csv(file_name):
    """
    If the file is not exist, throw an exception.
    Args:
        file_name(str): file name to read
    Returns:
        list(csv.reader(input_file, delimiter=","))(list): two dimentional list from csv
    """
    csv_path = os.getcwd() + "/allure-report/data/" + file_name
    try:
        with open(csv_path) as input_file:
            return list(csv.reader(input_file, delimiter=","))
    except Exception:
        print("Failed to open!")
        sys.exit()


def check_path(fullname, row_from_suite):
    """
    Args:
        file name(str): read from uid.json
        row(list): read from suite.csv
    Returns:
        bool: If the path from row corresponds to the full name return True else False.
    """
    name = row_from_suite[4:9]
    name = [x for x in name if x != ""]
    for i in name:
        if i not in fullname:
            return False
    return True


def create_func_dict(fun, suites_csv, status_dict, para_dict):
    """
    Create the dict to represent the detail of each function.
    Args:
        fun(dict): function name from behavior.json
        suites_csv(list): two dimentinal list read from suite.csv
        status_dict(dict): function name: [status1, status2]
        para_dict(dict): function name: [para1, para2]
    Returns:
        para_dict(dict): Contining info of each function
    """
    uid_name = "test-cases/" + fun["uid"] + ".json"
    temp = read_json(uid_name)
    para_list = []
    for row in suites_csv:
        if fun["name"] == row[9]:
            row[4] = "" if row[4] == "tests" else row[4]
            suite = row[4].replace(".", "/")
            file_name = suite + "/" + row[5] + ".py" if suite != "" else row[5] + ".py"
            path = file_name
            if row[6] != "" and "[" not in row[6]:
                path += "::" + row[6]
            match = re.search(r"(\S+)(\[)(.*)", fun["name"])
            func_name = match.group(1) if match else fun["name"]
            path += "::" + func_name
            if check_path(temp["fullName"], row):
                if match:
                    para_list.append("[" + match.group(3))
                break
    topo_marker = [s for s in temp["extra"]["tags"] if "topology(" in s][0]

    func_dict = {
        "suite": suite,
        "file_name": file_name,
        "topo_marker": topo_marker,
        "func_name": path,
        "status": fun["status"],
        "Parameterized": "x",
        "parameter_list": "s",
        "UID": fun["uid"],
    }
    if path not in status_dict:
        status_dict[path] = [fun["status"]]
        para_dict[path] = para_list
    else:
        status_dict[path] += [fun["status"]]
        para_dict[path] += para_list
    return func_dict


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


def create_func_list():
    """
    Create the sorted list of all functions and two dicts to
    Args: None
    Returns:
        fun(dict): function name from behavior.json
        status_dict(dict): function name: [status1, status2]
        para_dict(dict): function name: [para1, para2]

    """
    suite_csv = read_csv("suites.csv")
    func_list = list()
    status_dict = dict()
    para_dict = dict()
    for fun in read_json("behaviors.json")["children"]:
        func_list.append(create_func_dict(fun, suite_csv, status_dict, para_dict))
    func_list = sort_func_list(func_list)
    return func_list, status_dict, para_dict


def merge_para_func(func_list, status_dict, para_dict):
    """
    Merge all parameterized functions.
    Determine the status and parameter of each function after merging.
    Args:
        func_list(list): list of functions(dict)
        status_dict(dict): [function name: [status1, status2]]
        para_dict: [function name: [para1, para2]]
    Returns:
        new_list(list): funcion list after merging
    """
    new_list = func_list = list({v["func_name"]: v for v in func_list}.values())
    for row in new_list:
        row["Parameterized"] = "x" if not para_dict[row["func_name"]] else "v"
        row["parameter_list"] = ", ".join(para_dict[row["func_name"]])
        if (
            status_dict[row["func_name"]].count("broken") > 0
            or status_dict[row["func_name"]].count("failed") > 0
        ):
            row["status"] = "failed"
        elif status_dict[row["func_name"]].count("passed") > 0:
            row["status"] = "passed"
        elif status_dict[row["func_name"]].count("skipped") == len(
            status_dict[row["func_name"]]
        ):
            row["status"] = "skipped"
    return new_list
