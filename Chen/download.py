import wget
import os
import zipfile
import shutil


def check_input(input):
    if os.path.exists(input):
        target = os.getcwd() + "/allure-report.zip"
        shutil.copyfile(input, target)
        if ".zip" in input:
            extract()
    elif "http" in input:
        download(input)
    else:
        print("Fail to find the file!")
        exit()


def download(url):
    url += "artifact/allure-report.zip"
    # url = "https://jenkins.clounix.com/job/sonic/job/testbed/job/201911.clounix/job/sonic-mgmt/40/artifact/allure-report.zip"
    try:
        wget.download(url, os.getcwd())
        print()
    except Exception:
        print("Download failed, try again. Make sure you are connected the VPN!")
        exit()


def extract():
    if not os.path.exists("allure-report.zip"):
        print("File doesn't exist!")
        exit()
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
