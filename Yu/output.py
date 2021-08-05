import csv
import os


def write_output(file_path, func_list):
    # cut input path with "/" to get filename
    file_path_list = file_path.split("/")
    file_name = file_path_list[-1]
    # get only path and filename
    file_path_list.remove(file_path_list[-1])
    final_path = "/".join(file_path_list)

    test = os.path.join(final_path, file_name)
    with open(test, "w") as out:
        # add heading
        csv.writer(out).writerow(
            [
                "suite",
                "file_name",
                "topology",
                "test_case",
                "status",
                "is_parameterize",
                "parameter",
            ]
        )

        # write content
        for func in func_list:
            csv.writer(out).writerow(list(func.values()))
