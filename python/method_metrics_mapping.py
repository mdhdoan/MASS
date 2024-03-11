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

HEADERS = [
    "m1.textbody"
]

def increase_count(count, character):
    count += 1
    print(character, end="", flush=True)
    return count


if __name__ == '__main__':
    file_name = sys.argv[1]
    with open(file_name, 'r') as in_file:
        metric_matching_data = json.load(in_file[0])
        print(metric_matching_data)

    # prompt_template = """
    # You are a helpful, respectful and honest assistant for labeling topics.

    # I have a topic that contains the following documents delimited by triple backquotes (```). 
    # ```{documents}```
    
    # The topic is described by the following keywords delimited by triple backquotes (```):
    # ```{keywords}```

    # Previous attempt at labeling the work contains these topic labels that I would like to be try before generating new label. 
    # The labels are delimtied by triple backquotes (```):
    # ```{labels}```

    # Return ONLY a the topic label, which should not contain more than 5 words.
    # If your answer has any code in it, generate again. 
    # If the amount of words in your answer is more than 5, generate again.
    # If your answer include a clarification or explanation, only return the topic label
    # If the label includes any character such as [ and ] and ' and " remove those characters

    # For example, I want something look like these: 
    # Streamflow Measurement in Streams
    # Wetland Habitat and Waterfowl Management
    # """

    # llm = Ollama(model="mistral")
    # prompt = PromptTemplate(input_variables=["documents", "keywords", "labels"], template=prompt_template)
    # llm_chain = LLMChain(llm=llm, prompt=prompt)
