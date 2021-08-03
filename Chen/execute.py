import click
from download import *
from parse import *
from output import *

behaviors_json = read_json("behaviors.json")
suites_csv = read_csv("suites.csv")
func_list = list()
func_set = set()
status_dict = dict()
para_dict = dict()
for fun in behaviors_json["children"]:
    func_list.append(create_func_dict(fun, suites_csv, status_dict, para_dict))
    func_set.add(func_list[-1]["func_name"])
print(len(func_list))
func_set = sorted(func_set)
func_list = sort_func_list(func_list)
func_list_without_para = merge_para_func(status_dict, func_list, para_dict)
verify(func_set, func_list_without_para, status_dict)
write_output("output.csv", func_list_without_para)
