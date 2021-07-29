import wget
import os
import zipfile
import json
import re
import csv


def read_json(file_name):
    # read json -> dict
    json_path = os.getcwd()+'/allure-report/data/' + file_name
    try:
        input_file = open(json_path)
    except:
        print('Failed to open!')
    return json.load(input_file)


def read_csv(file_name):
    # read csv -> 2d list
    csv_path = os.getcwd()+'/allure-report/data/' + file_name
    try:
        input_file = open(csv_path)
    except:
        print('Failed to open!')
    return list(csv.reader(input_file, delimiter=','))


def create_func_dict(fun, suites_csv):
    for row in suites_csv:
        if fun['name'] == row[9]:
            suite = row[4].replace('.', '/')
            file_name = suite+'/'+row[5] + \
                '.py' if suite != '' else row[5]+'.py'
            path = file_name
            if row[6] != '':
                path += '::' + row[6]
    match = re.search("(\S+)(\[)(\S+)", fun["name"])
    func_name = match.group(1) if match else fun["name"]
    path += '::'+func_name
    uid_name = 'test-cases/'+fun["uid"]+'.json'
    temp = read_json(uid_name)
    topo_marker = [s for s in temp['extra']['tags'] if 'topology(' in s][0]
    func_dict = {'suite': suite, 'file_name': file_name, 'topo_marker': topo_marker,
                 'func_name': path, 'status': fun["status"], 'UID': fun["uid"]}
    return func_dict


def write_output(file_name, func_list):
    out = open(file_name, 'w', newline='')
    csv.writer(out).writerow(list(func_list[0].keys()))
    for func in func_list:
        csv.writer(out).writerow(list(func.values()))


behaviors_json = read_json('behaviors.json')
suites_csv = read_csv('suites.csv')
'''
print(suites_csv[0][9])
for row in suites_csv:
    print(row)
'''
func_list = list()
for fun in behaviors_json["children"]:
    func_list.append(create_func_dict(fun, suites_csv))


func_list = sorted(func_list, key=lambda k: k['func_name'])
func_list = sorted(func_list, key=lambda k: k['suite'])
func_list = sorted(func_list, key=lambda k: k['file_name'])
write_output('output.csv', func_list)
