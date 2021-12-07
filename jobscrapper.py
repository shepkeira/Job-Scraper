from bs4 import BeautifulSoup
from urllib.error import HTTPError
from urllib.request import Request, urlopen
import time
from summaryscrapper import scrapsummary
import sqlite3
from sqlite3 import Error

# How many times we retry getting jobs if we get a captcha
RECOUNT_TRY = 25

#table names from job titles
TABLE_NAMES = {
    'software_engineer': {'ids': 'software_id', 'jobs': 'software_job'},
    'cashier': {'ids': 'cashier_id', 'jobs': 'cashier_job'},
}

#connect to the database
def sql_connection():
    try:
        conn = sqlite3.connect('JobScrapper.db')
        return conn
    except Error:
        print(Error)

#get jobs
def scrapweb(URL, job_title):
    #get all the current job_ids from the table
    conn = sql_connection()
    ids = get_ids_from_file(conn, job_title)
    
    #number of jobs we want
    job_posts_desired = 10000
    #initalize start and count at 0
    start = 0
    count = len(ids)
    #we want to count in 10s because there are 10 jobs on each page from the start to the job_posts_desired
    for current_page in range(start, job_posts_desired, 10):
        #if we are not on the first page we need to add an extension
        extension = ""
        if count != 0:
            extension = "&start=" + str(current_page)
        url = URL + extension
        #logging for users to track the progress
        print("Starting on Extension: " + extension)
        #try getting the jobs for recount_try number of times
        for i in range(RECOUNT_TRY):
            #to check to see if we have added new jobs, we need to know how many we had before
            before_count = count
            try:
                time.sleep(i) #sleep for 1 second that way we don't call to many times
                #make request to indeed
                req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'})
                #find job results in request
                job_results = get_job_results(req)
                #interate through jobs
                for job_result in job_results:
                    #from the html get all the details we want, if we already have this job, return FALSE
                    job_dict = create_job_dict(job_result, ids)
                    #if we don't already have this job add it to the tables
                    if job_dict:
                        #write to job table
                        write_job(job_dict, conn, job_title)
                        #write to ids table
                        write_id(job_dict, conn, job_title)
                    #increase our count of jobs collected
                    count = count + 1
                #if we have not collected new jobs
                if before_count == count:
                    raise EmtpyRequestError("Nothing returned from request")
            #if there was a problem: no jobs or request error, retry
            except (HTTPError, EmtpyRequestError):
                if i < RECOUNT_TRY - 1:
                    continue
                else:
                    #if we retry RECOUNT_TRY number of times, skip to the next page
                    count = count+10
                    job_posts_desired = job_posts_desired+10
                    print("Error In class trying again")
                    conn.close() #if there is an error, close the connection
            break
        # move to next page
    #after everything close the connection
    conn.close()

# query table for ids
# return a list of ids
def get_ids_from_file(conn, job_title):
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['ids']
    statement = "SELECT job_id FROM "+ table

    cursor.execute(statement)
    output = cursor.fetchall()
    ids = [ele[0] for ele in output]
    cursor.close()
    return ids

#from the request get the HTML, and find all the job results, and return them
def get_job_results(req):
    web_page = urlopen(req).read()
    soup = BeautifulSoup(web_page, 'html.parser')

    job_results = soup.find_all('a', attrs={'class': 'result'})
    return job_results

#for our job_result and our ids, return the job_dict of the values we want or FALSE if we already have this file
def create_job_dict(job_result, ids):
    job_dict = dict()
    job_dict = job_info(job_result, job_dict)
    job_id = get_job_id(job_dict)
    if job_id not in ids:
        job_dict = job_summary(job_result, job_dict)
        
        return job_dict
    else:
        #logging for the user to see if we have already collected a job
        print("Job Already in File")
        return False

# write our job to the job table
def write_job(job_dict, conn, job_title):
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['jobs']
    insert_record = "INSERT INTO "+ table +" (summary_link, full_summary, link, title, company, summary) VALUES (?,?,?,?,?,?)"
    cursor.execute(insert_record, [job_dict['summary_link'],job_dict['full_summary'],job_dict['link'],job_dict['title'],job_dict['company'],job_dict['summary']])
    conn.commit()
    cursor.close()

# get the job id from the summary_link
def get_job_id(job_dict):
    return str(job_dict['summary_link']).split('=')[2]

#write the id to the ids table
def write_id(job_dict, conn, job_title):
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['ids']
    job_id = get_job_id(job_dict)
    insert_record = "INSERT INTO "+ table +" (job_id) VALUES (?)"
    cursor.execute(insert_record, [job_id])
    conn.commit()
    cursor.close()

#collect our job info: title, company name, location, summary (experp not full summary), and full summary_link
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
    job_id = job_result['id'].split("_")[-1]
    job_dict['summary_link'] = 'https://ca.indeed.com/viewjob?viewtype=embedded&jk=' + job_id
    return job_dict

# get the full job summary from the summary_link
def job_summary(job_result, job_dict):
    summary_text = scrapsummary(job_dict['summary_link'])

    job_dict['full_summary'] = summary_text

    job_dict['link'] = 'https://ca.indeed.com' + job_result.attrs['href']
    return job_dict

def query_for_last_id(job_title):
    conn = sql_connection()
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['jobs']
    statement = "SELECT id FROM " + table + " ORDER BY id DESC LIMIT 1;"
    cursor.execute(statement)
    output = cursor.fetchone()
    cursor.close()
    conn.close()
    return output

# new exception class for empty requests (we get a captcha)
class EmtpyRequestError(Exception):
    pass