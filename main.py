from jobscrapper import scrapweb, query_for_last_id
from datbase import full_database_backup
from process_jobs import process
from top_two import top_two_skill_before_clustering, before_clustering_dist
from skill_clustering import cluster
# from clustering import cluster_skills_2, calculate_cosine_matrix_2
# from distances import bhattacharyya_coefficient

JOBS = [
    {'URL': 'https://ca.indeed.com/jobs?q=software%20engineer&l=canada&sort=date', 'job_title': 'software_engineer'},
    # {'URL': 'https://ca.indeed.com/jobs?q=cashier&l=canada&sort=date', 'job_title': 'cashier'},
]

if __name__ == "__main__":
    for job in JOBS:
        url = job['URL']
        job_title = job['job_title']
        print("Starting on " + job_title)
        # Scrap for jobs
        # last_job_id = query_for_last_id(job_title)
        # scrapweb(url, job_title)
        #backup our jobs in our database
        # full_database_backup()
        # Process jobs for skills
        # process(job_title, last_job_id)
        # full_database_backup()
        # skills = top_two_skill_before_clustering(job_title)
        # bhatt_coef = before_clustering_dist(skills)
        full_database_backup()
        # Results before clustering:
        # For software_engineer
        # The top two skills are: 
        # "experience: with: 139
        # "experience with a scripting language (e.g. java, c# or c++)"" with 88
        # The distance between these two skills is: 16.1915082254503
        # For on cashier
        # The top two skills are: 
        # "experience" with 100
        # "experience:sales: 1 year (preferred)customer service: 1 year (preferred)work remotely:no" with 29
        # The distance between these two skills is: 19.383361389586504

        # Clustering
        # cluster(job_title)
        # print(distance)
        #compute the overlap between the skills of the two jobs (e.g., using the Bhattacharyya coefficient)
        #bhattacharyya_coefficient(skill_tfidf_dict_1, skill_tfidf_dict_2)