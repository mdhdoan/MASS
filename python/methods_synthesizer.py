from IPython.display import display
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

from langchain.chains.llm import LLMChain
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.schema import Document

############################## Variables ###################################

HEADERS = [
    "abstractText"
]

############################## AI PROMPTS ###################################
keywords_prompt = """
    You are a helpful, respectful and succinct assistant for labeling topics.

    I have a text body as seen below:
    {content}

    Create a list of highly relevant keywords relevant to the method. These keywords can serve as quick references to the main topics and themes covered. Your maximum is 10.
    The list shoule be a comma separated list, on one line.
    If your answer has any code in it, generate again. 
    """

abstract_prompt = """
    You are a helpful, respectful and succinct assistant for labeling topics.

    I have a text body as seen below:
    {content}

    Summarize the method in a comprehensive high-level, non-technical focus overview of the method, explaining its necessity and how it solves any issues raised. 
    If your answer has any code in it, generate again. 
    """

description_prompt = """
    You are a helpful, respectful and succinct assistant for labeling topics.

    I have a text body as seen below:
    {content}

    Provide a description that is technical focus, use the terms from the method as closely as possible, closely following the given content in a more detailed description of the text body. Focus indepth into the content and provide explanation where applicable.
    If your answer has any code in it, generate again. 
    """

target_prompt = """
    You are a helpful, respectful and succinct assistant for labeling topics.

    I have a text body as seen below:
    {content}

    Specifies the primary focus or goal of the method within 5 words.

    If your answer has any code in it, generate again. 
    """

constraint_prompt = """
    You are a helpful, respectful and succinct assistant for labeling topics.

    I have a text body as seen below:
    {content}

    Read through it and find what constraints are applicable to the method and where in the method it's stated so. If not, then please provide a detailed explanation why that constraint is there.
    If your answer has any code in it, generate again. 
    """

############################## Custom functions ###################################

def increase_count(count, character):
    count += 1
    print(character, end="", flush=True)
    return count

def feed_llm(prompt, text_content):
    llm = Ollama(model="llama3.2")
    prompt = PromptTemplate(input_variables=["content"], template=prompt)
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    # print('Begin Mixtral')
    result = llm_chain.invoke({'content': text_content})
    # print('Mixtral complete')
    label = result['text']
    return label


############################## MAIN ###################################
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
            # try:
            prompts = [keywords_prompt, abstract_prompt, description_prompt, target_prompt, constraint_prompt]
            keys = ['keywords', 'abstract', 'description', 'target', 'constraints']
            prompts_length = len(prompts)
            save_path = 'synth_data/methods/'
            os.makedirs('synth_data/methods/', exist_ok = True)
            result_file_name = os.path.join(save_path, file[:-4] + '_synth.json')
            synth_dict = {}
            for index in range(0, prompts_length):
                synth_result = {keys[index]: feed_llm(prompts[index], relevant_text)}
                synth_dict[keys[index]] = synth_result
            # except Exception as e:
            #     print(f"\n{file_name}")
            with open(result_file_name, 'w+') as synth_file:
                json.dump(synth_dict, synth_file, ensure_ascii=False, indent=2)
        count = increase_count(count, '.')
        # break
    print(f"\nProcessed {count} documents.\n")
