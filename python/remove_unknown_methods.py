import json
import os

with open('METRIC_METHOD_MATCHING_TEST_LIST_PASS.json', 'r') as json_file:
    json_data = json.load(json_file)
    for metric, method_details_list in json_data:
        for method_details in method_details_list:
            method_id = 
