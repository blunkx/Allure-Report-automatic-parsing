import wget
import os
import zipfile

for i in range(1, 40):
    url = "https://jenkins.clounix.com/job/sonic/job/testbed/job/201911.clounix/job/sonic-mgmt/" + \
        str(i) + "/artifact/allure-report.zip"
    try:
        wget.download(url, os.getcwd())
        print("\n#"+str(i))
    except:
        print('Download failed, try again. Make sure you are connected the VPN')
