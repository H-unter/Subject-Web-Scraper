from bs4 import BeautifulSoup
import json

PUNCTUATION = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''


def main():
    html_file_path = 'Subject SearchEE3300.html'
    parsed_data_path = 'subjects.json'
    try:
        subject_data = read_json_file(parsed_data_path)
        file_contents = read_html_file(html_file_path)
        subject_data = parse_subject_data(subject_data, file_contents)
        write_to_json(subject_data, parsed_data_path)
    except Exception as exception:
        print(f"An error occurred parsing subject data: {exception}")


def read_json_file(file_path):
    """Read and return the contents of a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def read_html_file(file_path):
    """Read and return the contents of a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def write_to_json(data, filename):
    """Write data to a JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def parse_subject_data(subject_data, file_contents):
    """Parse key subject data and update the json file accordingly."""
    page = BeautifulSoup(file_contents, 'html.parser')
    college = extract_college(page)
    if not college:
        print('College not found')
    elif college != 'College of Science and Engineering':
        print('irrelevant subject alert!')
    prerequisites_string = extract_prerequisite_string(page)
    subject_data[extract_subject_code(page)] = {
        'name': extract_name(page),
        'college': college,
        'prerequisites_string': prerequisites_string,
        'prerequisites_subjects': extract_prerequisite_subjects(prerequisites_string),
        'description': extract_description(page),
        'learning_outcomes': extract_learning_outcomes(page),
        'availabilities': extract_availabilities(page),
        'assessment': extract_assessment(page)
    }
    return subject_data


def extract_subject_code(page):
    """Extracts and returns subject code string from html page"""
    element = page.find('h2')
    return element.get_text(strip=True).split(" - ")[0] if element else None


def extract_name(page):
    """Extracts and returns subjects name string from html page"""
    element = page.find('h2')
    return element.get_text(strip=True).split(" - ")[1] if element else None


def extract_college(page):
    """Extracts and returns the college who administers the subject"""
    element = page.find('th', string='Administered by:')
    return clean_text(element.find_next_sibling('td').get_text(strip=True)) if element else None


def extract_prerequisite_string(page):
    """Extracts and returns subjects prerequisite list string from html page"""
    # Find all 'th' elements and iterate over them to find one that contains 'Prerequisites'
    for th in page.find_all('th'):
        if 'Prerequisites' in ''.join(th.stripped_strings):
            # The actual prerequisites text is in the next 'td' tag
            prerequisites_td = th.find_next_sibling('td')
            if prerequisites_td:
                return clean_text(prerequisites_td.get_text(strip=True))
            break  # Exit the loop once the correct 'th' is processed
    return None  # Return None if prerequisites are not found


def extract_prerequisite_subjects(string):
    """Return list of subjects given an input string"""
    string = ''.join(char for char in string if char not in PUNCTUATION)
    subjects = set()
    words = string.split()
    for word in words:
        if len(word) == 6 and word[0:1].isupper() and word[2:5].isnumeric():
            subjects.add(word)
    return list(subjects)


def extract_description(page):
    """Extracts and returns subjects description string from html page"""
    element = page.find('h3', string='Subject Description')
    return clean_text(element.find_next_sibling('ul').get_text(strip=True)) if element else None


def extract_learning_outcomes(page):
    """Extracts and returns subjects learning outcomes string from html page"""
    element = page.find('h3', string='Learning Outcomes')
    return clean_text(element.find_next_sibling('ul').get_text(strip=True)) if element else None


def extract_assessment(page):
    """Extracts and returns nested list of dictionaries containing assesment title and weighting for each assesment
    peicefrom html page"""
    element = page.find('h3', string='Subject Assessment')
    if element:
        ul = element.find_next_sibling('ul')
        return [parse_assessment_item(li) for li in ul.find_all('li')] if ul else None
    return None


def parse_assessment_item(li):
    """Extracts assesment item title and weighting"""
    text = li.get_text(strip=True)
    percent = int(''.join(filter(str.isdigit, text.split('(')[-1]))) if '(' in text else None
    return {'title': clean_text(text), 'percent_weighting': percent}


def extract_availabilities(page):
    """Extract the subject availabilities."""
    availability_divs = page.find_all('div', class_='StyledBox-sc-13pk1d4-0 kcFExs')
    return [clean_text(div.get_text(strip=True)) for div in availability_divs]


def clean_text(text):
    """Clean up text"""
    return ' '.join(text.split())


if __name__ == "__main__":
    main()
