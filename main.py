from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json
import re
import time


PUNCTUATION = '''!()-[]{};:'",<>./?@#$%^&*_~'''
BASE_URL = 'https://apps.jcu.edu.au/subjectsearch/#/subject/2024/'
RESCRAPE_ALL_SUBJECTS = False

def main():
    """Retrieve subject page htmls, parse them, store locally in subjects.json"""    
    parsed_data_path = 'subjects.json'
    subject_codes = read_subject_codes_from_file('subject_codes.txt')
    subject_data = read_json_file(parsed_data_path)
    
    driver = webdriver.Chrome()  # Initialize the WebDriver once

    try:
        for subject_code in subject_codes:
            if not subject_requires_rescraping(subject_code, subject_data):
                print(f'{subject_code} already has new availability information.')
            else:
                try:
                    subject_url = ''.join([BASE_URL, subject_code])
                    start_time = time.time()
                    file_contents = fetch_html_file(subject_url, driver)
                    elapsed_time = time.time() - start_time
                    print(f'Fetched file contents of {subject_code} from {subject_url}, took {elapsed_time:.2f} seconds')

                    parse_start_time = time.time()
                    subject_data = parse_subject_data(subject_data, file_contents)
                    parse_elapsed_time = time.time() - parse_start_time
                    print(f'Parsed file contents of {subject_code}, took {parse_elapsed_time:.2f} seconds')

                    write_start_time = time.time()
                    write_subject_to_json(subject_code, subject_data[subject_code], parsed_data_path)
                    write_elapsed_time = time.time() - write_start_time
                    print(f'Wrote data for {subject_code} to JSON, took {write_elapsed_time:.2f} seconds')
                except:
                    print(f'An error occoured for {subject_code}. Skipping.')

    finally:
        driver.quit()  # Ensure the WebDriver is closed
            



def read_json_file(file_path):
    """Read and return the contents of a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def read_subject_codes_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        subject_codes = file.read().splitlines()
    return subject_codes

def subject_requires_rescraping(subject_code, subject_data):
    """Determine if a subject requires a re-scrape of its data (data not complete or otherwise)"""
    is_subject_present = subject_code in subject_data.keys() # has it already been scraped?
    
    try:
        is_availabilities_present = 'availabilities' in subject_data[subject_code]
        first_availability = subject_data[subject_code]['availabilities'][0]
        is_subject_data_complete = is_subject_present and is_availabilities_present and ('study_period_dates' in first_availability)
    except:  
        is_subject_data_complete = False
        print(f'{subject_code} does not have new availability information.')
    finally:
        subject_requires_rescraping = not is_subject_data_complete or RESCRAPE_ALL_SUBJECTS
        return subject_requires_rescraping

def fetch_html_file(url, driver):
    """Fetch html file from url using an existing WebDriver instance"""
    try:
        driver.get(url)

        # Start timer for total time
        total_start_time = time.time()

        # Wait for the main element to load
        main_load_start_time = time.time()
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.StyledBox-sc-13pk1d4-0.gpfScO"))
        )
        main_load_end_time = time.time()
        print(f"Main element loaded in {main_load_end_time - main_load_start_time:.2f} seconds")

        # Scroll to the bottom to ensure all content is loaded
        scroll_start_time = time.time()
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)  # Reduced from 2 seconds to 1 second
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        scroll_end_time = time.time()
        print(f"Scrolling completed in {scroll_end_time - scroll_start_time:.2f} seconds")

        # Find and click all availability buttons
        button_click_start_time = time.time()
        buttons = driver.find_elements(By.CSS_SELECTOR, "button.StyledButton-sc-323bzc-0.evMQeP")
        for button in buttons:
            try:
                driver.execute_script("arguments[0].scrollIntoView(true);", button)
                time.sleep(0.5)  # Reduced from 1 second to 0.5 seconds
                button.click()
                time.sleep(0.5)  # Reduced from 1 second to 0.5 seconds
            except Exception as e:
                print(f"Error clicking button: {e}")
        button_click_end_time = time.time()
        print(f"Button clicking completed in {button_click_end_time - button_click_start_time:.2f} seconds")

        # Get the page source
        html_content = driver.page_source

        total_end_time = time.time()
        print(f"Total fetch_html_file execution time: {total_end_time - total_start_time:.2f} seconds")

    except Exception as exception:
        print(f"Error in fetching html content: {exception}")
    return html_content



def read_local_html_file(file_path):
    """Read and return the contents of a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def write_subject_to_json(subject_code, subject_data, filename):
    """Write subject data to a JSON file"""

    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)

    data[subject_code] = subject_data

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def parse_subject_data(subject_data, file_contents):
    """Parse key subject data and update the json file accordingly."""
    page = BeautifulSoup(file_contents, 'html.parser')
    code = extract_subject_code(page)
    college = extract_college(page)
    if not college:
        print('College not found')
    elif college != 'College of Science and Engineering':
        print('irrelevant subject alert!')
    prerequisites_string = extract_prerequisite_string(page)
    subject_data[code] = {
        'name': extract_name(page),
        'college': college,
        'prerequisites_string': prerequisites_string,
        'prerequisites_subjects': extract_prerequisite_subjects(prerequisites_string, code),
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


def extract_prerequisite_subjects(string, code):
    """Return list of subjects given an input string"""
    try:
        string = ''.join(char for char in string if char not in PUNCTUATION)
        subjects = set()
        words = string.split()
        for word in words:
            if len(word) == 6 and word[0:1].isupper() and word[2:5].isnumeric():
                subjects.add(word)
        return list(subjects)
    except:
        print(f"No prerequisites found for {code}")
        return []


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
    """Extract the subject availabilities with detailed information."""
    availabilities = []
    availability_divs = page.find_all('div', class_='StyledBox-sc-13pk1d4-0 gQMymQ')
    
    for div in availability_divs:
        button = div.find('button', {'role': 'tab'})
        if button and button.get('aria-expanded') == 'true':
            availability = {}
            availability['availability'] = clean_text(button.get_text(strip=True))
            
            details = div.find('div', {'aria-hidden': 'false'})
            if details:
                table = details.find('table')
                if table:
                    for tr in table.find_all('tr'):
                        th = tr.find('th')
                        td = tr.find('td') or tr.find('th', scope='col')
                        if th and td:
                            key = clean_text(th.get_text(strip=True).replace(':', '')).lower().replace(' ', '_')
                            if key == "lecturer(s)":
                                value = [lecturer.get_text(strip=True) for lecturer in td.find_all('div')]
                            elif key == "coordinator(s)":
                                value = [coordinator.get_text(strip=True) for coordinator in td.find_all('div')]
                            else:
                                value = clean_text(td.get_text(strip=True))
                                if key == "workload_expectations":
                                    value = re.sub(r'(\d+ Hours)', r' \1', value).replace(' - ', ' - ').replace('self-directed', ' self-directed')
                                elif key == "study_period_dates":
                                    value = value.replace('to', ' to ')
                            availability[key] = value
            availabilities.append(availability)
    
    return availabilities




def clean_text(text):
    """Clean up text"""
    return ' '.join(text.split())


if __name__ == "__main__":
    main()
