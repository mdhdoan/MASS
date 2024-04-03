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

HEADERS = [
    "background",
    "assumptions", 
]

def increase_count(count, character):
    count += 1
    print(character, end="", flush=True)
    return count

def feed_llm(text_content):
    prompt_template = """
    You are a helpful, respectful and succinct assistant for labeling topics.

    I have a text body as seen below:
    {content}

    Keywords
    Include a list of highly relevant keywords relevant to the protocol. These keywords can serve as quick references to the main topics and themes covered. Aiming to limit to 5. Then please fill out the following parts:
    1.  Abstract: The Abstract section provides a comprehensive high-level, non-technical focus overview of the protocol, explaining its necessity and offering a succinct solution. 
    2.	Values, Statements and Outcomes: Values that describe why we are putting money into this, Problem Statement of what problem are they trying to solve, Desired outcomes such as what kind of outcomes are specified or desired from the text body.
    3.	Description: Provide a more technical focus, more detailed description of the text body. Focus and depth into why certain methods, metrics, and indicators are used, if any are mentioned. Also explaining why, mechanics, processes, and specifics. Contains more specific details such as project#, protocols#, etc.
    4.	Objectives: Describe the objective in detail, Summary of Solution Coverage: How much of the problem statement is this objective covering, and Keywords: List specific keywords or specifics related to the objective. 
    5.	Target: Specifies the primary focus or goal of the protocol in a few words.
    6.	Constraints: whatever kind of constraints for the current protocol

    If your answer has any code in it, generate again. 
    """
    llm = Ollama(model="mixtral")
    prompt = PromptTemplate(input_variables=["content"], template=prompt_template)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    result = llm_chain.invoke({'content': text_content})
    print('Mixtral complete')
    label = result['text']
    return label

if __name__ == '__main__':
    dir, count = sys.argv[1], 0
    for file in os.listdir(dir):
        file_name = os.path.join(dir, file)
        if not os.path.isfile(file_name) or not file_name.endswith('.json'):
            continue
        with open(file_name, 'rt', encoding='utf-8') as in_file:
            doc = json.load(in_file)
            relevant_text = str(doc['background']) + str(doc['assumptions'] + ' '.join(doc['objectives']))
            try:
                result = feed_llm(relevant_text)
                with open('synth ' + file_name + '.txt', 'w+') as synth_file:
                    synth_file.write(result)
            except Exception as e:
                print(f"\n{file_name}")
        count = increase_count(count, '.')
        break
    print(f"\nRead {count} documents.\n")
