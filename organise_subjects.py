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

if __name__ == "__main__":
    sort_json_keys('subjects.json')