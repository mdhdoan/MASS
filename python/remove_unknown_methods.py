import json
import os

metric_data = []
load_data = []
with open('METRIC_METHOD_MATCHING_TEST_LIST_PASS.json', 'r') as json_file:
    for metric_data in json_file:
        metric_method_dict = json.load(metric_data)
        holder_metric = {}
        for metric, methods in metric_method_dict:
            print(metric)
            method_list = []
            for method in methods:
                if method[1] != "DESCRIPTION NOT FOUND, TITLE MIGHT BE HALLUCINATING":
                    method_list.append(method[0])
            holder_metric[metric] = method_list
            metric_data.append(holder_metric)
        print(metric_data)
        break