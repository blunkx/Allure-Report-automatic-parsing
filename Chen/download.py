import wget
import os
import zipfile
import click

# url = input('Enter the url of the allure report: ')
# url += 'artifact/allure-report.zip'
# url = 'https://jenkins.clounix.com/job/sonic/job/testbed/job/201911.clounix/job/sonic-mgmt/40/artifact/allure-report.zip'


def parse():
    print("Parsing")


@click.command()
@click.option("--url", prompt="Enter the URL", help="Enter the url before artifact")
def get_url(url):
    url += "artifact/allure-report.zip"
    try:
        wget.download(url, os.getcwd())
    except:
        print(
            "Download failed, try again. Make sure you are connected the VPN and enter the correct URL."
        )
        exit()
    if not os.path.exists("allure-report.zip"):
        print("File doesn't exist!")
    else:
        with zipfile.ZipFile("allure-report.zip", "r") as zip_ref:
            try:
                zip_ref.extractall(os.getcwd())
                print("\nUnzip Done!")
            except:
                print("unzip failed!")
    if not os.path.isdir("allure-report/data/test-cases") or not os.path.isdir(
        "allure-report/data"
    ):
        print("Failed to open the directory, check the integrity of the zip file!")
        exit()
    parse()


@click.command()
@click.option(
    "--download",
    prompt="Download report? Enter T or F",
    help="Select parse only or download + parse",
)
def dl(download):
    if download == "T":
        url = get_url()

    elif download == "F":
        parse()
        return
    print("Erro, Plese enter T or F!")
    exit()


if __name__ == "__main__":
    dl()
