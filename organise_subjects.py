import json

def sort_json_keys(file_path):
    # Load the JSON data
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Sort the keys
    sorted_data = {key: data[key] for key in sorted(data.keys())}
    
    # Save the sorted JSON data
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(sorted_data, file, ensure_ascii=False, indent=4)

def filter_cse_subjects(input_file_path, output_file_path):
    # Load the JSON data
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Filter the subjects
    filtered_data = {key: value for key, value in data.items() if value.get('college') == 'College of Science and Engineering'}
    
    # Save the filtered JSON data
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(filtered_data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # Sort the keys in the original JSON file
    sort_json_keys('subjects.json')
    
    # Filter the CSE subjects and save to a new JSON file
    filter_cse_subjects('subjects.json', 'cse_subjects.json')
