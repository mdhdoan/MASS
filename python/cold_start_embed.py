from IPython.display import display
import json
import pandas as pd
import os
import re
import sys

from umap import UMAP
from hdbscan import HDBSCAN
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer

from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired, MaximalMarginalRelevance
from bertopic.vectorizers import ClassTfidfTransformer

from langchain.chains.llm import LLMChain
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.schema import Document

HEADERS = [
    "abstractText"
    # "background"
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
    umap_model = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine', random_state=42)
    # Step 3 - Cluster reduced embeddings
    hdbscan_model = HDBSCAN(min_cluster_size=15, metric='euclidean', cluster_selection_method='eom', prediction_data=True)
    # Step 4 - Tokenize topics
    vectorizer_model = CountVectorizer(stop_words="english", ngram_range=(1, 3), min_df=3)
    # Step 5 - Create topic representation
    ctfidf_model = ClassTfidfTransformer(bm25_weighting=True, reduce_frequent_words=True)
    # Step 6 - (Optional) Fine-tune topic representation
    representation_model = KeyBERTInspired()
    # representation_model = {
    #         "KBI": KeyBERTInspired(top_n_words=30),
    #         "MMR": MaximalMarginalRelevance(top_n_words=30, diversity=.5),
    #     }
    
    # Step 7 - Provide zeroshot list for guidance
    zeroshot_topics = [
        "Physical", "Ecological", "Chemical",
        "Data Collection", "Data Analysis", "Statistical Methods",
        "Population Estimation", "Fish Capture, Handling, and Release", "Biology"
    ]

    # All steps together
    topic_model = BERTopic(
        embedding_model=embedding_model,          # Step 1 - Extract embeddings
        umap_model=umap_model,                    # Step 2 - Reduce dimensionality
        hdbscan_model=hdbscan_model,              # Step 3 - Cluster reduced embeddings
        vectorizer_model=vectorizer_model,        # Step 4 - Tokenize topics
        ctfidf_model=ctfidf_model,                # Step 5 - Extract topic words
        representation_model=representation_model # Step 6 - (Optional) Fine-tune topic represenations
        # zeroshot_topic_list=zeroshot_topics, 
        # zeroshot_min_similarity=.85
    )
    
    topics, probs = topic_model.fit_transform(documents, embeddings)

    all_doc_details = topic_model.get_document_info(documents)
    print(type(all_doc_details))
    display(all_doc_details)
    all_doc_details.to_json('full_details.json', orient = 'records', lines=True)
    
    # System prompt describes information given to all conversations
    prompt_template = """
    You are a helpful, respectful and honest assistant for labeling topics.

    I have a topic that contains the following documents delimited by triple backquotes (```). 
    ```{documents}```
    
    The topic is described by the following keywords delimited by triple backquotes (```):
    ```{keywords}```

    Consider a topic label from {zeroshot_topics} before creating a new label
    Return ONLY a the topic label, which should not contain more than 5 words.
    If your answer has any code in it, generate again. 
    If the amount of words in your answer is more than 5, generate again.
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
            result = llm_chain.invoke({'documents': docs, 'keywords': keywords, 'zeroshot_topics': zeroshot_topics})
            label = result['text']
            print(f"[{i}] --- {topic_model.topic_labels_[i]} --- {label}")
            label_dict[i] = label
    
    topic_model.set_topic_labels(label_dict)

    topic_model.save(
        "model/data/method", 
        serialization="pytorch", save_ctfidf=True, save_embedding_model="sentence-transformers/all-MiniLM-L6-v2"
    )
    
    count = 0
    for file in os.listdir(in_path):
        file_name = os.path.join(in_path, file)
        # print('try to find file')
        if not os.path.isfile(file_name) or not file_name.endswith('.json'):
            print('file not found: ', file_name)
            continue
        with open(file_name, 'rt', encoding='utf-8') as in_file:
            doc = json.load(in_file)
            try:
                for k in HEADERS:
                    if doc[k]:
                        text_data = doc[k]
                embed_data = embedding_model.encode(text_data)
                # print('embed extract success')
                doc['vector'] = embed_data.tolist()
                # print(type(doc['vector']))
                # print('doc update: ', doc)
                save_path = 'embed/' + sys.argv[1]
                os.makedirs(save_path, exist_ok = True)
                # print('path made success', save_path)
                # json_data = json.dump(doc, indent=2)
                # print('json dump success')
                # file = re.sub(r'[^a-zA-Z0-9]', '', file)
                new_file_name = os.path.join(save_path, 'Embedded_' + file)
                # print('path join success: ', new_file_name)
                for field, text in doc.items():
                    doc[field] = re.sub(r'[^a-zA-Z0-9]', '', text)
                with open(new_file_name, 'w+', encoding= 'utf-32') as json_file:
                    # print('file created success: ', new_file_name)
                    json.dump(doc, json_file, ensure_ascii=False, indent=2)
                    # print('file write success')
                count = increase_count(count, '.')
            except Exception as e:
                print(f"\nHit Exception with {file}, {e}")
            # break
            
    print(f"\nAdded embedding to {count} documents.\n")    

    # for embed in embeddings:
    #     print(embed)
    #     break