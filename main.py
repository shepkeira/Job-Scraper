import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import urllib
from urllib.request import Request, urlopen
import json
#from scraper import IndeedScraper
#from urllib import request.urlopen

def getdata(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as httpErr:
        print(f'Http error occurred: {httpErr}')
        return None
    except Exception as err:
        print(f'A generic error occurred: {err}')
        return None
    else:
        return response.content

def html_code(url):
    htmldata = getdata(url)
    soup = BeautifulSoup(htmldata, 'html.parser')
    return soup

def job_data(soup):
    data_str = ""
    for item in soup.find_all("a", class_="jobtitle turnstileLink"):
        data_str = data_str + item.get_text()
    result_1 = data_str.split("\n")
    return(result_1)

def company_data(soup):
    data_str = ""
    result = ""
    for item in soup.find_all("div", class_="sjcl"):
        data_str = data_str + itme.get_text()
    result_1 = data_str.split("\n")

    res = []
    for i in range(1, len(result_1)):
        if len(result_1[i]) > 1:
            res.append(result_1[i])
    return res

def extract_location(result):
    return_array = []
    x = result.find_all('span', {'class': 'location'})
    for b in result.find_all('span', {'class': 'location'}):
        location = b.text
        return_array.append(location)
        #dflocation.loc[len(dflocation)] = [location]    
    return return_array

def extract_company(result):        
    for i in result.find_all('span', {'class':'company'}):
        company = i.text
        dfcompany.loc[len(dfcompany)] = [company]   

def extract_job_title(result):
    for a in result.find_all('a', {'data-tn-element':'jobTitle'}):
        job_title = a.text
        dfjob_title.loc[len(dfjob_title)] = [job_title]

def extract_salary(result):
    for entry in result.find_all('td', {'class' : 'snip'}):
        try:
            salary = entry.find('nobr').text
            dfsalary.loc[len(dfsalary)] = [salary]  
        except:
            salary = 'NA'
            dfsalary.loc[len(dfsalary)] = [salary]    

if __name__ == "__main__":

    #url = 'https://fzqy8f.deta.dev/api/salary/?job_title=Software+Engineer&location=San+Francisco&salary_type=YEARLY'
    # https://www.indeed.com/jobs?q=data%20scientist%20%2420%2C000&l=New%20York&start=10&vjk=f373de5a794c1da2
    #URL = "http://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l=New+York"
    #https://www.indeed.com/jobs?q=data%20scientist%20&l=New%20York&vjk=4c8333ce1a6bc841
    URL = 'https://ca.indeed.com/jobs?q=data+science+junior&l=British+Columbia'
    data_collected = []
    job_posts_desired = 100
    job_posts_per_page = 10
    pages_desired = round(job_posts_desired /job_posts_per_page)
    for i in range(0, pages_desired):
        extension = ""
        if i != 0:
            extension = "&start=" + str(i * 10)
        url = URL + extension
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        web_page = urlopen(req).read()
        soup = BeautifulSoup(web_page, 'html.parser')
        #print(soup)

        job_posts = []
        x = soup.find_all('table', attrs={'class': 'jobCard_mainContent big6_visualChanges'}) #jobCard_mainContent big6_visualChanges #job_seen_beacon
        y = soup.find_all('div', attrs={'class': 'job_seen_beacon'})
        a = soup.find_all('a', attrs={'class': 'result'})
        for div in a:
            job = dict()
            job['link'] = 'https://www.indeed.com' + div.attrs['href']

            for h2 in div.findAll('h2', attrs={'class': 'jobTitle'}):
                job['title'] = h2.string
            for company_div in div.findAll('div', attrs={'class': 'company_location'}):
                for company_name in company_div.findAll('span', attrs={'class': 'companyName'}):
                    job['company'] = company_name.string
                for company_location in company_div.findAll('div', attrs={'class': 'compnayLocation'}):
                    job['location'] = company_location.string
            for summary in div.findAll('div', attrs={'class': 'job-snippet'}):
                job['summary'] = str(summary)
            job_posts.append(job)
        data_collected = data_collected + job_posts
    print(len(data_collected))

import csv 
import os
here = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(here, "results.txt")
with open(file_path, 'w') as f:
    for line in data_collected:
        f.write(json.dumps(line))
