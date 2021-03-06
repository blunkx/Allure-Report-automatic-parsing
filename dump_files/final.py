import wget
import os
import zipfile
import json
import re
import csv


def download():
    # url = input('Enter the url of the allure report: ')
    # url += 'artifact/allure-report.zip'
    url = "https://jenkins.clounix.com/job/sonic/job/testbed/job/201911.clounix/job/sonic-mgmt/40/artifact/allure-report.zip"
    try:
        wget.download(url, os.getcwd())
    except Exception:
        print("Download failed, try again. Make sure you are connected the VPN")
        exit()
    if not os.path.exists("allure-report.zip"):
        print("File doesn't exist!")
    else:
        with zipfile.ZipFile("allure-report.zip", "r") as zip_ref:
            try:
                zip_ref.extractall(os.getcwd())
                print("\nUnzip Done!")
            except Exception:
                print("unzip failed!")
    if not os.path.isdir("allure-report/data/test-cases") or not os.path.isdir(
        "allure-report/data"
    ):
        print("Failed to open the directory")
        exit()


def read_json(file_name):
    # read json -> dict
    json_path = os.getcwd() + "/allure-report/data/" + file_name
    try:
        input_file = open(json_path)
    except Exception:
        print("Failed to open Json!")
        exit()
    return json.load(input_file)


def read_csv(file_name):
    # read csv -> 2d list
    csv_path = os.getcwd() + "/allure-report/data/" + file_name
    try:
        input_file = open(csv_path)
    except Exception:
        print("Failed to open CSV!")
        exit()
    return list(csv.reader(input_file, delimiter=","))


def check_path(fullname, row_from_suite):
    name = row_from_suite[4:9]
    name = [x for x in name if x != ""]
    for i in name:
        if i not in fullname:
            return False
    return True


def create_func_dict(fun, suites_csv, status_dict):
    uid_name = "test-cases/" + fun["uid"] + ".json"
    temp = read_json(uid_name)
    for row in suites_csv:
        if fun["name"] == row[9]:
            row[4] = "" if row[4] == "tests" else row[4]
            suite = row[4].replace(".", "/")
            file_name = suite + "/" + row[5] + ".py" if suite != "" else row[5] + ".py"
            path = file_name
            if row[6] != "" and "[" not in row[6]:
                path += "::" + row[6]
            match = re.search("(\S+)(\[)(\S+)", fun["name"])
            func_name = match.group(1) if match else fun["name"]
            path += "::" + func_name
            if check_path(temp["fullName"], row):
                break
    topo_marker = [s for s in temp["extra"]["tags"] if "topology(" in s][0]
    func_dict = {
        "suite": suite,
        "file_name": file_name,
        "topo_marker": topo_marker,
        "func_name": path,
        "status": fun["status"],
        "UID": fun["uid"],
    }
    if path not in status_dict:
        status_dict[path] = [fun["status"]]
    else:
        status_dict[path] += [fun["status"]]
    return func_dict


def merger_para_func(status_dict, func_list):
    new_list = func_list = list({v["func_name"]: v for v in func_list}.values())
    for row in new_list:
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


def verify(func_set, func_list_without_para, status_dict):
    # check that each function in func_set also exists in the func_list_without_para
    func_name_list = [
        v["func_name"] for v in func_list_without_para if v["func_name"] in func_set
    ]
    for func in func_name_list:
        try:
            status_dict[func]
        except Exception:
            print("Error!")
            exit()
    print(len(func_set))
    print(len(func_name_list))
    print(len(status_dict))


def write_output(file_name, func_list):
    out = open(file_name, "w", newline="")
    row = list(func_list[0].keys())
    del row[-1]
    csv.writer(out).writerow(row)
    for func in func_list:
        row = list(func.values())
        del row[-1]
        csv.writer(out).writerow(row)


print("Start Pasring!") if input(
    "Enter 1 to parse only, 2 to download and parse: "
) == "1" else download()
behaviors_json = read_json("behaviors.json")
suites_csv = read_csv("suites.csv")
func_list = list()
func_set = set()
status_dict = dict()
for fun in behaviors_json["children"]:
    func_list.append(create_func_dict(fun, suites_csv, status_dict))
    func_set.add(func_list[-1]["func_name"])
print(len(func_list))
func_set = sorted(func_set)
func_list = sorted(func_list, key=lambda k: k["func_name"])
func_list = sorted(func_list, key=lambda k: k["suite"])
func_list = sorted(func_list, key=lambda k: k["file_name"])
func_list_without_para = merger_para_func(status_dict, func_list)
verify(func_set, func_list_without_para, status_dict)
write_output("output.csv", func_list_without_para)
