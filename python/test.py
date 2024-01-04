import csv
import json
from os import link
import urllib.request
from urllib.request import FancyURLopener
# import os

def api_to_json(url):
    response_body = urllib.request.urlopen(url).read()
    return json.loads(response_body)

# designs_link = 'https://www.monitoringresources.org/api/v1/designs'
# designs_jdata = []
methods_link ='https://www.monitoringresources.org/api/v1/methods'
methods_jdata = api_to_json(methods_link)
# projects_link = 'https://www.monitoringresources.org/api/v1/projects'
# projects_jdata = []
programs_link = 'https://www.monitoringresources.org/api/v1/programs'
programs_jdata = api_to_json(programs_link)
protocols_link = 'https://www.monitoringresources.org/api/v1/protocols'
protocols_jdata = api_to_json(protocols_link)
# repositories_link = 'https://www.monitoringresources.org/api/v1/repositories'
# repositories_jdata = []
# studydesigns_link = 'https://www.monitoringresources.org/api/v1/studydesigns'
# studydesigns_jdata =[]

# collection_event_request = urllib.request.Request(collection_event_link, method = 'PUT')
# print(collection_event_request)
# response_body = urllib.request.urlopen(collection_event_request)
# collection_event_jdata = json.load(response_body)
# print(collection_event_jdata)


list_of_links = [methods_link, programs_link, protocols_link]
jdata_list = [methods_jdata, programs_jdata, protocols_jdata]

# programs_jdata_full = []
# i = 0
# for id_list in programs_jdata:
#     jdata_url = str('https://www.monitoringresources.org/api/v1/programs/'+ str(id_list['id']))
#     programs_jdata_full.append(api_to_json(jdata_url))
#     url_list = programs_jdata_full[i]['protocols']
#     for url in url_list:
#         field_name = 'link_to'
#         if field_name not in programs_jdata_full[i]:
#             programs_jdata_full[i][field_name] = url['url']
#         else:
#             programs_jdata_full[i][field_name] = programs_jdata_full[i][field_name] + '|' + url['url']
#     i = i + 1
# # print(programs_jdata[0:3])

# protocols_jdata_full = []
# i = 0
# for id_list in protocols_jdata:
#     # print(id_list)
#     jdata_url = str('https://www.monitoringresources.org/api/v1/protocols/'+ str(id_list['id']))
#     protocols_jdata_full.append(api_to_json(jdata_url))
#     url_list = protocols_jdata_full[i]['methods']
#     url_string = ''
#     for url in url_list:
#         url_string = url_string + '|' + url
#     protocols_jdata_full[i]['link_to'] = url_string
#     i = i + 1
# print(protocols_jdata_full[0:3])

# methods_jdata_full = []
# for id_list in methods_jdata:
#     jdata_url = str('https://www.monitoringresources.org/api/v1/methods/'+ str(id_list['id']))
#     methods_jdata_full.append(api_to_json(jdata_url))
#     # print(methods_jdata_full)

# protocols_jdata_full = []
# i = 0
# for id_list in protocols_jdata:
#     # print(id_list)
#     jdata_url = str('https://www.monitoringresources.org/api/v1/protocols/'+ str(id_list['id']))
#     protocols_jdata_full.append(api_to_json(jdata_url))
#     url_list = protocols_jdata_full[i]['methods']
#     url_string = ''
#     for url in url_list:
#         url_string = url_string + '|' + url
#     protocols_jdata_full[i]['link_to'] = url_string
#     i = i + 1





# full_data_list = [programs_jdata_full, protocols_jdata_full, methods_jdata_full]
# len_list = len(full_data_list)

# for i in range(0, len_list):
# for data in protocols_jdata_full:
#     # file_name = ((list_of_links[i][43:]) + '.tsv')
#     keys = protocols_jdata_full[0].keys()
#     with open('protocols.tsv', 'w', newline='') as output_file:
#         dict_writer = csv.DictWriter(output_file, keys, delimiter='\t')
#         dict_writer.writeheader()
#         dict_writer.writerows(protocols_jdata_full)

