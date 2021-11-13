from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import json
import os
import time
from summaryscrapper import RECOUNT_TRY, scrapsummary

RECOUNT_TRY = 25

def scrapweb(URL, file_name):
    here = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(here, file_name)
    job_posts_desired = 10000
    count = 2145
    while count < job_posts_desired:
        extension = ""
        if count != 0:
            extension = "&start=" + str(count)
        print("Starting on Extension: " + extension)
        url = URL + extension
        for i in range(RECOUNT_TRY):
            before_count = count
            try:
                time.sleep(i) #sleep for 1 second
                req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'})
                # req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                job_results = get_job_results(req)
                for job_result in job_results:
                    job_dict = create_job_dict(job_result)
                    write_job(file_path, job_dict)
                    count = count + 1
                if before_count == count:
                    raise EmtpyRequestError("Nothing returned from request")
            except (HTTPError, EmtpyRequestError):
                if i < RECOUNT_TRY - 1:
                    continue
                else:
                    count = count+1
                    job_posts_desired = job_posts_desired+1
                    print("Error In class trying again")
            break

def get_job_results(req):
    web_page = urlopen(req).read()
    soup = BeautifulSoup(web_page, 'html.parser')

    job_results = soup.find_all('a', attrs={'class': 'result'})
    return job_results

def create_job_dict(job_result):
    job_dict = dict()
    job_dict = job_summary(job_result, job_dict)
    job_dict = job_info(job_result, job_dict)
    return job_dict

def write_job(file_path, job_dict):
    with open(file_path, 'a') as f:
        f.write(json.dumps(job_dict))
        f.write('\n')

def job_info(job_result, job_dict):
    for job_title in job_result.findAll('h2', attrs={'class': 'jobTitle'}):
        job_dict['title'] = job_title.string
    for company_div in job_result.findAll('div', attrs={'class': 'company_location'}):
        for company_name in company_div.findAll('span', attrs={'class': 'companyName'}):
            job_dict['company'] = company_name.string
        for company_location in company_div.findAll('div', attrs={'class': 'compnayLocation'}):
            job_dict['location'] = company_location.string
    for summary in job_result.findAll('div', attrs={'class': 'job-snippet'}):
        job_dict['summary'] = str(summary)
    return job_dict

def job_summary(job_result, job_dict):
    job_id = job_result['id'].split("_")[-1]
    job_dict['summary_link'] = 'https://ca.indeed.com/viewjob?viewtype=embedded&jk=' + job_id

    summary_text = scrapsummary(job_dict['summary_link'])

    job_dict['full_summary'] = summary_text

    job_dict['link'] = 'https://ca.indeed.com' + job_result.attrs['href']
    return job_dict

class EmtpyRequestError(Exception):
    pass