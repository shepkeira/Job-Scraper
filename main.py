from jobscrapper import scrapweb, query_for_last_id
from datbase import full_database_backup, sql_connection, load_database_from_folder, empty_table
from process_jobs import process
from top_two import top_two_skill_before_clustering, clustering_dist, top_two_skill_after_clustering
from skill_clustering import cluster, calculate_dendograms
from hierarchical_clustering import cluster_skills
import sqlite3

JOBS = [
    {'URL': 'https://ca.indeed.com/jobs?q=software%20engineer&l=canada&sort=date', 'job_title': 'software_engineer'},
    {'URL': 'https://ca.indeed.com/jobs?q=cashier&l=canada&sort=date', 'job_title': 'cashier'},
]

BEFORE_CLUTERING_SKILLS = {
    'software_engineer': [],
    'cashier': []
}

AFTER_CLUTERING_SKILLS = {
    'software_engineer': [],
    'cashier': []
}

# print the results without doing any new calculations
def print_results():
    try:
        load_database_from_folder()
    except sqlite3.OperationalError as e:
        print("Tables were created before")
    for job in JOBS:
        job_title = job['job_title']
        print("Starting on " + job_title)
        print("Before clustering")
        skills = top_two_skill_before_clustering(job_title)
        clustering_dist(skills)
        BEFORE_CLUTERING_SKILLS[job_title] = BEFORE_CLUTERING_SKILLS[job_title] + skills
        print("After clustering")
        skills = top_two_skill_after_clustering(job_title)
        clustering_dist(skills)
        AFTER_CLUTERING_SKILLS[job_title] = AFTER_CLUTERING_SKILLS[job_title] + skills
    for n in range(0,2):
        print("Comparing The Two Job Titles BEFORE Clustering")
        cashier_skills = BEFORE_CLUTERING_SKILLS['cashier']
        software_engineer_skills = BEFORE_CLUTERING_SKILLS['software_engineer']
        top_skills = [cashier_skills[n], software_engineer_skills[n]]
        print("Skill " + str(n+1))
        clustering_dist(top_skills)
    for n in range(0,2):
        print("Comparing The Two Job Titles AFTER Clustering")
        cashier_skills = AFTER_CLUTERING_SKILLS['cashier']
        software_engineer_skills = AFTER_CLUTERING_SKILLS['software_engineer']
        top_skills = [cashier_skills[n], software_engineer_skills[n]]
        print("Skill " + str(n+1))
        clustering_dist(top_skills)

# redo clustering and print new results
def recluster_and_print_results():
    try:
        load_database_from_folder()
    except sqlite3.OperationalError as e:
        print("Tables were created before")
    for job in JOBS:
        job_title = job['job_title']
        print("Starting on " + job_title)
        print("Before Clustering")
        skills = top_two_skill_before_clustering(job_title)
        clustering_dist(skills)
        BEFORE_CLUTERING_SKILLS[job_title] = BEFORE_CLUTERING_SKILLS[job_title] + skills

        # Clustering
        conn = sql_connection()
        cluster_skills(conn, job_title)
        
        # results after clustering:
        print("After Clustering")
        skills = top_two_skill_after_clustering(job_title)
        clustering_dist(skills)
        AFTER_CLUTERING_SKILLS[job_title] = AFTER_CLUTERING_SKILLS[job_title] + skills
    for n in range(0,2):
        print("Comparing The Two Job Titles Before Clustering")
        cashier_skills = BEFORE_CLUTERING_SKILLS['cashier']
        software_engineer_skills = BEFORE_CLUTERING_SKILLS['software_engineer']
        top_skills = [cashier_skills[n], software_engineer_skills[n]]
        print("Skill " + str(n+1))
        clustering_dist(top_skills)
    for n in range(0,2):
        print("Comparing The Two Job Titles AFTER Clustering")
        cashier_skills = AFTER_CLUTERING_SKILLS['cashier']
        software_engineer_skills = AFTER_CLUTERING_SKILLS['software_engineer']
        top_skills = [cashier_skills[n], software_engineer_skills[n]]
        print("Skill " + str(n+1))
        clustering_dist(top_skills)

# using exisitng jobs redo processing and all following calculations
def calculate_new_results_no_new_jobs():
    #load database if its not already created
    try:
        load_database_from_folder()
    except sqlite3.OperationalError as e:
        print("Tables were created before")
    finally:
        empty_table("cashier_skill")
        empty_table("cashier_processed_skill")
        empty_table("software_skill")
        empty_table("software_processed_skill")
    for job in JOBS:
        job_title = job['job_title']
        print("Starting on " + job_title)
        # Scrap for jobs
        last_job_id = -1
        # Process jobs for skills
        print("Processing Summaries")
        process(job_title, last_job_id) #15mins
        print("Before Clustering")
        skills = top_two_skill_before_clustering(job_title)
        clustering_dist(skills)
        BEFORE_CLUTERING_SKILLS[job_title] = BEFORE_CLUTERING_SKILLS[job_title] + skills

        # Clustering
        print("Begining Clustering")
        cluster(job_title)
        
        # results after clustering:
        print("After Clustering")
        skills = top_two_skill_after_clustering(job_title)
        clustering_dist(skills)
        AFTER_CLUTERING_SKILLS[job_title] = AFTER_CLUTERING_SKILLS[job_title] + skills
    for n in range(0,2):
        print("Comparing The Two Job Titles Before Clustering")
        cashier_skills = BEFORE_CLUTERING_SKILLS['cashier']
        software_engineer_skills = BEFORE_CLUTERING_SKILLS['software_engineer']
        top_skills = [cashier_skills[n], software_engineer_skills[n]]
        print("Skill " + str(n+1))
        clustering_dist(top_skills)
    for n in range(0,2):
        print("Comparing The Two Job Titles AFTER Clustering")
        cashier_skills = AFTER_CLUTERING_SKILLS['cashier']
        software_engineer_skills = AFTER_CLUTERING_SKILLS['software_engineer']
        top_skills = [cashier_skills[n], software_engineer_skills[n]]
        print("Skill " + str(n+1))
        clustering_dist(top_skills)

# scrap for jobs and run all calcuations on them
def calculate_new_results():
    #load database if its not already created
    try:
        load_database_from_folder()
    except sqlite3.OperationalError as e:
        print("Tables were created before")
    finally:
        empty_table("cashier_skill")
        empty_table("cashier_processed_skill")
        empty_table("software_skill")
        empty_table("software_processed_skill")
    for job in JOBS:
        url = job['URL']
        job_title = job['job_title']
        print("Starting on " + job_title)
        # Scrap for jobs
        last_job_id = query_for_last_id(job_title)
        print("Web Scrapping")
        scrapweb(url, job_title)
        # Process jobs for skills
        print("Processing Summaries")
        process(job_title, last_job_id)
        
        print("Before Clustering")
        skills = top_two_skill_before_clustering(job_title)
        clustering_dist(skills)
        BEFORE_CLUTERING_SKILLS[job_title] = BEFORE_CLUTERING_SKILLS[job_title] + skills

        # Clustering
        print("Begining Clustering")
        cluster(job_title)
        
        # results after clustering:
        print("After Clustering")
        skills = top_two_skill_after_clustering(job_title)
        clustering_dist(skills)
        AFTER_CLUTERING_SKILLS[job_title] = AFTER_CLUTERING_SKILLS[job_title] + skills
    for n in range(0,2):
        print("Comparing The Two Job Titles Before Clustering")
        cashier_skills = BEFORE_CLUTERING_SKILLS['cashier']
        software_engineer_skills = BEFORE_CLUTERING_SKILLS['software_engineer']
        top_skills = [cashier_skills[n], software_engineer_skills[n]]
        print("Skill " + str(n+1))
        clustering_dist(top_skills)
    for n in range(0,2):
        print("Comparing The Two Job Titles AFTER Clustering")
        cashier_skills = AFTER_CLUTERING_SKILLS['cashier']
        software_engineer_skills = AFTER_CLUTERING_SKILLS['software_engineer']
        top_skills = [cashier_skills[n], software_engineer_skills[n]]
        print("Skill " + str(n+1))
        clustering_dist(top_skills)


# if you don't want to see the clustering collect some new jobs and process them before printing the new results
def calculate_new_results_without_clustering():
    #load database if its not already created
    try:
        load_database_from_folder()
    except sqlite3.OperationalError as e:
        print("Tables were created before")
    finally:
        empty_table("cashier_skill")
        empty_table("cashier_processed_skill")
        empty_table("software_skill")
        empty_table("software_processed_skill")
    for job in JOBS:
        url = job['URL']
        job_title = job['job_title']
        print("Starting on " + job_title)
        # Scrap for jobs
        last_job_id = query_for_last_id(job_title)
        print("Web Scrapping")
        scrapweb(url, job_title)
        # Process jobs for skills
        print("Processing Summaries")
        process(job_title, last_job_id)
        
        print("Before Clustering")
        skills = top_two_skill_before_clustering(job_title)
        clustering_dist(skills)
        BEFORE_CLUTERING_SKILLS[job_title] = BEFORE_CLUTERING_SKILLS[job_title] + skills
    for n in range(0,2):
        print("Comparing The Two Job Titles Before Clustering")
        cashier_skills = BEFORE_CLUTERING_SKILLS['cashier']
        software_engineer_skills = BEFORE_CLUTERING_SKILLS['software_engineer']
        top_skills = [cashier_skills[n], software_engineer_skills[n]]
        print("Skill " + str(n+1))
        clustering_dist(top_skills)
