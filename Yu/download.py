import requests
import wget
from zipfile import ZipFile


def download_request(url):
    #use request libiary to download zip and exractall
    r = requests.get(url)
    code = open("allure-report.zip", "wb")
    code.write(r.content)
    code.close()
    zip_ref = ZipFile("allure-report.zip", "r")
    zip_ref.extractall()


def download_wget(url):
    #use wget libiary to download zip and exractall
    wget.download(url)
    zip_ref = ZipFile("allure-report.zip", "r")
    zip_ref.extractall()
    print()
