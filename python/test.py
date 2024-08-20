import json
import os
import random
import sklearn
import sys

from langchain.chains.llm import LLMChain
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

from umap import UMAP
from hdbscan import HDBSCAN
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer

from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired, MaximalMarginalRelevance
from bertopic.vectorizers import ClassTfidfTransformer

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
    representation_model = {
            "KBI": KeyBERTInspired(top_n_words=30),
            "MMR": MaximalMarginalRelevance(top_n_words=30, diversity=.5),
        }
    
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
    prompt_template = """
    You are a helpful, honest assistant for labeling topics.
    YOU DO NOT EXPLAIN YOUR CHOICES, UNLESS ASKED SPECIFICALLY

    I have the following method: 
    ```{method}```
    
    I have the following structure of methods ontology:
{
  "SITE": {
    "Habitat": {
      "Physical": [
        "Flow",
        "Temperature",
        "Structure",
        "Sediment Composition",
        "Hydraulic Connectivity"
      ],
      "Ecological": [
        "Population",
        "Environmental Disturbance Monitoring",
        "Reproductive Success",
        "Food Webs",
        "Vegetation or Plant Life",
        "Behavioral Studies",
        "Species Interactions",
        "Habitat Fragmentation"
      ],
      "Chemical": [
        "Constituents",
        "Pollutant",
        "Nutrient Levels",
        "Water Quality"
      ]
    }
  },
  "METHODS": {
    "Data Collection": [
      "Sampling Design",
      "Field Methods",
      "Monitoring Techniques",
      "Remote Sensing",
      "Acoustic Monitoring",
      "Survey Methods"
    ],
    "Data Analysis": {
      "Statistical Analysis": [
        "Descriptive Statistics & Confidence Intervals",
        "Spatial Analysis",
        "Temporal Analysis",
        "Generic Analysis": [
          "Regression Models",
          "Multivariate Analysis"
        ]
      ],
      "Population Estimation": [
        "Mark-Recapture"
      ]
    }
  },
  "FISHERIES MANAGEMENT": {
    "Population Estimation": [
      "Mark-Recapture",
      "Survey Methods"
    ],
    "Ecological": [
      "Tagging and Tracking",
      "Non-lethal Sampling",
      "Genetics",
      "Biodiversity",
      "Reproductive Biology",
      "Physiology"
    ]
  }
}


    I want you to provide me the title of the field you think it belongs to. Do not be creative in answering, and provide only the word. 
    If your answer has more words than the title, discard all other information, keep only the title.
    Provide only 1 answer, I do not need alternative. If more than 1 is considered, keep only the first one
    Example of acceptable answer: 
    Field Methods
    Sampling Design

    DO NOT EXPLAIN
    If your answer has any code in it, generate again. 
    """
    llm = Ollama(model="mistral-large")
    prompt = PromptTemplate(input_variables=["method"], template=prompt_template)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    # print(len(documents))
    count = 0
    sorted_methods = {}
    for title, method in documents.items():
        result = llm_chain.invoke({'method': method})
        sorted_methods[title] = result['text']
        count = increase_count(count, '.')
    with open('sorted_methods_collect.json', 'a+') as result_file:
        ontology_data = json.dumps(sorted_methods, indent = 2)
        result_file.write(ontology_data)
    