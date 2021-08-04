import os
import json
import re
import csv


def read_json(file_name):
    # read json -> dict
    json_path = os.getcwd() + "/allure-report/data/" + file_name
    try:
        input_file = open(json_path)
    except Exception:
        print("Failed to open!")
        exit()
    return json.load(input_file)


def read_csv(file_name):
    # read csv -> 2d list
    csv_path = os.getcwd() + "/allure-report/data/" + file_name
    try:
        input_file = open(csv_path)
    except Exception:
        print("Failed to open!")
        exit()
    return list(csv.reader(input_file, delimiter=","))


def check_path(fullname, row_from_suite):
    name = row_from_suite[4:9]
    name = [x for x in name if x != ""]
    for i in name:
        if i not in fullname:
            return False
    return True


def create_func_dict(fun, suites_csv, status_dict, para_dict):
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
                para_list.append("[" + match.group(3)) if match else ""
                break
    topo_marker = [s for s in temp["extra"]["tags"] if "topology(" in s][0]

    func_dict = {
        "suite": suite,
        "file_name": file_name,
        "topo_marker": topo_marker,
        "func_name": path,
        "status": fun["status"],
        "isParameterized": "x",
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
    func_list = sorted(func_list, key=lambda k: k["func_name"])
    func_list = sorted(func_list, key=lambda k: k["suite"])
    func_list = sorted(func_list, key=lambda k: k["file_name"])
    return func_list


def merge_para_func(status_dict, func_list, para_dict):
    new_list = func_list = list({v["func_name"]: v for v in func_list}.values())
    for row in new_list:
        # print(status_dict[row["func_name"]])
        row["isParameterized"] = "x" if not para_dict[row["func_name"]] else "v"
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
