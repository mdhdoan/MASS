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
    "abstractText"
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

    1.  Create a list of highly relevant keywords relevant to the method. These keywords can serve as quick references to the main topics and themes covered. Aiming to limit to 5.

    Once that is done, continue fill out the following with the available informations: 

    2.  Abstract: The Abstract section provides a comprehensive high-level, non-technical focus overview of the method, explaining its necessity and how it solves it. 
    3.	Description: Provide a more technical focus, closely following the given content in a more detailed description of the text body. Focus indepth into the content and provide explanation where applicable.
    4.	Target: Specifies the primary focus or goal of the method in a few words.
    5.	Constraints: whatever kind of constraints for the current method

    If your answer has any code in it, generate again. 
    """
    llm = Ollama(model="mixtral")
    prompt = PromptTemplate(input_variables=["content"], template=prompt_template)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    # print('Begin Mixtral')
    result = llm_chain.invoke({'content': text_content})
    # print('Mixtral complete')
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
            abstractText = str(doc['abstractText']) if doc['abstractText'] else ''

            # Add the context from protocols, and the objectives related that it's trying to solve. Borrow data from synth of possible
            # Add metric connection from the other files for possible solutions

            relevant_text = abstractText
            try:
                result = feed_llm(relevant_text)
                save_path = 'synth_data/methods/'
                os.makedirs('synth_data/methods/', exist_ok = True)
                result_file_name = os.path.join(save_path, file[:-4] + '_synth.txt')
                with open(result_file_name, 'w+') as synth_file:
                    synth_file.write(result)
            except Exception as e:
                print(f"\n{file_name}")
        count = increase_count(count, '.')
        # break
    print(f"\nProcessed {count} documents.\n")
