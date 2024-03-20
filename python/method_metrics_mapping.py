import csv
import json
import numpy
import os
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
    metric_matching_data = {}
    metric_to_consider = ''
    method_data = []

    with open(file_name, 'r', encoding = 'utf-8-sig') as in_file:
        metric_matching_data = csv.DictReader(in_file)
        for row in metric_matching_data:
            metric_to_consider = row['Metric']
            method_data.append({row['Title']: row['Textbody']})
    metric_to_consider = metric_matching_data
    # print(method_data)

    # # Step 1 - Extract embeddings
    # embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    # embeddings = embedding_model.encode(method_data, show_progress_bar=True)

    # # Step 2 - Reduce dimensionality
    # umap_model = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine')

    # # Step 3 - Cluster reduced embeddings
    # hdbscan_model = HDBSCAN(min_cluster_size=15, metric='euclidean', cluster_selection_method='eom', prediction_data=True)

    # # Step 4 - Tokenize topics
    # vectorizer_model = CountVectorizer(stop_words="english")

    # # Step 5 - Create topic representation
    # ctfidf_model = ClassTfidfTransformer()

    # # Step 6 - (Optional) Fine-tune topic representations with 
    # # a `bertopic.representation` model
    # representation_model = KeyBERTInspired()

    # # All steps together
    # topic_model = BERTopic(
    #     embedding_model=embedding_model,          # Step 1 - Extract embeddings
    #     umap_model=umap_model,                    # Step 2 - Reduce dimensionality
    #     hdbscan_model=hdbscan_model,              # Step 3 - Cluster reduced embeddings
    #     vectorizer_model=vectorizer_model,        # Step 4 - Tokenize topics
    #     ctfidf_model=ctfidf_model,                # Step 5 - Extract topic words
    #     representation_model=representation_model # Step 6 - (Optional) Fine-tune topic represenations
    # )

    prompt_template = """
    You are a helpful, respectful and honest assistant for labeling topics.

    I have a list of title that contains the following text bodies in a list and stored as a dictionary (JSON format): 
    {method_data}
    
    The metric to consider is:
    {metric_to_consider}

    From the given list of title and context from the following text bodies, please return the most matching in terms of metric, and only the metric
    """

    llm = Ollama(model="mistral")
    prompt = PromptTemplate(input_variables=["method_data", "metric_to_consider"], template=prompt_template)
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    result = llm_chain.invoke({'method_data': method_data, 'metric_to_consider': metric_to_consider})
    matching_title = result['text']
    print(matching_title)
