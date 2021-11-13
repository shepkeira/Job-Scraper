from json.decoder import JSONDecodeError
from jobscrapper import job_summary, scrapweb
from summaryscrapper import scrapsummary
import os
import json

if __name__ == "__main__":
    file_name = "software_engineer.txt"
    #file_name = "cashier.txt"
    job_ids = []
    final_jobs = {}
    here = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(here, file_name)
    write_file_name = "software_engineer_1.txt"
    write_here = os.path.dirname(os.path.abspath(__file__))
    write_file_path = os.path.join(write_here, write_file_name)
    jobs = []
    with open(file_path, 'r') as f:
        jobs = f.readlines()
    
    for job in jobs:
        try:
            job_result = json.loads(job)
            job_id = str(job_result['summary_link']).split('=')[2]
            #check if we already have it
            if job_id not in job_ids:
                # if no, does this one have a full summary?
                this_job_summary = job_result['full_summary']
                if len(this_job_summary) == 0:
                    # if no, call for one and add it
                    summary_text = scrapsummary(job_result['summary_link'])
                    job_result['full_summary'] = summary_text
                # add the job
                job_ids.append(str(job_id))
                final_jobs[job_id] = job_result
            else:
                # if yes, do we need a full_summary still?
                if len(final_jobs[job_id]['full_summary']) == 0:
                    #if yes, does this have a full summary?
                    this_job_summary = job_result['full_summary']
                    if len(this_job_summary) == 0:
                        #if no, call for one again and add it
                        summary_text = scrapsummary(job_result['summary_link'])
                        final_jobs[job_id]['full_summary'] = summary_text
                        
                    else:
                        #if yes, take this one
                        final_jobs[job_id]['full_summary'] = this_job_summary
                    #if no, move to next one
                else:
                    continue
        except JSONDecodeError:
            print(job)     
    with open(write_file_path, 'a') as f:
        #print(len(final_jobs))
        jobs_json = json.dumps(final_jobs, indent=4)
        f.write(jobs_json)
        
        

