from jobscrapper import scrapweb, query_for_last_id
from datbase import full_database_backup, sql_connection, load_jobs_backup
from process_jobs import process
from top_two import top_two_skill_before_clustering, clustering_dist, top_two_skill_after_clustering
from skill_clustering import cluster
from hierarchical_clustering import cluster_skills

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



def print_results():
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

def recluster_and_print_results():
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
        full_database_backup()
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

def calculate_new_results():
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
        full_database_backup()
        print("Before Clustering")
        skills = top_two_skill_before_clustering(job_title)
        clustering_dist(skills)
        BEFORE_CLUTERING_SKILLS[job_title] = BEFORE_CLUTERING_SKILLS[job_title] + skills

        # Clustering
        print("Begining Clustering")
        cluster(job_title)
        full_database_backup()
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

#############################################################
def calculate_new_results_no_new_jobs():
    # load_jobs_backup()
    for job in JOBS:
        job_title = job['job_title']
        print("Starting on " + job_title)
        # Scrap for jobs
        last_job_id = -1 # we are not collecting new jobs
        # Process jobs for skills
        print("Processing Summaries")
        #process(job_title, last_job_id) #15mins
        # full_database_backup()
        print("Before Clustering")
        skills = top_two_skill_before_clustering(job_title)
        clustering_dist(skills)
        BEFORE_CLUTERING_SKILLS[job_title] = BEFORE_CLUTERING_SKILLS[job_title] + skills

        # Clustering
        print("Begining Clustering")
        cluster(job_title)
        full_database_backup()
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

def calculate_new_results_without_clustering():
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
        full_database_backup()
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

# calculate_new_results_no_new_jobs()