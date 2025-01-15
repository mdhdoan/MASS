import os
import sys

def remove_spaces_in_filenames(directory):
    try:
        for filename in os.listdir(directory):
            old_path = os.path.join(directory, filename)
            # Skip if not a file
            if not os.path.isfile(old_path):
                continue
            
            new_filename = filename.replace("}{", ",\n")  # Replace spaces with underscores
            new_path = os.path.join(directory, new_filename)
            
            # Rename the file if the name has changed
            if old_path != new_path:
                os.rename(old_path, new_path)
                print(f"Renamed: '{filename}' to '{new_filename}'")
        
        print("All files have been processed.")
    except Exception as e:
        print(f"An error occurred: {e}")

def fix_bad_json(directory):
    try:
        for file in os.listdir(directory):
            file_name = os.path.join(directory, file)
            if not os.path.isfile(file_name) or not file_name.endswith('.json'):
                continue
            with open(file_name, 'r') as file_content:
                content = file_content.read()
                corrected_content = content.replace('}{', ',')
                # print(corrected_content)
            
            # Replace '}{' with '},\n{'
            # corrected_content = content.replace('}{', ',\n')
            
            # Add brackets around the entire content to make it a valid JSON array
            # corrected_content = f"[{corrected_content}]"
            
            with open(file_name, 'w') as output_file:
                output_file.write(corrected_content)
        
            print(f"Corrected JSON saved to: {file_name}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Usage example
directory = sys.argv[1]  # Replace with your directory path
# remove_spaces_in_filenames(directory)
fix_bad_json(directory)