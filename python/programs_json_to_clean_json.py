import json
import os
from os import link
from zmq import NULL

with open('json_data/programs_jdata.json', 'r') as program_file:
    programs_jdata = json.load(program_file)

extracted_program = {}
for key, value in programs_jdata.items():
    extracted_program['url'] = value['url']
    extracted_program['title'] = value['name']
    extracted_program['id'] = value['id']
    extracted_program['primaryContactName'] = value['primaryContactName']
    extracted_program['primaryContactEmail'] = value['primaryContactEmail']
    extracted_program['organizations'] = value['organizations']
    extracted_program['protocols'] = value['protocols']

    # print('Key: ', value['url'], '\n\t Value: ', result_value)
    save_path = 'json_data/programs/'
    os.makedirs('json_data/programs/', exist_ok = True)
    json_data = json.dumps(extracted_program, indent=2)
    file_name = extracted_program['title'].replace(':', '')
    file_name = file_name.replace('"', '')
    file_name = file_name.replace('<', 'less than ')
    file_name = os.path.join(save_path, file_name.replace('/', ' or ') + '.json')
    # print(file_name)
    with open(file_name, 'w+') as json_file:
        json_file.write(json_data)
    # break
# print(extracted_method)
        