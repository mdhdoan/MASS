import pandas as pd
import transformers
from transformers import pipeline

protocol_df = pd.read_csv('protocols.tsv', sep = '\t', encoding= 'latin')
protocol_tag_data = protocol_df[['title', 'id', 'background', 'objectives', 'tags', 'metric_title', 'metric_category', 'metric_subcategory']]

category_df = pd.read_csv('CATEGORIES-AllCategories.csv')
metrics_df = pd.read_csv('METRICS-AllMetrics.csv')
subject_df = pd.read_csv('SUBJECTS-AllSubjects.csv')

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# golden_data_id_list = [3570, 3542, 3552, 2227, 3366, 3593, 2232, 2271, 3549, 55, 3594]# 3633, 3569, 3446]#, 3274, 88, 89, 90]
# golden_tag_data = pd.DataFrame(columns = ['title', 'id', 'background', 'objectives', 'tags', 'metric_title', 'metric_category', 'metric_subcategory'])

# for protocol_id in golden_data_id_list:
#     # print(protocol_id)
#     for protocol_index, protocol in protocol_tag_data.iterrows():
#         if protocol['id'] == protocol_id:
#             # print(protocol['id'], protocol['background'])
#             golden_tag_data.loc[len(golden_tag_data.index)] = protocol #type: ignore
#             break

# golden_protocol_data = pd.DataFrame(columns = list(protocol_df.columns))
# # display(golden_protocol_data)
# for protocol_id in golden_data_id_list:
#     # print(protocol_id)
#     for protocol_index, protocol in protocol_df.iterrows():
#         if protocol['id'] == protocol_id:
#             # print(protocol['id'], protocol['background'])
#             # print(protocol['id'])
#             golden_protocol_data.loc[len(golden_protocol_data.index)] = protocol #type: ignore
#             # display(golden_protocol_data)
#             break

# golden_protocol_data.to_csv('protocol_silver.tsv', sep = '\t')

subject_tags = subject_df['Subject Name']
i = 0
column_list = ['Text']
for tag in subject_tags:
    column_list.append(tag)

# print(subject_tags[0])

protocol_subject_relevancy_table = pd.DataFrame(columns = column_list)
# print(relevancy_table)
total_protocols = len(protocol_tag_data.index)
while i < total_protocols:
    row_relevancy = []
    tags_and_scores = classifier(protocol_tag_data['background'][i], subject_tags, multi_lable = True)
    # print(tags_and_scores)
    row_relevancy.append(tags_and_scores['sequence']) # type: ignore
    for score in tags_and_scores['scores']:# type: ignore
        row_relevancy.append(score) # type: ignore
    # print(row_relevancy)
    protocol_subject_relevancy_table.loc[len(protocol_subject_relevancy_table.index)] = row_relevancy# type: ignore
    i = i + 1
    print('completed: ', i, ' / ', total_protocols)

category_tags = category_df['Category Name']
column_list = ['Text']
for tag in category_tags:
    column_list.append(tag)

protocol_category_relevancy_table = pd.DataFrame(columns = column_list)
protocol_category_relevancy_table['Text'] = protocol_subject_relevancy_table['Text']

# display(protocol_category_relevancy_table)
# for text in protocol_category_relevancy_table['Text']:
#     for subject in subject_tags:
#         print(protocol_subject_relevancy_table.iloc[text][subject])

total_categories = len(category_df.index) - 1

for pcrt_index, pcrt_row in protocol_category_relevancy_table.iterrows():
    for category_index, category_row in category_df.iterrows():
        category_subject = category_row['Subject']
        subject_score = protocol_subject_relevancy_table.loc[pcrt_index, category_subject] # type: ignore
        # print(subject_score)
        # category_subject_name = category_row['Subject']
        if subject_score < 0.1: 
            protocol_category_relevancy_table.loc[pcrt_index, category_row['Category Name']] = 0 #type: ignore
            print('score too low')
            continue
        else:
            print('score good')
            tags_and_scores = classifier(pcrt_row['Text'], category_row['Category Name'])
            # print(tags_and_scores['scores'])
            protocol_category_relevancy_table.loc[pcrt_index, category_row['Category Name']] = tags_and_scores['scores'][0] # type: ignore
            # print(pcrt_row[category_row['Category Name']])
            # print(protocol_category_relevancy_table.loc[pcrt_index,])
            print('completed: ', category_index, ' / ', total_categories)
    print('completed: ', pcrt_index, ' / ', total_protocols)

protocol_category_relevancy_table.to_csv('protocol_category.tsv', sep = '\t')