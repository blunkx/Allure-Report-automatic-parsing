import re
import sys
import os
import shutil
import click
from download import download_wget
from output import write_output
import parsing


@click.command()
@click.option("-r", "--reportfile", "url", help="allure-report url.")
@click.option("-o", "--output", "path", help="allure-report url.")
def all_flow(url, path):
    if re.search(r"(http:\/\/)\S+", url) or re.search(r"https:\/\/\S+", url):
        download_wget(url)
    else:
        try:
            shutil.move(url, os.getcwd() + "/allure-report")
        except Exception:
            print("Path Error")
            sys.exit()

    json_array = parsing.read_json("behaviors.json")
    suites_rows = parsing.read_csv("suites.csv")
    func_list = list()
    parameterize = dict()
    parsing.create_dict(json_array, suites_rows, func_list, parameterize)

    parsing.edit_status(func_list)

    parsing.remove_suites_tests(func_list)

    func_list = sorted(func_list, key=lambda k: k["path_list"])
    func_list = sorted(func_list, key=lambda k: k["suite"])
    func_list = sorted(func_list, key=lambda k: k["file_name"])
    func_list = list({v["path_list"]: v for v in func_list}.values())

    print("case number:" + str(len(func_list)))
    if path is not None:
        write_output(path, func_list)
    else:
        print(func_list)


if __name__ == "__main__":
    all_flow()
