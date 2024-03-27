from bs4 import BeautifulSoup
import json
import os
from os import link
from urllib.request import FancyURLopener
from sympy import false
from torch import NoneType
from zmq import NULL

with open('./json_data/studydesigns_jdata.json', 'r') as study_design_file:
    study_designs_jdata = json.load(study_design_file)

extracted_study_design = {}
for key, value in study_designs_jdata.items():
    # print('Key: ', key, '\n\tValue: ', value)
    result_value = 'No valid data'
    for value_key, value_value in value.items():
        # print('Key: ', value_key, '\n\tValue: ', value_value, '\n')
        if value_value is None or type(value_value) is NoneType or value_value is NULL:
            continue
        if value_key == 'backgroundRationale':
            # print(value_value)
            value_temp = BeautifulSoup(value_value, 'html.parser').get_text(strip = True)
            result_value = ''.join([i if ord(i) < 128 else '' for i in value_temp])
        else:
            continue
    # print(result_value[:10])
    result_value = result_value.replace('\r', '')
    result_value = result_value.replace('\n', '')
    result_value = result_value.replace('\"', '')
    extracted_study_design['backgroundRationale'] = result_value
    
    for design_key, design_value in value.items():
        print(design_value, type(design_value))
        if not isinstance(design_value, str) and not isinstance(design_value, int) and design_key == 'backgroundRationale':
            print('Key not valid: ', design_key)
            continue
        else:
            print('Key existed')
            extracted_study_design[design_key] = design_value

    print(extracted_study_design)
    # print('Key: ', value['url'], '\n\t Value: ', result_value)
    save_path = 'json_data/study_designs/'
    os.makedirs('json_data/study_designs/', exist_ok = True)
    json_data = json.dumps(extracted_study_design, indent=2)
    file_name = extracted_study_design['name'].replace(':', '')
    file_name = file_name.replace('"', '')
    file_name = file_name.replace('<', 'less than ')
    file_name = os.path.join(save_path, file_name.replace('/', ' or ') + '.json')
    # print(file_name)
    with open(file_name, 'w+') as json_file:
        json_file.write(json_data)
    # break
# print(extracted_method)
        