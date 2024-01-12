from bs4 import BeautifulSoup
import json


def main():
    file_path = 'Subject Search.html'
    try:
        file_contents = read_file(file_path)
        subject_data = parse_subject_data(file_contents)
        write_to_json(subject_data, 'subject.json')
    except Exception as e:
        print(f"An error occurred: {e}")


def read_file(file_path):
    """Read and return the contents of a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def parse_subject_data(file_contents):
    """Parse key subject data."""
    page = BeautifulSoup(file_contents, 'html.parser')
    return {
        'code': extract_subject_code(page),  # EE2201
        'full_name': extract_full_name(page),  # Circuit Theory
        'prerequisites': extract_prerequisites(page),  # EG1012 and MA2000. Allow concurrent enrolment for MA2000.
        'description': extract_description(page),
        # AC circuit theorems and network analysis. Sinusoids and phasors. Frequency response...
        'learning_outcomes': extract_learning_outcomes(page),
        # to demonstrate competence in the application of available techniques including mesh and nodal analysis; circuit
        'assessment': extract_assessment(page)
    }


def extract_subject_code(page):
    """Extracts and returns subject code string from html page"""
    element = page.find('h2')
    return element.get_text(strip=True).split(" - ")[0] if element else None


def extract_full_name(page):
    """Extracts and returns subjects name string from html page"""
    element = page.find('h2')
    return element.get_text(strip=True).split(" - ")[1] if element else None


def extract_prerequisites(page):
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


def extract_description(page):
    """Extracts and returns subjects description string from html page"""
    element = page.find('h3', string='Subject Description')
    return clean_text(element.find_next_sibling('ul').get_text(strip=True)) if element else None


def extract_learning_outcomes(page):
    """Extracts and returns subjects learning outcomes string from html page"""
    element = page.find('h3', string='Learning Outcomes')
    return clean_text(element.find_next_sibling('ul').get_text(strip=True)) if element else None


def extract_assessment(page):
    """Extracts and returns nested list of dictionaries containing assesment title and weighting for each assesment peicefrom html page"""
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


def clean_text(text):
    """Clean up text"""
    return ' '.join(text.split())


def write_to_json(data, filename):
    """Write data to a JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
