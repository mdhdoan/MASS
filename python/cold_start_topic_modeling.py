from IPython.display import display
import json
import pandas as pd
import os
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
    "abstractText"
]

def increase_count(count, character):
    count += 1
    print(character, end="", flush=True)
    return count

def create_prompt(format_instructions):
    QA_TEMPLATE = """
        I have a topic that contains the following documents delimited by triple backquotes (```). They could not be in English. The data also include French
        ```{documents}```
        
        The topic is described by the following keywords delimited by triple backquotes (```):
        ```{keywords}```

        Do not provide further information besides the topic label, which should not contain more than 5 words.
        Do not include codes in your answer
        I want something look like these: 
        "Streamflow Measurement in Streams"
        "Wetland Habitat and Waterfowl Management"
        Answer: {format_instructions}
    """
    #Verify your answer, and if the result list has more than 2 items, then Value has multiple parts. Treat them all as one value only, and ignore the number in brackets in them. Retry to shorten it to format above.
    return PromptTemplate(
        input_variables=["documents", "keywords"], 
        partial_variables={"format_instructions": format_instructions}, 
        template=QA_TEMPLATE)

if __name__ == '__main__':
    in_path, documents, count = sys.argv[1], [], 0
    for file in os.listdir(in_path):
        file_name = os.path.join(in_path, file)
        if not os.path.isfile(file_name) or not file_name.endswith('.json'):
            continue
            
        with open(file_name, 'rt', encoding='utf-8') as in_file:
            doc = json.load(in_file)
            # print(doc)
            try:
                # print('value is:', value[0])
                documents.append('\n'.join([doc[k] for k in HEADERS if doc[k]]))
            except Exception as e:
                print(f"\n{file_name}")
            # break
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
    vectorizer_model = CountVectorizer(stop_words="english", ngram_range=(1, 3), min_df=3)

    # Step 5 - Create topic representation
    ctfidf_model = ClassTfidfTransformer(bm25_weighting=True, reduce_frequent_words=True)

    # Step 6 - (Optional) Fine-tune topic representations with 
    # a `bertopic.representation` model
    representation_model = KeyBERTInspired()
    

    # All steps together
    topic_model = BERTopic(
        embedding_model=embedding_model,            # Step 1 - Extract embeddings
        umap_model=umap_model,                      # Step 2 - Reduce dimensionality
        hdbscan_model=hdbscan_model,                # Step 3 - Cluster reduced embeddings
        vectorizer_model=vectorizer_model,          # Step 4 - Tokenize topics
        ctfidf_model=ctfidf_model,                  # Step 5 - Extract topic words
        representation_model=representation_model,  # Step 6 - (Optional) Fine-tune topic representations
        top_n_words=10,
        calculate_probabilities=True,
        verbose=True
    )
    
    topics, probs = topic_model.fit_transform(documents, embeddings)

    # System prompt describes information given to all conversations
    prompt_template = """
    I have a topic that contains the following documents delimited by triple backquotes (```). They could not be in English. The data also include French
    ```{documents}```
    
    The topic is described by the following keywords delimited by triple backquotes (```):
    ```{keywords}```

    Do not provide further information besides the topic label, which should not contain more than 5 words.
    Do not include codes in your answer
    I want something look like these: 
    "Streamflow Measurement in Streams"
    "Wetland Habitat and Waterfowl Management"
    """

    llm = Ollama(model="llama3.2")
    prompt = PromptTemplate(input_variables=["documents", "keywords"], template=prompt_template)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    
    print(topic_model.get_topic_info())
    label_dict = dict()
    for i in range(-1, len(topic_model.get_topic_info())-1):
        if i == -1:
            label_dict[i] = 'Outlier Topic'
        else:
            keywords = topic_model.topic_labels_[i].split('_')[1:]
            docs = topic_model.representative_docs_[i]
            result = llm_chain.invoke({'documents': docs, 'keywords': keywords})
            label = result['text']
            print(f"[{i}] --- {topic_model.topic_labels_[i]} --- {label}")
            bad_string_list = ['[',']','"','\n']
            for bad_string in bad_string_list:
                label = label.replace(bad_string, '')
            label_dict[i] = label
    
    topic_model.set_topic_labels(label_dict)

    topic_model.save(
        "model/" + sys.argv[1][2:], 
        serialization="pytorch", save_ctfidf=True, save_embedding_model="sentence-transformers/all-MiniLM-L6-v2"
    )
    