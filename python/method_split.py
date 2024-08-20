import json
import os
import shutil
import sys

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
            # print(doc['type'], doc['type'] == "Data Analysis/Interpretation")
            # shutil.copy(file_name, './json_data/methods_analysis/')
            try:
                if doc['type'] == "Data Analysis/Interpretation":
                    if os.path.exists(os.path.join('./json_data/methods_analysis/', file_name)):
                        continue
                    else:
                        shutil.copy(file_name, './json_data/methods_analysis/')
                elif doc['type'] == "Data Collection":
                    if os.path.exists(os.path.join('./json_data/methods_collect/', file_name)):
                        continue
                    else:
                        shutil.copy(file_name, './json_data/methods_collect/')
            except Exception as e:
                print(f"\n{file_name}")
            count = increase_count(count, '.')
        # break
    print(f"\nProcessed {count} documents.\n")