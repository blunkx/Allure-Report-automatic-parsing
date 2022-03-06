#!/usr/bin/env python3
import csv
import json
import sys
from pathlib import Path


def read_csv(file_name):
    """
    If the file is not exist, throw an exception.
    Args:
        file_name(str): file name to read
    Returns:
        list(csv.reader(input_file, delimiter=","))(list): two dimentional list from csv
    """
    csv_path = Path.cwd() / "allure-report" / "data" / file_name
    try:
        with open(csv_path) as input_file:
            return list(csv.reader(input_file, delimiter=","))
    except Exception:
        print("Failed to open!")
        sys.exit()


def write_csv(file_name, function_list):
    """
    If there is no file_path, print all data.
    Otherwise output the data to CSV files.
    Args:
        file_name(str): filename to output
        function_list(list): list of all functions, each stored as a dict
    Returns:
        None
    """
    file_path = Path.cwd() / file_name
    try:
        with open(file_path, "w", newline="") as out:
            row = list(function_list[0].keys())
            csv.writer(out).writerow(row)
            for func in function_list:
                row = list(func.values())
                csv.writer(out).writerow(row)
    except Exception:
        print("Failed to open!")
        sys.exit()


def get_case_num():
    """
    Get allure report number.
    Args:
        None
    Returns:
        data[0]["buildOrder"](int): the report number
    """
    csv_path = Path.cwd() / "allure-report" / "history" / "retry-trend.json"
    try:
        with open(csv_path) as input_file:
            data = json.load(input_file)
            # return the case number
            return data[0]["buildOrder"]
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


def create_func_list(suite_csv):
    """
    Create the sorted list of all functions and two dicts to
    Args:
        suites_csv(list): two dimentinal list read from suite.csv
    Returns:
        result(list): list of all functions, each function is stored in a dict
    """
    result = list()
    for row in suite_csv:
        suite = row[4]
        file_name = row[4] + "/" + row[5] + ".py"
        topo_marker = ""
        func_name = file_name + "::" + row[9]
        """
        Status	Start Time	Stop Time	Duration in ms	Parent Suite	Suite	Sub Suite	Test Class	Test Method    Name    Description
        0       1           2           3               4               5       6           7           8              9       10
        """
        match = "x" if row[5] not in row[9] else ""
        func_dict = {
            "suite": suite,
            "file_name": file_name,
            "topo_marker": topo_marker,
            "func_name": func_name,
            "status": row[0],
            "match": match,
        }
        result.append(func_dict)
    return result


def main():
    suite_csv = read_csv("suites.csv")
    suite_csv.pop(0)
    result = sort_func_list(create_func_list(suite_csv))
    write_csv("sdk_tests #{}.csv".format(get_case_num()), result)


if __name__ == "__main__":
    main()