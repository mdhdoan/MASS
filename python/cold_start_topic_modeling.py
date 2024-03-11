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


if __name__ == '__main__':
    in_path, documents, count = sys.argv[1], [], 0
    for file in os.listdir(in_path):
        file_name = os.path.join(in_path, file)
        if not os.path.isfile(file_name) or not file_name.endswith('.json'):
            continue
            
        with open(file_name, 'rt', encoding='utf-8') as in_file:
            doc = json.load(in_file)
            try:
                documents.append('\n'.join([doc[k] for k in HEADERS if doc[k]]))
            except Exception as e:
                print(f"\n{file_name}")
            count = increase_count(count, '.')
    print(f"\nRead {count} documents.\n")

    # Step 1 - Extract embeddings
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = embedding_model.encode(documents, show_progress_bar=True)

    # Step 2 - Reduce dimensionality
    umap_model = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine')

    # Step 3 - Cluster reduced embeddings
    hdbscan_model = HDBSCAN(min_cluster_size=15, metric='euclidean', cluster_selection_method='eom', prediction_data=True)

    # Step 4 - Tokenize topics
    vectorizer_model = CountVectorizer(stop_words="english")

    # Step 5 - Create topic representation
    ctfidf_model = ClassTfidfTransformer()

    # Step 6 - (Optional) Fine-tune topic representations with 
    # a `bertopic.representation` model
    representation_model = KeyBERTInspired()
    
    # All steps together
    topic_model = BERTopic(
        embedding_model=embedding_model,          # Step 1 - Extract embeddings
        umap_model=umap_model,                    # Step 2 - Reduce dimensionality
        hdbscan_model=hdbscan_model,              # Step 3 - Cluster reduced embeddings
        vectorizer_model=vectorizer_model,        # Step 4 - Tokenize topics
        ctfidf_model=ctfidf_model,                # Step 5 - Extract topic words
        representation_model=representation_model # Step 6 - (Optional) Fine-tune topic represenations
    )
    
    topics, probs = topic_model.fit_transform(documents, embeddings)

    labels = ['Anadromous fish telemetry using PIT tags', 'Columbia River Salmonid Ecology and Monitoring', 'eDNA extraction and Purification', 'Fish Age Estimation in Fisheries',
              'Fish Passage Criteria Evaluation', 'Fish Seining Techniqies', 'Fishing: Gill Nets and Tangle Nets in Fisheries','Genetic Population Structure and Heterozygosity Analysis',
              'Riparian Vegetaion monitoring in Watersheds', 'Salmon Research in Columbia River Plume', 'Salmonid Tagging Procedures', 'Streamflow Measurement in Streams',
              'Topographic RBT tools for ArcGIS', 'Vegetaion Estimates: Woody and Non-Woody coverage', 'Wetland Habitat and Waterfowl Management', 'Woody Debris Tallying']

    # System prompt describes information given to all conversations
    prompt_template = """
    You are a helpful, respectful and honest assistant for labeling topics.

    I have a topic that contains the following documents delimited by triple backquotes (```). 
    ```{documents}```
    
    The topic is described by the following keywords delimited by triple backquotes (```):
    ```{keywords}```

    Previous attempt at labeling the work contains these topic labels that I would like to be try before generating new label. 
    The labels are delimtied by triple backquotes (```):
    ```{labels}```

    Return ONLY a the topic label, which should not contain more than 5 words.
    If your answer has any code in it, generate again. 
    If the amount of words in your answer is more than 5, generate again.
    If your answer include a clarification or explanation, only return the topic label
    If the label includes any character such as [ and ] and ' and " remove those characters

    For example, I want something look like these: 
    Streamflow Measurement in Streams
    Wetland Habitat and Waterfowl Management
    """

    llm = Ollama(model="mistral")
    prompt = PromptTemplate(input_variables=["documents", "keywords", "labels"], template=prompt_template)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    
    print(topic_model.get_topic_info())
    label_dict = dict()
    for i in range(-1, len(topic_model.get_topic_info())-1):
        if i == -1:
            label_dict[i] = 'Outlier Topic'
        else:
            keywords = topic_model.topic_labels_[i].split('_')[1:]
            docs = topic_model.representative_docs_[i]
            result = llm_chain.invoke({'documents': docs, 'keywords': keywords, 'labels': labels})
            label = result['text']
            print(f"[{i}] --- {topic_model.topic_labels_[i]} --- {label}")
            bad_string_list = ['[',']','"','\n']
            for bad_string in bad_string_list:
                label = label.replace(bad_string, '')
            label_dict[i] = label
    
    topic_model.set_topic_labels(label_dict)

    topic_model.save(
        "model/data", 
        serialization="pytorch", save_ctfidf=True, save_embedding_model="sentence-transformers/all-MiniLM-L6-v2"
    )
    