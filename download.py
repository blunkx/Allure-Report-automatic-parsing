import wget
import os
import zipfile

#url = input('Enter the url of the allure report: ')
#url += 'artifact/allure-report.zip'
url = 'https://jenkins.clounix.com/job/sonic/job/testbed/job/201911.clounix/job/sonic-mgmt/40/artifact/allure-report.zip'
try:
    wget.download(url, os.getcwd())
except:
    print('Download failed, try again. Make sure you are connected the VPN')
    exit()
if not os.path.exists('allure-report.zip'):
    print('File doesn\'t exist!')
else:
    with zipfile.ZipFile('allure-report.zip', 'r') as zip_ref:
        try:
            zip_ref.extractall(os.getcwd())
            print('\nUnzip Done!')
        except:
            print('unzip failed!')
if not os.path.isdir('allure-report/data/test-cases') or not os.path.isdir('allure-report/data'):
    print('Failed to open the directory, check the integrity of the zip file!')
    exit()
