# Job-Scraper

## Libraries needed

To run this code you will need the following libraries. `pip install` should work for all of them, however it may be different for your system. Please test that you can import them before running the code.

```
pip install bs4
pip install requests
pip install pysqlite3 
pip install numpy
pip install --user -U nltk
pip install dictances
```

You will also need to import  the stopwords corpora from nltk. To do so you will have to run the following lines of python, after intalling nltk
```
import nltk
nltk.download('stopwords')
```

## Running the code
### Set Up
To start you will need to create the database for your process.

If you want to start with no data run:
```
from datbase import create_database
create_database()
```

If you would like to start with the exisiting data you will run:
```
from datbase import load_backup
load_backup()
```

### Run the code
To print the results from exisiting data run the following code (this process is pretty fast):
```
from main import print_results
print_results()
```

To create new data (note this process takes many hours to run!):
```
from main import calculate_new_results
calculate_new_results()
```

To recreate the clusters and run again (this process may take a few hours):
```
from main import recluster_and_print_results
recluster_and_print_results()
```

To recalculate the results without clustering (this process will take a few hours):
```
from main import calculate_new_results_without_clustering
calculate_new_results_without_clustering()
```

There is verious logging throught the code to keep track of progress

### Other Technologies
As there is much data collected in this project I suggested using a database browser to view it. I used "DB Browser (SQLite)" for this.

## The Code
### The Files
Exploring the codebase? Here is an explanation of some of the code:

backupdatabase.sql contains all current data that can be loaded into the database

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
At this time the code is not able to successfully collect all the requested jobs.
There is a known issue with the sentence tokenization, not successfuly seperating new lines as new sentences.
The part of speech tagging is not always accurate.
The code itself is very slow to run.

## Expected results
### For software_engineer
#### Before clustering                                                                                                        
The top two skills are:
"experience" with: 223
and
"python" with: 96
The distance between these two skills is: 1.0
#### After clustering
The top two skills are:
"experience" with: 3605
and
"job description:" with: 92
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
"experience" with: 435 
and
"ope" with: 75
The distance between these two skills is: 2.414213562373095
### Comparing The Two Job Titles Before Clustering
#### Skill 1
The top two skills are:
"experience" with: 140
and
"experience" with: 223
The distance between these two skills is: 6.0
Comparing The Two Job Titles Before Clustering
#### Skill 2
The top two skills are:
"ope" with: 73
and
"python" with: 96
The distance between these two skills is: 2.0
### Comparing The Two Job Titles AFTER Clustering
#### Skill 1
The top two skills are:
"experience" with: 435
and
"experience" with: 3605 
The distance between these two skills is: 6.0
#### Skill 2
The top two skills are:
"ope" with: 75
and
"job description:" with: 92
The distance between these two skills is: 3.0    