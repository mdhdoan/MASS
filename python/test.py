import json
import os
import random
import sys

from langchain.chains.llm import LLMChain
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

random.seed(2024)

HEADERS = [
    "abstractText"
]
NAME = [
    "title"
]

def increase_count(count, character):
    count += 1
    print(character, end="", flush=True)
    return count


if __name__ == '__main__':
    in_path, documents, count = sys.argv[1], {}, 0
    for file in os.listdir(in_path):
        file_name = os.path.join(in_path, file)
        if not os.path.isfile(file_name) or not file_name.endswith('.json'):
            continue
        with open(file_name, 'rt', encoding='utf-8') as in_file:
            doc = json.load(in_file)
            try:
                for key, value in doc.items():
                    documents[doc['title']] = doc['abstractText']
            except Exception as e:
                print(f"\n{file_name}")
            count = increase_count(count, '.')
    print(f"\nRead {count} documents.\n")
    
    # topics, probs = topic_model.fit_transform(documents, embeddings)
    prompt_template = """
    You are a helpful, honest assistant for labeling topics.

    I have the following method: 
    ```{method}```
    
    I have the following structure of methods ontology:
    SITE:
        Habitat:
            Physical:
                Flow
                Temperature
                Structure
            Ecological
            Chemical:
                Pollutant
                Constituents

    I want you to sort the method into the appropriate methods ontology above, and where possible, please add more where relevant.
    This is the structure of the answer I want:
    < WHERE IT BELONGS | REASON WHY IT BELONGS THERE >
    
    RETURN your answer based on my structure above.
    If your answer has any code in it, generate again. 
    """
    llm = Ollama(model="mixtral")
    prompt = PromptTemplate(input_variables=["method"], template=prompt_template)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    # print(len(documents))
    sorted_methods = {}
    count = 0
    for title, method in documents.items():
        result = llm_chain.invoke({'method': method})
        sorted_methods[title] = result['text']
        count = increase_count(count, '.')
    with open('sorted_methods.json', 'w+') as result_file:
        ontology_data = json.dumps(sorted_methods, indent = 2)
        result_file.write(ontology_data)
    