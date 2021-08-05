"""
The module is supply multiple ways to download zip to exractall
    1. request
    2. wget
"""


from zipfile import ZipFile
import requests
import wget


def download_request(url):
    """
    Use request libiary to download zip and exractall

        Parameters:
                url (string): A download allure-report zip

        Returns:
                no return
    """
    report_zip = requests.get(url)
    with open("allure-report.zip", "wb") as code:
        code.write(report_zip.content)
    with ZipFile("allure-report.zip", "r") as zip_ref:
        zip_ref.extractall()


def download_wget(url):
    """
    Use wget libiary to download zip and exractall

        Parameters:
                url (string): A download allure-report zip

        Returns:
                no return
    """
    wget.download(url)
    with ZipFile("allure-report.zip", "r") as zip_ref:
        zip_ref.extractall()
        print()
