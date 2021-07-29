import os
import re
import json
import csv
import requests
from zipfile import ZipFile


def read_json(file_name):
    # read json -> dict
    json_path = os.getcwd() + '/allure-report/data/' + file_name
    try:
        input_file = open(json_path)
    except:
        print('Failed to open!')
    return json.load(input_file)


def read_csv(file_name):
    # read csv -> 2d list
    csv_path = os.getcwd() + '/allure-report/data/' + file_name
    try:
        input_file = open(csv_path)
    except:
        print('Failed to open!')
    return list(csv.reader(input_file, delimiter=','))


def create_dict():
    json_array = read_json('behaviors.json')
    suites_rows = read_csv('suites.csv')
    for fun in json_array["children"]:
        match = re.search("(\S+)(\[)(\S+)", fun["name"])
        if match:
            func_name = match.group(1)
        else:
            func_name = fun["name"]
        path = ""
        suite = ""
        for row in suites_rows:
            match_csv = re.search("(\S+)(\[)(\S+)", row[9])
            if match_csv:
                func_name_csv = match_csv.group(1)
            else:
                func_name_csv = row[9]
            if (func_name == func_name_csv):
                is_class = re.search("(\S+)(\[)(\S+)", row[6])
                if (row[6] != "" and not is_class):
                    path = row[5] + ".py" + "::" + row[6]
                else:
                    path = row[5] + ".py"
                suite = row[4].replace(".", "/")
                break

        if suite != "":
            file_name = suite + "/" + row[5] + ".py"
            path_list = suite + "/" + path + "::" + func_name
        else:
            file_name = row[5] + ".py"
            path_list = path + "::" + func_name

        uid_file = open("allure-report/data/test-cases/" + fun['uid'] +
                        ".json")
        uid_array = json.load(uid_file)
        topo = [s for s in uid_array['extra']['tags'] if 'topology(' in s][0]
        func_dict = {
            'suite': suite,
            'file_name': file_name,
            'topo_marker': topo,
            'path_list': path_list,
            'status': fun["status"],
        }
        func_list.append(func_dict)


def write_output(file_name, func_list):
    out = open(file_name, 'w')
    for func in func_list:
        csv.writer(out).writerow(list(func.values()))


url = "https://jenkins.clounix.com/job/sonic/job/testbed/job/201911.clounix/job/sonic-mgmt/40/artifact/allure-report.zip"
#r = requests.get(url)
#code = open("allure.zip", "wb")
# code.write(r.content)
# code.close()
zip_ref = ZipFile("allure.zip", 'r')
zip_ref.extractall()
func_list = list()
create_dict()
for func in func_list:
    same_funcs = list(
        filter(lambda fun: fun['path_list'] == func["path_list"], func_list))
    count_pass = 0
    count_skip = 0
    count_fail = 0
    for same_func in same_funcs:
        if (same_func["status"] == "passed"):
            count_pass += 1
        elif (same_func["status"] == "skipped"):
            count_skip += 1
        elif (same_func["status"] == "failed"):
            count_fail += 1

    if (count_fail > 0):
        new_status = "failed"
    elif (count_fail == 0 and count_pass == 0):
        new_status = "skipped"
    elif (count_fail == 0 and count_pass > 0):
        new_status = "passed"

    func["status"] = new_status

func_list = {v['path_list']: v for v in func_list}.values()
func_list = sorted(func_list, key=lambda k: k['path_list'])
func_list = sorted(func_list, key=lambda k: k['suite'])
func_list = sorted(func_list, key=lambda k: k['file_name'])

print(func_list)
write_output("output.csv", func_list)
