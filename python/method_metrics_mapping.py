import csv
import json
from neo4j import GraphDatabase
import sys

from langchain.chains.llm import LLMChain
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

URI = ''
AUTH = ('','')
neo4j_driver = ''

def connect_gdb():
    with GraphDatabase.driver(URI, auth = AUTH) as driver:
        driver.verify_connectivity()
        neo4j_driver = driver
        neo4j_driver.verify_connectivity()

def csv_to_list_of_dicts(filename, delimiter=','):
    result_list = []
    with open(filename, 'r', encoding = 'utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        for row in reader:
            for key, value in row.items():
                row[key] = value.replace('"', '')
            result_list.append(dict(row))
    return result_list

prompt_template = """
        You are a helpful and careful assistant for labeling topics.
        I am giving you two dictionaries called the metric dictionary and the method dictionary. 
        
        The metric dictionary is a dictionary of metric titles keys, and their potential matching method titles as values.
        Here is the metric dictionary: {metric_dict}

        The method dictionary is a dictionary of method titles as keys, and their description as their values.
        Here is the method dictionary: {method_dict}

        I need you to match each metric to the closest matching method given their description
        Return for me a list of methods name ONLY.
        Do not give me any additional texts.
        If your response contains anything other than the list of method names, remove them.
        """


if __name__ == '__main__':  
    file_name = sys.argv[1]

    metric_matching_data = csv_to_list_of_dicts(file_name)
    # print(metric_matching_data)

    llm = Ollama(model="mistral")
    prompt = PromptTemplate(input_variables=["metric_dict", "method_dict"], template=prompt_template)
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    method_dict = {}
    metric_dict = {}
    protocol_dict = {}
    protocol_list = []
    prev_metric = ''
    for row in metric_matching_data:
        # print(row)
        # print('metric: ' + row['metric_title'] + ' | pid: ' + row['pid'] + ' | method_title: ' + row['method_title'])
        method_dict[row['method_title']] = row['method_text']
        # print(method_dict)
        if row['metric_title'] in metric_dict:
            # print(metric_dict[row['metric_title']])
            if row['method_title'] not in metric_dict[row['metric_title']]:
                metric_dict[row['metric_title']].append(row['method_title'])
        else:
            metric_dict[row['metric_title']] = [row['method_title']]
        # print(metric_dict)
        if row['pid'] in protocol_dict:
            if row['metric_title'] not in protocol_dict[row['pid']]:
                protocol_dict[row['pid']].append(row['metric_title'])
        else:
            protocol_dict[row['pid']] = [row['metric_title']]
            # print(protocol_dict[row['pid']])
        # print(protocol_dict)
        # protocol_list.append(row['pid'])
        # break
    # protocol_list = list(set(protocol_list))

    test = 0
    test_result = {}
    for protocol_id, metrics in protocol_dict.items():
        print('List of Metrics: ', metrics)
        print('Begin mistral with protocol number ' + protocol_id + ' and metric: ', end = '')
        # break
        for metric in metrics:
            print(metric + ' and a list of methods: ' + str(metric_dict[metric]))
            comparable_method_dict = {}
            for method in metric_dict[metric]:
                # print(method) #, method_dict[method])
                comparable_method_dict[method] = method_dict[method]
            # result['text'] = 'holder'
            print('--- BEGIN Mistral work --- ')
            result = llm_chain.invoke({'metric_dict': metric, "method_dict": comparable_method_dict})
            matching_title = result['text']
            print('--- END Mistral work --- ')
            print(' which has the closest mathing result to be: \n\t' + matching_title)
            # test_result[metric] = matching_title
            json_matching_result = eval(matching_title)
            for method in json_matching_result:
                # print(method_dict[method])
                if method not in method_dict:
                    try:
                        method_dict[method + str(' v1.0')]
                    except: 
                        description = 'DESCRIPTION NOT FOUND, TITLE MIGHT BE HALLUCINATING'
                else:
                    description = method_dict[method]
                if metric not in test_result:
                    test_result[metric] = [[method, description]]
                else:
                    test_result[metric].append([method, description])
                
            print('NEXT METRIC\n\n')
        print('Writing to file...')
        with open('METRIC_METHOD_MATCHING_TEST_LIST.json', 'w+') as test_result_file:
            writing_data = json.dumps(test_result, indent = 4)
            test_result_file.write(writing_data)
        test = test + 1
        if test == 10:
            break
        else:
            continue
