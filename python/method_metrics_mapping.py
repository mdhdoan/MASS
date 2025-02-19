import csv
import json
from neo4j import GraphDatabase
from pathlib import Path
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
        Please return in a python list with each method title same as below
            [comma separated list of methods name, each surrounded by single quotation mark]
        Check on your list within the desired format that it only contains method titles, and nothing else. 
        In your response, no need to include any additional words besides the desired output.
        """


if __name__ == '__main__':  
    file_name = sys.argv[1]

    metric_matching_data = csv_to_list_of_dicts(file_name)
    # print(metric_matching_data)

    llm = Ollama(model="llama3.3")
    prompt = PromptTemplate(input_variables=["metric_dict", "method_dict"], template=prompt_template)
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    method_dict = {}
    metric_dict = {}
    protocol_dict = {}
    protocol_list = []
    path = Path('./bad_metrics.txt')
    if path.exists():
        with open('bad_metrics.txt', 'r') as bad_metric_records:
            content = bad_metric_records.read()
            bad_metric_list = content.strip('[]').split(',')
    else:
        bad_metric_list = []

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

    total_protocol = len(protocol_dict)
    protocol_counter = 0
    # test_result = {}
    fail_counter = 0
    metric_counter = 0
    total_metrics = 0
    for protocol_id, metrics in protocol_dict.items():
        print('protocol #', protocol_counter, 'out of', total_protocol, 'id:', protocol_id)
        total_metrics_in_protocol = len(metrics)
        # print('List of Metrics: ', metrics)
        # print('Begin mistral with protocol number ' + protocol_id + ' and metric:', end = ' ')
        # break
        metric_total_fail_counter = 0
        for metric in metrics:
            metric_fail_counter = 0
            metric_counter += 1
            print('Metric:', metric, end = '... ')
            # print(metric + ' and a list of ', len(metric_dict[metric]), ' methods')
            # print(metric + ' and a list of methods: ' + str(metric_dict[metric]))
            comparable_method_dict = {}
            for method in metric_dict[metric]:
                # print(method) #, method_dict[method])
                comparable_method_dict[method] = method_dict[method]
            # result['text'] = 'holder'
            # print('--- BEGIN Mistral work --- ')
            result = llm_chain.invoke({'metric_dict': metric, "method_dict": comparable_method_dict})
            matching_title = result['text']
            # print('--- END Mistral work --- ')
            # print(metric + ' has the closest matching result as: \n\t' + matching_title)
            test_result = {}
            # test_result[metric] = matching_title
            try:
                json_matching_result = eval(matching_title)
            except:
                bad_metric_list.append(metric)
                fail_counter += 1
                metric_fail_counter +=1
                with open('METRIC_METHOD_MATCHING_TEST_LIST_Interrupted.json', 'a') as test_result_file:
                    test_result['ERROR NOTE'] = 'MISTRAL DID NOT GIVE A USABLE LIST\n' + matching_title
                    writing_data = json.dumps(test_result, indent = 4)
                    test_result_file.write(writing_data)
                    print('fail - bad list')
                    print('Completed with fail rate: ' + str(metric_fail_counter) + ' out of ' + str(total_metrics_in_protocol) + ' with metric ' + str(metric))
                    # print('Writing to FAILED file...')
                    continue
            for method in json_matching_result:
                # print(method_dict[method])
                if method not in method_dict:
                    try:
                        description = method_dict[method + str(' v1.0')]
                    except: 
                        metric_fail_counter += 1
                        bad_metric_list.append(metric)
                        description = 'DESCRIPTION NOT FOUND, TITLE MIGHT BE HALLUCINATING'
                else:
                    description = method_dict[method]

                if metric not in test_result:
                    # print('Metric ', metric, ' not included yet')
                    test_result[metric] = [[method, description]]
                else:
                    test_result[metric].append([method, description])
            print('PASS')
            # print('Writing to PASS file...')
            with open('METRIC_METHOD_MATCHING_TEST_LIST_PASS.json', 'a+') as test_result_file:
                writing_data = json.dumps(test_result, indent = 4)
                test_result_file.write(writing_data + ',\n')
            print('Completed with fail rate: ' + str(metric_fail_counter) + ' methods out of ' + str(total_metrics_in_protocol) + ' with metric ' + str(metric))
            metric_total_fail_counter += metric_fail_counter
            total_metrics += total_metrics_in_protocol
            print('total metrics so far:', total_metrics)
            print('NEXT METRIC\n')

        print('Completed with fail rate: ' + str(metric_total_fail_counter) + ' methods out of ' + str(total_metrics) + ' with protocol ID ' + str(protocol_id) +'\n\n')
        protocol_counter = protocol_counter + 1
        fail_counter += metric_total_fail_counter
        # total_metrics += total_metrics_in_protocol
        print('total metrics so far:', total_metrics)
        # if protocol_counter == 2:
        #     break
        # else:
        #     continue
    print('Completed with fail rate: ' + str(fail_counter) + ' metrics out of ' + str(total_metrics) + ' with ' + str(total_protocol) + ' protocols')
    for metric in bad_metric_list:
        with open('bad_metrics.txt', 'a+') as bad_metric_records:
            bad_metric_records.write(str(metric))
    # Mar 28 Completed with fail rate: 63metrics out of 2108 with 322 protocols
    # AUG 27 Completed with fail rate: 3357 metrics out of 26714 with 322 protocols
    # AUG 27 Completed with fail rate: 2242 metrics out of 27502 with 322 protocols
