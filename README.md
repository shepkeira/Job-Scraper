# Job-Scraper

## Libraries needed

To run this code you will need the following libraries. `pip install` should work for all of them, however it may be different for your system. Please test that you can import them in a python console/script before running the code.

```
pip install bs4
pip install requests
pip install pysqlite3 
pip install numpy
pip install --user -U nltk
pip install dictances
pip install -U scikit-learn
pip install scipy
```

You will also need to import  the stopwords corpora from nltk. To do so you will have to run the following lines of python, after intalling nltk
```{python}
import nltk
nltk.download('stopwords')
```

## The Database
The database is seperates data from different job titles into different tables.

### job table
id is an integer user to identify each row
summary_link is a string which contains the URL of the webpage which contains the full_summary for the job, the end of this URL is also the indeed job id for this job
full_summary is a string containing the full summary of the job

* There are other things collected in the jobs table however they did not end up being necessary

### id table
id is an integer user to identify each row
job_id is a string which is the job id from indeed

### skill table
id is an integer user to identify each row
skill is a string of the various skill collected from all the summaries

### processed_skill table
id is an integer user to identify each row
skill is a string of a skill collected from a summary
processed_skill is a string of the skill after processing (no stop words, punctuation, stemmed)

### vectors table
id is an integer user to identify each row
doc_vector is a string containing the document vector for an id
skill_id references a processed_skill id found in the processed_skill table

#### cosine_matrix table
id is an integer user to identify each row
skill_id_i references a processed_skill id found in the processed_skill table
skill_id_j references a processed_skill id found in the processed_skill table
value is a float which is the cosine_similarity between the vectors created by skill_id_i and skill_id_j

### cluster table
id is an integer user to identify each row
skill_id references a processed_skill id found in the processed_skill table
cluster is an integer which refers to which cluster the skill is in. All rows with the same cluster integer are in the same cluster.



## Running the code

### Run the code
To print the results from exisiting data run the following code (this process is pretty fast):
```
from main import print_results
print_results()
```

To recreate the clusters and run again (this process may take an hour or two):
```
from main import recluster_and_print_results
recluster_and_print_results()
```

To do redo all processing and clustering (this process will take a few hours):
```
from main import calculate_new_results_no_new_jobs
calculate_new_results_no_new_jobs()
```

To create new data and recluster (note this process takes a many hours to run!):
```
from main import calculate_new_results
calculate_new_results()
```

To create new data and only display results before clustering (note this process takes a many hours to run!):
```
from main import calculate_new_results_without_clustering
calculate_new_results_without_clustering()
```

```
from datbase import full_database_backup
full_database_backup()
```

There is verious logging throught the code to keep track of progress

### Other Technologies
As there is much data collected in this project I suggested using a database browser to view it. I used "DB Browser (SQLite)" for this.

## The Code
### The Files
Exploring the codebase? Here is an explanation of some of the code:

backupdatabase this folder contains all current data that can be loaded into the database split into files that are below the github file size limit

datbase.py contains code for setting up the database, and connecting to it

document_vector.py this file is used to create the document_vectors from the skills

findskills.py is used to determine if a line of the summary is is a skill or not

hierarchical_clustering.py this code for clustering the skills into groups

JobScrapper.db this is the database file

jobscrapper.py this is the file for scrapping jobs from indeed

main.py this is the file that starts all the code and connects the different files

process_jobs.py this file uses the summaries and tries to find the skills from

skill_clustering.py this file cacluates the cosine_matrix, and calls the docuement_vectors, and hierarchical_clustering files

summaryscrapper.py this file scraps the summaries for the jobs from indeed

top_two.py this file calculates the top two skills and the bhattacharyya_coefficient between them and prints it to the screen

### Buggy Code
At this time the code is not able to successfully collect all the requested jobs for various reasons.
The part of speech tagging is not always accurate.
The code itself is very slow to run.
The code is not great at differentiating skills and non-skills.
There are many response lines in the response and the results can be hard to follow.

## Expected results
### For software_engineer
#### Before clustering                                                                                                        
The top two skills are:
"experience" with: 311
and
"etc." with: 200
The distance between these two skills is: 1.4142135623730951
#### After clustering
The top two skills are:
"experience" with: 9048
and
"redis" with: 108
The distance between these two skills is: 4.414213562373095                                                              
### Starting on cashier
#### Before clustering
The top two skills are:
"experience" with: 140
and
"ope" with: 73
The distance between these two skills is: 2.414213562373095 
#### After clustering
The top two skills are:
"experience" with: 679
and
"ope" with: 76
The distance between these two skills is: 2.414213562373095
### Comparing The Two Job Titles Before Clustering
#### Skill 1
The top two skills are:
"experience" with: 184
and
"experience" with: 311
The distance between these two skills is: 6.0
Comparing The Two Job Titles Before Clustering
#### Skill 2
The top two skills are:
"ope" with: 73
and
" etc." with: 200
The distance between these two skills is: 1.0
### Comparing The Two Job Titles AFTER Clustering
#### Skill 1
The top two skills are:
"experience" with: 679
and
"experience" with: 9048 
The distance between these two skills is: 6.0
#### Skill 2
The top two skills are:
"ope" with: 76
and
" redis" with: 108
The distance between these two skills is: 1.0