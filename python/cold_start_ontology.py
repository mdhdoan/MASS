import json
import os
import random
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

random.seed(2023)

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
          'Fish Passage Criteria Evaluation', 'Fish Seining Techniques', 'Fishing: Gill Nets and Tangle Nets in Fisheries', 'Genetic Population Structure and Heterozygosity Analysis', 
          'Riparian Vegetation monitoring in Watersheds', 'Salmon Research in Columbia River Plume', 'Salmonid Tagging Procedures', 'Streamflow Measurement in Streams', 
          'Topographic RBT tools for ArcGIS', 'Vegetation Estimates: Woody and Non-Woody coverage', 'Wetland Habitat and Waterfowl Management', 'Woody Debris Tallying']

    # System prompt describes information given to all conversations
    ontology_prompt_template = """
    You are a respectful and obedient and honest assistant for labeling topics.

    I have a text body that contains the following documents delimited by triple backquotes (```). 
    ```{documents}```

    The topic is described by the following keywords delimited by triple backquotes (```):
    ```{keywords}```

    Previous attempts at labeling the work contains these topic labels that I want you to consider before generating new label. 
    The labels are delimtied by triple backquotes (```):
    ```{labels}```

    Generate for me a short and concise label, and an ontology on the text body.
    """

    ontology_union_prompt_template = """
    You are a respectful and obedient and honest assistant for labeling topics.

    I have many ontologies in this list: 
    ```{ontologies}```

    Generate for me an ontology that is a combination of the entire list.
    """
    # Classify the text body against the list of labels above, then continue below

    # Provide me a label most representative after the label classified, as well as a definition of that label.
    # Also from the list of labels, provide me a list of similar label.

    # The format I am looking for is 'label goes here': Definition | Similar label: [similar label]

    # If there is no similar label, return 'Similar label: []' instead
    # If label is not of that format, try again.
    # If label includes an explanation to why similar lables were chosen, remove the explanation part.
    # If label contains codes, try again and remove them
    # Do not generate anything after the ] character. If generated, remove them

    # For example, the label should look like this:
    # Columbia River Salmonid Ecology and Monitoring - 'Fisheries Management and Monitoring': This label represents the various methods and techniques used in fisheries management and monitoring.
    # Similar labels: ['Fishing: Gill Nets and Tangle Nets in Fisheries', 'Salmonid Tagging Procedures', 'Genetic Population Structure and Heterozygosity Analysis', 'Riparian Vegetation monitoring in Watersheds']
 
    # """

    llm = Ollama(model="llama3.2")
    # prompt = PromptTemplate(input_variables=["documents", "keywords", "labels"], template=ontology_prompt_template)
    # llm_chain = LLMChain(llm=llm, prompt=prompt)
    
    # print(topic_model.get_topic_info())
    # label_dict = dict()
    # # result = llm_chain.invoke({'documents': documents, 'labels': labels})
    # # print(result['text'])
    # for i in range(-1, len(topic_model.get_topic_info())-1):
    #     if i == -1:
    #         label_dict[i] = 'Outlier Topic'
    #     else:
    #         keywords = topic_model.topic_labels_[i].split('_')[1:]
    #         docs = topic_model.representative_docs_[i]
    #         result = llm_chain.invoke({'documents': docs, 'keywords': keywords, 'labels': labels})
    #         label = result['text']
    #         print(f"[{i}] --- {topic_model.topic_labels_[i]} --- {label}")
    #         bad_string_list = ['[',']','"','\n']
    #         for bad_string in bad_string_list:
    #             label = label.replace(bad_string, '')
    #         label_dict[i] = label

    # topic_model.set_topic_labels(label_dict)

    # topic_model.save(
    #     "model/ontology_data", 
    #     serialization="pytorch", save_ctfidf=True, save_embedding_model="sentence-transformers/all-MiniLM-L6-v2"
    # )

    label_file_path = '.\model\ontology_data'
    label_file_name = os.path.join(label_file_path, 'topics.json')
    with open(label_file_name, 'r') as l_file:
        label_data = json.load(l_file)
    label_list = label_data['custom_labels']
    bad_string_list = ['[',']','"','\n']
    label_dict = {}
    dict_length = len(label_list)
    for label in label_list:
        for bad_string in bad_string_list:
            label = label.replace(bad_string, '')
    for i in range (1,dict_length):
        label_dict[str(i)] = label_list[i]     

    union_prompt = PromptTemplate(input_variables=["ontology"], template=ontology_union_prompt_template)
    union_llm_chain = LLMChain(llm=llm, prompt=union_prompt)
    result = union_llm_chain.invoke({'ontologies': label_dict})
    ontology = result['text']

    with open('ontology.json', 'w+') as ontology_file:
        ontology_data = json.dumps(ontology, indent = 2)
        ontology_file.write(ontology_data)
        print('Ontology written to: ontology.json')
    