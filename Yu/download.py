from zipfile import ZipFile
import requests
import wget


def download_request(url):
    # use request libiary to download zip and exractall
    report_zip = requests.get(url)
    with open("allure-report.zip", "wb") as code:
        code.write(report_zip.content)
    with ZipFile("allure-report.zip", "r") as zip_ref:
        zip_ref.extractall()


def download_wget(url):
    # use wget libiary to download zip and exractall
    wget.download(url)
    with ZipFile("allure-report.zip", "r") as zip_ref:
        zip_ref.extractall()
        print()
