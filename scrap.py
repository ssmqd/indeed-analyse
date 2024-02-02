import undetected_chromedriver as uc2 
import csv, time, os
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
from math import ceil

class IneedJobAnalytic:
    def __init__(self, search_topic='retail', num_jobs=4):
        self.search_topic = search_topic # Topic to serach (value selected by user)
        self.num_jobs = int(num_jobs) # Number of jobs to scrape (value selected by user)
        self.driver = None # Initiate the selenium web driver 
        self.links = [] # Create list to handle job links
        self.data_dict = [] # Create dictionary where scraped data will be stored
        self.csv_file = f'{self.search_topic}.csv' # Define the name of csv file based on user search topic 
    
    # Create web driver
    def start_driver(self): 
        options = uc2.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    # Scrape jobs data through previously generated link in create_links() function
    def scrape_jobs(self):
        print('Jobs parsing started ...')
        for link in self.links:
            self.driver.get(link)
            sleep(1)
            self.handle_popups() 
            title = self.get_exist_info('//h1[starts-with(@data-testid, "jobsearch")]')
            company = self.get_exist_info('//div[starts-with(@data-testid, "inlineHeader")]')
            job_type = self.get_exist_info('//div[substring(@data-testid, string-length(@data-testid) - string-length("-tile") +1) = "-tile"]')
            location = self.get_exist_info('//div[substring(@data-testid, string-length(@data-testid) - string-length("companyLocation") +1) = "companyLocation"]')
            self.data_dict.append({'Job title':title, 'Company name':company, 'Job type':job_type, 'Location':location}) # Insert main data into dictionary
            print(f'Job {title} was successfuly inserted!')

    # Insert jobs links into list
    def create_links(self): 
        print(f'Serching for {self.search_topic} jobs')
        num_of_pages = ceil(self.num_jobs / 15) # Determine the number of pages to open based on the total number of jobs to scrape, considering that each page lists 15 jobs
        for i in range(num_of_pages):
            url_meta = '' if i + 1 < 2 else f'&start={i * 10}'
            self.driver.get('https://uk.indeed.com/jobs?q=' + self.search_topic + url_meta)
            jobs = self.driver.find_elements(By.XPATH, '//a[starts-with(@id, "job_")]')
            self.links.extend([jobs[j].get_attribute('href') for j in range(min(self.num_jobs, len(jobs)))])
        print(f'Links list with was successfuly created!')
            

    # Close google and coockie request pop-ups
    def handle_popups(self):
        try:
            self.driver.find_element(By.XPATH, '//*[@id="google-Only-Modal"]/div/div[1]/button').click()
            self.driver.find_element(By.XPATH, '//button[starts-with(@id, "onetrust-accept-btn-handl")]').click()
            sleep(1)
        except:
            pass
    
    # Iterate trough html elements using XPATH menthod to find and return values(.text) of elements
    def get_exist_info(self, path):
        try:
            element = self.driver.find_element(By.XPATH, path).text
            return element if element else 'N/A'
        except:
            return 'N/A'

    # Create csv file from dictionary created in scrape_jobs() function
    def create_csv(self):
        try:
            with open(self.csv_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(self.data_dict[0].keys())
                for i in range(self.num_jobs):
                    writer.writerow(self.data_dict[i].values())
                print(f'Data has been written to {self.csv_file}')
        except Exception as e:
            print(f'Error while creating {self.csv_file} file: {e}')

    # Close driver if exists
    def close_driver(self):
        if self.driver:
            self.driver.close()


def main():
    scraper = IneedJobAnalytic(input('Write topic to serach: '), input('Write number of jobs to output: '))
    scraper.start_driver()
    scraper.create_links()
    scraper.scrape_jobs()
    scraper.create_csv()
    scraper.close_driver()

if __name__=="__main__":
    main()