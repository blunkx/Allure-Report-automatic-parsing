from download import *
from parsing import *
from output import *
import click


@click.command()
@click.option("--url", help="allure-report url.")
def all_flow(url):
    download_wget(url)
    json_array = read_json("behaviors.json")
    suites_rows = read_csv("suites.csv")
    func_list = list()
    parameterize = dict()
    create_dict(json_array, suites_rows, func_list, parameterize)

    edit_status(func_list)

    remove_suites_tests(func_list)

    func_list = sorted(func_list, key=lambda k: k["path_list"])
    func_list = sorted(func_list, key=lambda k: k["suite"])
    func_list = sorted(func_list, key=lambda k: k["file_name"])
    func_list = list({v["path_list"]: v for v in func_list}.values())

    print("case number:" + str(len(func_list)))
    write_output("output.csv", func_list)


if __name__ == "__main__":
    all_flow()
