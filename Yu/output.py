import csv


def write_output(file_name, func_list):
    out = open(file_name, "w")
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
