import json
import numpy
import os
import pandas as pd
import random
import sklearn
import sys

from umap import UMAP
from hdbscan import HDBSCAN
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer

from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired
from bertopic.vectorizers import ClassTfidfTransformer

from langchain.chains.llm import LLMChain
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.schema import Document

random.seed(2024)

############################## AI PROMPTS ###################################
keywords_prompt = """
    You are a helpful, respectful and succinct assistant for labeling topics.

    I have a text body as seen below:
    {content}

    Create a list of highly relevant keywords relevant to the method. These keywords can serve as quick references to the main topics and themes covered. Aiming to limit to 5.
    The list shoule be a comma separated list, on one line.
    If your answer has any code in it, generate again. 
    """

abstract_prompt = """
    You are a helpful, respectful and succinct assistant for labeling topics.

    I have a text body as seen below:
    {content}

    Summarize the method in a comprehensive high-level, non-technical focus overview of the method, explaining its necessity and how it solves any issues raised. 
    
    If your answer has any code in it, generate again. 
    """

value_prompt = """
    You are a helpful, respectful and succinct assistant for labeling topics.

    I have a text body as seen below:
    {content}

    I need you to provide me the potential values and explain why should we invest money into this
    If your answer has any code in it, generate again.
"""

problem_statement_prompt = """
    You are a helpful, respectful and succinct assistant for labeling topics.

    I have a text body as seen below:
    {content}

    I need you to provide me the problem the protocol is trying to solve.
    If your answer has any code in it, generate again.
"""

desired_outcomes_prompt = """
    You are a helpful, respectful and succinct assistant for labeling topics.

    I have a text body as seen below:
    {content}

    I need you to provide me the desired outcome that is stated from the protocol.
    If your answer has any code in it, generate again.
"""

description_prompt = """
    You are a helpful, respectful and succinct assistant for labeling topics.

    I have a text body as seen below:
    {content}

    Provide a description that is technical focus, use the terms from the method as closely as possible, closely following the given content in a more detailed description of the text body. Focus indepth into the content and provide explanation where applicable.
    
    If your answer has any code in it, generate again. 
    """

objectives_prompt = """
    You are a helpful, respectful and succinct assistant for labeling topics.

    I have a text body as seen below:
    {content}
    Describe the objectives in detail, include two points about the Summary of Solution Coverage: How much of the problem statement is this objective covering, and Keywords: List specific keywords or specifics related to the objective. 
    If your answer has any code in it, generate again.
    """

target_prompt = """
    You are a helpful, respectful and succinct assistant for labeling topics.

    I have a text body as seen below:
    {content}

    Specifies the primary focus or goal of the method within 5 words.

    If your answer has any code in it, generate again. 
    """

constraint_prompt = """
    You are a helpful, respectful and succinct assistant for labeling topics.

    I have a text body as seen below:
    {content}

    Read through it and find what constraints are applicable to the method and where in the method it's stated so. If not, then please provide a detailed explanation why that constraint is there.
    If your answer has any code in it, generate again. 
    """

############################## Custom functions ###################################

def increase_count(count, character):
    count += 1
    print(character, end="", flush=True)
    return count

def feed_llm(prompt, text_content):
    llm = Ollama(model="mistral")
    prompt = PromptTemplate(input_variables=["content"], template=prompt)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    # print('Begin Mixtral')
    result = llm_chain.invoke({'content': text_content})
    # print('Mixtral complete')
    label = result['text']
    return label

############################## MAIN ###################################
if __name__ == '__main__':
    dir, count = sys.argv[1], 0
    for file in os.listdir(dir):
        file_name = os.path.join(dir, file)
        if not os.path.isfile(file_name) or not file_name.endswith('.json'):
            continue
        with open(file_name, 'rt', encoding='utf-8') as in_file:
            doc = json.load(in_file)
            background = str(doc['background']) if doc['background'] else ''
            assumptions = str(doc['assumptions']) if doc['assumptions'] else ''
            objectives = ' '.join(doc['objectives']) if doc['objectives'] else ''
            relevant_text = background + assumptions + objectives
            try:
                prompts = [keywords_prompt, abstract_prompt, value_prompt, problem_statement_prompt, desired_outcomes_prompt, description_prompt, objectives_prompt, target_prompt, constraint_prompt]
                keys = ['keywords', 'abstract', 'value', 'problem_statement', 'desired_outcomes', 'description', 'objectives', 'target', 'constraints']
                prompts_length = len(prompts)
                for index in range(0, prompts_length):
                    synth_result = {keys[index]: feed_llm(prompts[index], relevant_text)}
                    save_path = 'synth_data/protocols/'
                    os.makedirs('synth_data/protocols/', exist_ok = True)
                    result_file_name = os.path.join(save_path, file[:-4] + '_synth.json')
                    with open(result_file_name, 'a+') as synth_file:
                        json.dump(synth_result, synth_file, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"\n{file_name}")
        count = increase_count(count, '.')
        # break
    print(f"\nProcessed {count} documents.\n")
