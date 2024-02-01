import time 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc2
from math import ceil

class IneedJobAnalytic:
    def __init__(self, search_topic='retail', num_jobs=4):
        self.search_topic = search_topic
        self.num_jobs = num_jobs
        self.driver = None
        self.links = []
        self.num_of_pages = ceil(self.num_jobs / 10)

    def start_driver(self):
        options = uc2.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    def scrape_jobs(self):
        for link in self.links[0]:
            self.driver.get(link)
            time.sleep(2)
            self.handle_popups()
            title = self.get_exist_info('//h1[starts-with(@data-testid, "jobsearch")]')
            company = self.get_exist_info('//div[starts-with(@data-testid, "inlineHeader")]')
            job_type = self.get_exist_info('//div[substring(@data-testid, string-length(@data-testid) - string-length("-tile") +1) = "-tile"]')
            location = self.get_exist_info('//div[substring(@data-testid, string-length(@data-testid) - string-length("companyLocation") +1) = "companyLocation"]')
            self.print_job_info(title, company, job_type, location)

    def create_links(self):
        url_meta = '' if self.num_of_pages < 2 else f'&start={self.num_of_pages * 10}'
        for i in range(self.num_of_pages):
            self.driver.get('https://uk.indeed.com/jobs?q=' + self.search_topic + url_meta)
            jobs = self.driver.find_elements(By.XPATH, '//a[starts-with(@id, "job_")]')
            self.links.append([jobs[j].get_attribute('href') for j in range(min(self.num_jobs, len(jobs)))])

    def handle_popups(self):
        try:
            self.driver.find_element(By.XPATH, '//*[@id="google-Only-Modal"]/div/div[1]/button').click()
            self.driver.find_element(By.XPATH, '//button[starts-with(@id, "onetrust-accept-btn-handl")]').click()
            time.sleep(1)
        except:
            pass
    
    def get_exist_info(self, path):
        try:
            element = self.driver.find_element(By.XPATH, path).text
            return element if element else 'N/A'
        except:
            return 'N/A'

    def print_job_info(self, title, company, job_type, location):
        print('____________________________________________________________________________________________________\n')
        print(f'Job title: {title}\nCompany name: {company}\nJob type: {job_type}\nLocation: {location}')
        print('____________________________________________________________________________________________________\n')

    def close_driver(self):
        if self.driver:
            self.driver.close()


def main():
    scraper = IneedJobAnalytic(search_topic='data', num_jobs=12)
    scraper.start_driver()
    scraper.create_links()
    scraper.scrape_jobs()
    scraper.close_driver()

if __name__=="__main__":
    main()