import wget
import os
import zipfile
import json
import re


json_path = os.getcwd()+'/allure-report/data/' + 'categories.json'
try:
    input_file = open(json_path)
except:
    print('Failed to open!')
json_dict = json.load(input_file)
print(type(json_dict))

for it in json_dict:
    a = type(it)
    print(a)
