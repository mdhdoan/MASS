import json
import os
import sys

from umap import UMAP
from hdbscan import HDBSCAN
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import CountVectorizer

from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired
from bertopic.vectorizers import ClassTfidfTransformer

HEADERS = [
    "abstractText"
]

def increase_count(count, character):
    count += 1
    print(character, end="", flush=True)
    return count


if __name__ == '__main__':
    model_name = 'data'
    topic_model = BERTopic.load("model/" + model_name)
    label_dict = {
        0: "Stream Channel Classification and Sampling",
        1: "Water Chemistry and Groundwater Temperature Analysis",
        2: "Estimating egg survival during spawning",
        3: "Salmonid tagging procedures",
        4: "Site Layout: Locating and Marking",
        5: "Electrofishing trout in rivers",
        6: "Macroinvertebrate sampling protocol",
        7: "Salmonid trap efficiency methods",
        8: "Genetic population structure and heterozygosity",
        9: "Salmonid Redd Detection Efficiency",
        10: "Floodplain Vegetation Restoration",
        11: "Hydroacoustic methods for fish population assessment",
        12: "Fisheries sampling techniques",
        13: "Fishing: Gillnet Use in Fisheries",
        14: "Columbia River Basin Salmonid Ecology (ESA and Water Quality)",
        15: "Streamflow Measurement in Streams",
        16: "eDNA Extraction and Purification",
        17: "Wetlands Wildlife Habitat Management",
        18: "Vegetation Cover Estimation",
        19: "Woody Debris Tallying: Diameter and Length Classes",
        20: "RBT toolkit for river channel analysis (ArcGIS)",
        21: "Salmon Research in Columbia River Plume",
        22: "Fish Passage Criteria Evaluation",
        23: "Stream habitat assessment through thalweg profiling",
        24: "Fish Seining Techniques",
        25: "Riparian Vegetation Monitoring in Watersheds",
        26: "Anadromous fish telemetry using PIT tags",
        27: "Habitat Statistics for Fish Projects (EPA)"
    }
    topic_model.set_topic_labels(label_dict)

    in_path, documents, count = sys.argv[1], [], 0
    errorfile = ''
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

    sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = sentence_model.encode(documents, show_progress_bar=True)

    viz_topics = topic_model.visualize_topics(top_n_topics=28)
    viz_topics.show()
    viz_topics.write_html("viz/" + model_name + '-topics.html')
    
    # viz_heatmap = topic_model.visualize_heatmap()
    viz_heatmap = topic_model.visualize_heatmap(custom_labels=True)
    viz_heatmap.show()
    viz_heatmap.write_html("viz/" + model_name + '-heatmap.html')

    viz_words = topic_model.visualize_barchart(top_n_topics=28)
    # viz_words = topic_model.visualize_barchart(top_n_topics=20, custom_labels=True)
    viz_words.show()
    viz_words.write_html("viz/" + model_name + '-words.html')

    # # Run the visualization with the original embeddings
    topic_model.visualize_documents(documents, embeddings=embeddings)

    # Reduce dimensionality of embeddings, this step is optional but much faster to perform iteratively:
    reduced_embeddings = UMAP(n_neighbors=10, n_components=2, min_dist=0.0, metric='cosine').fit_transform(embeddings)
    viz_docs = topic_model.visualize_documents(documents, reduced_embeddings=reduced_embeddings, width=2048, height=1152, custom_labels=True)
    viz_docs.show()
    viz_docs.write_html("viz/" + model_name + '-docs.html')
    
    hierarchical_topics = topic_model.hierarchical_topics(documents)
    viz_hie_tops = topic_model.visualize_hierarchy(hierarchical_topics=hierarchical_topics, custom_labels=True)
    viz_hie_tops.show()
    viz_hie_tops.write_html("viz/" + model_name + '-hierarchy.html')
    