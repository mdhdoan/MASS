import csv
import json
from os import link
from queue import Empty
import urllib.request
# import os

def api_to_json(url):
    response_body = urllib.request.urlopen(url).read()
    return json.loads(response_body)

# Collect long, lat, sitename
# designs_link = 'https://www.monitoringresources.org/api/v1/designs'
# designs_jdata = api_to_json(designs_link)

# methods_link ='https://www.monitoringresources.org/api/v1/methods'
# methods_jdata = api_to_json(methods_link)

# # projects_link = 'https://www.monitoringresources.org/api/v1/projects'
# # projects_jdata = []

# programs_link = 'https://www.monitoringresources.org/api/v1/programs'
# programs_jdata = api_to_json(programs_link)

# protocols_link = 'https://www.monitoringresources.org/api/v1/protocols'
# protocols_jdata = api_to_json(protocols_link)

# # repositories_link = 'https://www.monitoringresources.org/api/v1/repositories'
# # repositories_jdata = []

studydesigns_link = 'https://www.monitoringresources.org/api/v1/studydesigns'
studydesigns_jdata = api_to_json(studydesigns_link)

# list_of_links = [designs_link, methods_link, programs_link, protocols_link, studydesigns_link]
# jdata_list = [designs_jdata, methods_jdata, programs_jdata, protocols_jdata, studydesigns_jdata]

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
#     org_list = programs_jdata_full[i]['organizations']
#     for org in org_list:
#         field_name = 'link_to_org'
#         if field_name not in programs_jdata_full[i]:
#             programs_jdata_full[i][field_name] = org
#         else:
#             programs_jdata_full[i][field_name] = programs_jdata_full[i][field_name] + '|' + org
#     i = i + 1

# print(programs_jdata_full[0])

# protocols_jdata_full = []
# i = 0
# for id_list in protocols_jdata:
#     # print(id_list)
#     jdata_url = str('https://www.monitoringresources.org/api/v1/protocols/'+ str(id_list['id']))
#     protocols_jdata_full.append(api_to_json(jdata_url))
#     url_list = protocols_jdata_full[i]['methods']
#     for url in url_list:
#         field_name = 'link_to'
#         if field_name not in protocols_jdata_full[i]:
#             protocols_jdata_full[i][field_name] = url
#         else:
#             protocols_jdata_full[i][field_name] = protocols_jdata_full[i][field_name] + '|' + url
#     # protocols_jdata_full[i]['tags'] = []
#     protocols_jdata_full[i]['metric_title'] = []
#     protocols_jdata_full[i]['metric_category'] = []
#     protocols_jdata_full[i]['metric_subcategory'] = []    
#     if protocols_jdata_full[i]['metrics']:
#         # print(protocols_jdata_full[i])
#         for metric in protocols_jdata_full[i]['metrics']:
#             #print(metric['title'], list(metric['title']))
#             if metric['title'] in protocols_jdata_full[i]['metric_title']:
#                 continue
#             else:
#                 protocols_jdata_full[i]['metric_title'].append(metric['title'])
#                 # protocols_jdata_full[i]['tags'].append(metric['title'])
#             if metric['category'] in protocols_jdata_full[i]['metric_category']:
#                 continue
#             else:
#                 protocols_jdata_full[i]['metric_category'].append(metric['category'])
#                 # protocols_jdata_full[i]['tags'].append(metric['category'])
#         # protocols_jdata_full[i]['tags'].append(protocols_jdata_full[i]['metric_category'])        
#             if metric['subcategory'] in protocols_jdata_full[i]['metric_subcategory']:
#                 continue
#             else:
#                 protocols_jdata_full[i]['metric_subcategory'].append(metric['subcategory'])
#                 # protocols_jdata_full[i]['tags'].append(metric['subcategory'])
#         i = i + 1 
#     else:
#         i = i + 1   

# print(protocols_jdata_full[0:3])

# methods_jdata_full = []
# for id_list in methods_jdata:
#     jdata_url = str('https://www.monitoringresources.org/api/v1/methods/'+ str(id_list['id']))
#     methods_jdata_full.append(api_to_json(jdata_url))
# print(methods_jdata_full)

# print(studydesigns_jdata[0])
# study_design_data = api_to_json("http://www.monitoringresources.org/api/v1/studyDesigns/1840")
# print(study_design_data)
# for keys, items in study_design_data.items():
#     print(keys, ": ", items, '\n')
# studydesigns_jdata_full = []
# for id_list in studydesigns_jdata:
#     jdata_url = str('https://www.monitoringresources.org/api/v1/studyDesigns/'+ str(id_list['id']))
#     studydesigns_jdata_full.append(api_to_json(jdata_url))
# print(studydesigns_jdata_full)


# print(designs_jdata[0])
# sites_data = api_to_json("http://www.monitoringresources.org/api/v1/designs/10/sites")
# for site in sites_data:
#     print(sites_data)
#     print(sites_data['results'])
#     print('fullname:' + "http://www.monitoringresources.org/api/v1/designs/10/sites/" + site['title'])
#     print(api_to_json("http://www.monitoringresources.org/api/v1/designs/10/sites/" + site['title']))

# import transformers
# from transformers import pipeline

# classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
# print('start')
# index = 0
# for protocol in protocols_jdata_full:
#     tag_label = []
#     if protocol['tags']:
#         index = index + 1
#         print(index)
#         print(protocol['tags'])
#         tag_label = protocol['tags']
#         for method_link in protocol['methods']:
#             # print(method_link)
#             for method in methods_jdata_full:
#                 method['tags'] = {}
#                 # print(method['url'])
#                 if method['url'] == method_link:
#                     # print(method['url'])
#                     for tag in tag_label:
#                         outputs = classifier(method['abstractText'], [tag])
#                         # print(type(outputs['labels'][0]), type(outputs['scores'][0]))
#                         method['tags'][outputs['labels'][0]] = outputs['scores'][0] # type: ignore
#         if index == 10:
#             break                
#     else: 
#         index = index + 1
#         print(index)
#         if index == 10:
#             break  
#         continue


# full_data_list = [programs_jdata_full, protocols_jdata_full, methods_jdata_full]
# len_list = len(full_data_list)

# for i in range(0, len_list):
# for data in methods_jdata_full:
#     # file_name = ((list_of_links[i][43:]) + '.tsv')
#     keys = methods_jdata_full[0].keys()
#     with open('methods.tsv', 'w', newline='') as output_file:
#         dict_writer = csv.DictWriter(output_file, keys, delimiter='\t')
#         dict_writer.writeheader()
#         dict_writer.writerows(methods_jdata_full)
