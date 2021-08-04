import os
import json
import csv
import re


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


def check_path(csv_path_lists, full_name_lists):
    # check behavier.csv is same with UID.json
    all_in_csv = True
    for csv_path_list in csv_path_lists:
        if csv_path_list not in full_name_lists:
            all_in_csv = False
    return all_in_csv


def create_dict(json_array, suites_rows, func_list, parameterize):
    # create all test function lists
    regex_function_name = re.compile(r"(\S+)(\[)(.*)")
    for fun in json_array["children"]:
        function_name_match = regex_function_name.search(fun["name"])

        func_name = function_name_match.group(1) if function_name_match else fun["name"]

        # find more info in suites csv
        for row in suites_rows:
            if fun["name"] == row[9]:
                is_class = regex_function_name.search(row[6])

                if row[6] != "" and not is_class:
                    path = row[5] + ".py" + "::" + row[6]
                    lists = [row[5], row[6]]
                else:
                    path = row[5] + ".py"
                    lists = [row[5]]

                suite = row[4].replace(".", "/")
                suite_list = row[4].split(".")
                csv_path_lists = lists + suite_list
                only_file_name = row[5]
                break

        # add suites if it is null
        suite = "tests" if suite == "" else suite
        file_name = suite + "/" + only_file_name + ".py"
        path_list = suite + "/" + path + "::" + func_name

        # read UID.json
        uid_array = read_json("test-cases/" + fun["uid"] + ".json")
        full_name = uid_array["fullName"]
        full_name_lists = re.split(r"\.|#", full_name)

        all_in_csv = check_path(csv_path_lists, full_name_lists)

        # if suites csv path is not same with UID.json
        if all_in_csv is False:
            suite_lists = suite.split("/")

            for suite_list in suite_lists:
                if suite_list in full_name_lists:
                    full_name_lists.remove(suite_list)

            if suite in full_name_lists:
                full_name_lists.remove(suite)

            file_name = suite + "/" + full_name_lists[0] + ".py"

            if len(full_name_lists) == 2:
                path_list = file_name + "::" + full_name_lists[1]
            elif len(full_name_lists) == 3:
                path_list = (
                    file_name + "::" + full_name_lists[1] + "::" + full_name_lists[2]
                )

        # get test_function topology
        topo = [s for s in uid_array["extra"]["tags"] if "topology(" in s][0]

        # create function dictionary and add func_list
        func_dict = {
            "suite": suite,
            "file_name": file_name,
            "topo_marker": topo,
            "path_list": path_list,
            "status": fun["status"],
        }
        func_list.append(func_dict)

        # if have parameter get it and add to parameterize dict
        if function_name_match:
            parameter = function_name_match.group(3)
            parameter = parameter.replace("]", "")
            parameter_list = list(parameter)
            parameter_list.insert(0, "[")
            parameter_list.append("]")
            if parameterize.get(path_list) is None:
                parameterize[path_list] = list()
            parameterize[path_list].append("".join(parameter_list))
        else:
            if parameterize.get(path_list) is None:
                parameterize[path_list] = list()
            parameter = ""

    add_parameter_in_func_list(func_list, parameterize)


def add_parameter_in_func_list(func_list, parameterize):
    # check the function is or isn't parameterize and add the parameter list
    for fun in func_list:
        if len(parameterize[fun["path_list"]]) > 0:
            fun["is_parameterize"] = "v"
        else:
            fun["is_parameterize"] = "x"

        temp_list = parameterize[fun["path_list"]]
        fun["parameter"] = ", ".join(temp_list)


def edit_status(func_list):
    # merage the status with parameterize function
    for func in func_list:
        same_funcs = list(
            filter(lambda fun: fun["path_list"] == func["path_list"], func_list)
        )
        count_pass, count_skip, count_fail = 0, 0, 0
        for same_func in same_funcs:
            if same_func["status"] == "passed":
                count_pass += 1
            elif same_func["status"] == "skipped":
                count_skip += 1
            elif same_func["status"] == "failed" or same_func["status"] == "broken":
                count_fail += 1

        if count_fail > 0:
            new_status = "failed"
        elif count_fail == 0 and count_pass == 0:
            new_status = "skipped"
        elif count_fail == 0 and count_pass > 0:
            new_status = "passed"

        func["status"] = new_status


def remove_suites_tests(func_list):
    # if the suites remove suites
    for func in func_list:
        if func["suite"] == "tests":
            func["suite"] = ""
            file_name = func["file_name"].split("/")
            file_name.remove("tests")
            func["file_name"] = "".join(file_name)
            path_lists = func["path_list"].split("/")
            path_lists.remove("tests")
            func["path_list"] = "".join(path_lists)
