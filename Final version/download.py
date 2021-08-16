"""
The module include methods to check url and path.
It also provides methods to download and extract the allure-report.
Method list:
    check_input
    download
    extract
"""
import os
import zipfile
import shutil
import sys
import wget


def check_input(input_from_r):
    """
    Determine whether the input is an url or a path.
    Args:
        input_from_r(str): the argument from user
    Returns:
        None
    """
    if os.path.exists(input_from_r):
        target = os.path.join(os.getcwd() + "allure-report.zip")
        shutil.copyfile(input_from_r, target)
        if ".zip" in input_from_r:
            extract()
    elif "http" in input_from_r:
        download(input_from_r)
    else:
        print("Fail to find the file!")
        sys.exit()


def download(url):
    """
    Download the file from url by using wget.
    If download failed, throw an exception.
    Args:
        url(str)
    Returns:
        None

    """
    # url = os.path.join(url, "artifact", "allure-report.zip")
    print(url)
    try:
        wget.download(url, os.getcwd())
    except Exception:
        print("Download failed, try again. Make sure you are connected the VPN!")
        sys.exit()
    extract()


def extract():
    """
    Extract the zip file at work directory.
    If extract failed, throw an exception.
    Args:
        None
    Returns:
        None
    """
    if not os.path.exists("allure-report.zip"):
        print("File doesn't exist!")
        sys.exit()
    else:
        with zipfile.ZipFile("allure-report.zip", "r") as zip_ref:
            try:
                zip_ref.extractall(os.getcwd())
                print("\nUnzip Done!")
            except Exception:
                print("unzip failed!")

    if not os.path.isdir(
        os.path.join("allure-report", "data", "test-cases")
    ) or not os.path.isdir(os.path.join("allure-report", "data")):
        print("Failed to open the directory")
        sys.exit()
