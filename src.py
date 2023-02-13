import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

COLUMNS = ['title', 'company', 'location', 'link', 'details', 'qualifications', 'benefits', 'description']
filename = 'results.csv'

def create_csv():
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS)

def append_csv(new_row):
    with open(filename, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(new_row)

def get_url(position, location):
    template = 'https://www.indeed.com/jobs?q={}&l={}'
    url = template.format(position, location)
    return url

def collect_job_info(card):
    job_title = card.find_element(By.CLASS_NAME, 'jobTitle')

    job_title_text = job_title.text
    job_company_text = card.find_element(By.CLASS_NAME, 'companyName').text
    job_location_text = card.find_element(By.CLASS_NAME, 'companyLocation').text
    
    job_link = job_title.find_element(By.TAG_NAME, 'a')
    job_link_href = job_link.get_attribute('href')
    driver.execute_script('arguments[0].click();', job_link)
    
    job_description = WebDriverWait(driver, timeout=10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'jobsearch-JobComponent-description')))

    job_details_text = ''
    job_details = job_description.find_elements(By.ID, 'jobDetailsSection')
    if len(job_details) > 0:
        job_details_text = job_details[0].text
    
    job_qualifications_text = ''
    job_qualifications = job_description.find_elements(By.ID, 'qualificationsSection')
    if len(job_qualifications) > 0:
        job_qualifications_text = job_qualifications[0].text

    job_benefits_text = ''
    job_benefits = job_description.find_elements(By.ID, 'benefits')
    if len(job_benefits) > 0:
        job_benefits_text = job_benefits[0].text

    job_description_text = ''
    job_description_element = job_description.find_elements(By.ID, 'jobDescriptionText')
    if len(job_description_element) > 0:
        job_description_text = job_description_element[0].text
    
    return (job_title_text, job_company_text, job_location_text, job_link_href, job_details_text, job_qualifications_text, job_benefits_text, job_description_text)

def scrape_current_page():
    cards = driver.find_elements(By.CLASS_NAME, 'jobCard_mainContent')
    
    for card in cards:
        append_csv(collect_job_info(card))
    
def next_page():
    next_page_button = driver.find_element(By.XPATH, '//*[@data-testid="pagination-page-next"]')
    driver.execute_script('arguments[0].click();', next_page_button)
    
url = get_url('software developer', 'san antonio tx')

driver = webdriver.Firefox()
driver.get(url)

for i in range(3):
    WebDriverWait(driver, timeout=10).until(expected_conditions.text_to_be_present_in_element_attribute((By.XPATH, '//*[@data-testid="pagination-page-current"]'), 'innerHTML', str(i+1)))
    scrape_current_page()
    next_page()

driver.quit()

