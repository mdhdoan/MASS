from bs4 import BeautifulSoup
import json
import os
import urllib.request
import urllib.error
from os import link
from urllib.request import FancyURLopener
from sympy import false
from torch import NoneType
from zmq import NULL

# with open('studydesigns_jdata.json', 'r') as study_design_file:
#     study_designs_jdata = json.load(study_design_file)

# with open('protocols_jdata.json', 'r') as protocol_file:
#     protocols_jdata = json.load(protocol_file)

with open('./json_data/methods_jdata.json', 'r') as method_file:
    methods_jdata = json.load(method_file)

# print(type(study_designs_jdata))
# extracted_study_design = {}
# for key, value in study_designs_jdata.items():
#     # print('Key: ', key, '\n\tValue: ', value)
#     result_value = ''
#     for value_key, value_value in value.items():
#         # print(key, value)
#         if value_value is None or type(value_value) is NoneType:
#             continue
#         if value_key == 'backgroundRationale' or value_key == 'keyAssumptions' or value_key == 'qualityControlConsiderations' or value_key == 'trainingRequirements' or value_key == 'safetyConsiderations':
#             if result_value == '': 
#                 result_value = value_value
#             else:
#                 # print(result_value, ' | ', value_value)
#                 result_value = result_value + ' ' + value_value
#         else:
#             continue
#     extracted_study_design[value['url']] = result_value

# extracted_protocol = {}
# for key, value in protocols_jdata.items():
#     # print('Key: ', key, '\n\tValue: ', value)
#     result_value = ''
#     for value_key, value_value in value.items():
#         print('Key: ', value_key, '\n\tValue: ', value_value, '\n')
#         if value_value is None or type(value_value) is NoneType:
#             continue
#         if value_key == 'assumptions' or value_key == 'background':
#             if result_value == '': 
#                 result_value = value_value
#             else:
#                 # print(result_value, ' | ', value_value)
#                 result_value = result_value + ' ' + value_value
#         else:
#             continue
#     extracted_protocol[value['url']] = result_value

extracted_method = {}
for key, value in methods_jdata.items():
    # print('Key: ', key, '\n\tValue: ', value)
    result_value = 'No valid data'
    for value_key, value_value in value.items():
        # print('Key: ', value_key, '\n\tValue: ', value_value, '\n')
        if value_value is None or type(value_value) is NoneType or value_value is NULL:
            continue
        if value_key == 'abstractText':
            # print(value_value)
            value_temp = BeautifulSoup(value_value, 'html.parser').get_text(strip = True)
            result_value = ''.join([i if ord(i) < 128 else '' for i in value_temp])
            # value_no_
            # result_value
        else:
            continue
    # print(result_value[:10])
    result_value = result_value.replace('\r', '')
    result_value = result_value.replace('\n', '')
    result_value = result_value.replace('\"', '')
    extracted_method['abstractText'] = result_value
    extracted_method['url'] = value['url']
    # print('Key: ', value['url'], '\n\t Value: ', result_value)
    save_path = 'json_data/methods/'
    os.makedirs('json_data/methods/', exist_ok = True)
    json_data = json.dumps(extracted_method, indent=2)
    file_name = os.path.join(save_path, value['title'].replace('/', ' or ') + '.json')
    # print(file_name)
    with open(file_name, 'w+') as json_file:
        json_file.write(json_data)
    # break
# print(extracted_method)
        