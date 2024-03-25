import csv
import neo4j
import sys

from langchain.chains.llm import LLMChain
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

URI = ''
AUTH = ('','')
neo4j_driver = ''

def increase_count(count, character):
    count += 1
    print(character, end="", flush=True)
    return count

def connect_gdb():
    with GraphDatabase.driver(URI, auth = AUTH) as driver:
        driver.verify_connectivity()
        neo4j_driver = driver
        neo4j_driver.verify_connectivity()

if __name__ == '__main__':
    file_name = sys.argv[1]
    metric_matching_data = {}
    metric_to_consider = ''
    method_data = []

    with open(file_name, 'r', encoding = 'utf-8-sig') as in_file:
        metric_matching_data = csv.DictReader(in_file)
        for row in metric_matching_data:
            metric_to_consider = row['metric_title']
            method_data.append({row['metric_title']: row['Textbody']})
    metric_to_consider = metric_matching_data
    print(method_data)

    # prompt_template = """
    # You are a helpful, respectful and honest assistant for labeling topics.

    # I have a list of title that contains the following text bodies in a list and stored as a dictionary (JSON format): 
    # {method_data}
    
    # The metric to consider is:
    # {metric_to_consider}

    # From the given list of title and context from the following text bodies, please return the most matching in terms of metric, and only the metric
    # """

    # llm = Ollama(model="mistral")
    # prompt = PromptTemplate(input_variables=["method_data", "metric_to_consider"], template=prompt_template)
    # llm_chain = LLMChain(llm=llm, prompt=prompt)

    # result = llm_chain.invoke({'method_data': method_data, 'metric_to_consider': metric_to_consider})
    # matching_title = result['text']
    # print(matching_title)
