import csv
import os


def write_output(file_path, func_list):
    file_path_list = file_path.split("/")
    file_name = file_path_list[-1]
    file_path_list.remove(file_path_list[-1])
    final_path = "/".join(file_path_list)
    test = os.path.join(final_path, file_name)
    out = open(test, "w")
    csv.writer(out).writerow(
        [
            "suite",
            "file_name",
            "topology",
            "test_case",
            "status",
            "is_parameterixe",
            "parameter",
        ]
    )

    for func in func_list:
        csv.writer(out).writerow(list(func.values()))
