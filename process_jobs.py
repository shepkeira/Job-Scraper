import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from string import punctuation
from findskills import find_skills
from datbase import sql_connection

STOP_WORDS = nltk.corpus.stopwords.words('english')
PUNCTUATION = list(punctuation)

HEADERS = [
    "what do you bring",
    "qualifications",
    "requirements",
    "must haves",
    "what you will do",
    "minimum requirements",
    "preferred qualifications",
    "keys to your success",
    "about you",
    "required skills",
    "who you are",
    "education",
    "responsibilities",
    "workplace information",
    "about us",
    "who we are",
    "role location",
    "position description",
    "job duties and responsibilities",
    "company overview",
    "the position",
    "join us",
    "who we are",
    "compensation and benefits",
    "why work with us?",
    "company overview",
    "about the role",
    "about the possition",
    "disclaimer",
    "why?",
    "work setting",
    "education",
    "position summary",
    "security and safety",
    "work conditions and physical capabilities",
    "employment type",
    "type of role",
    "part time",
    "part-time",
    "full-time",
    "full time",
    "physical requirements",
    "note",
    "wage",
    "rate",
    "overview",
    "compensation",
    "position summary",
    "work environment",
    "work performed",
    "company overview",
    "company",
    "product"
]

SKILLS_SECTION = [
    "what do you bring",
    "qualifications",
    "requirements",
    "must haves",
    "what you will do",
    "minimum requirements",
    "preferred qualifications",
    "skills",
    "keys to your success",
    "about you",
    "required skills",
    "who you are",
    "education",
    "experience"
]

OTHER_SECTIONS = [
    "responsibilities",
    "workplace information",
    "about us",
    "who we are",
    "role location",
    "position description",
    "job duties and responsibilities",
    "company overview",
    "the position",
    "join us",
    "who we are",
    "compensation and benefits",
    "why work with us?",
    "company overview",
    "about the role",
    "about the possition",
    "disclaimer",
    "why?",
    "work setting",
    "education",
    "position summary",
    "security and safety",
    "work conditions and physical capabilities",
    "employment type",
    "type of role",
    "part time",
    "part-time",
    "full-time",
    "full time",
    "physical requirements",
    "note",
    "wage",
    "rate",
    "overview",
    "compensation",
    "position summary",
    "work environment",
    "work performed",
    "company overview",
    "company",
    "product"
]

TABLE_NAMES = {
    'software_engineer': {
        'skills': 'software_skill',
        'jobs': 'software_job',
        'processed': 'software_processed_skill'
    },
    'cashier': {
        'skills': 'cashier_skill',
        'jobs': 'cashier_job',
        'processed': 'cashier_processed_skill'
    },
}

#process the jobs to find only the skills sections, then process those skills sections to find only actual skills
def process(job_title, last_job_id):
    #collect only lines from the skills seciton and write them to the table
    print("Processing Files For Skills Sections")
    last_id = processfiles(job_title, last_job_id)
    #process all the skills and put them into a table
    print("Processing Skills Section for Skills")
    processskills(job_title, last_id)

#collect the job summary for all the jobs
def query_for_job_summary(job_title, last_job_id):
    conn = sql_connection()
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['jobs']
    statement = "SELECT full_summary FROM "+ table + " WHERE id > " + last_job_id
    
    cursor.execute(statement)
    output = cursor.fetchall()
    cursor.close()
    conn.close()
    summaries = [ele[0] for ele in output]
    return summaries

#collect all the skills from the table
def query_for_skills(job_title, last_id):
    conn = sql_connection()
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['skills']
    statement = "SELECT skill FROM "+ table + " WHERE id > " + last_id + ";"
    
    cursor.execute(statement)
    output = cursor.fetchall()
    cursor.close()
    conn.close()
    skills = [ele[0] for ele in output]
    return skills

def query_for_last_id(job_title):
    conn = sql_connection()
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['skills']
    statement = "SELECT id FROM " + table + " ORDER BY id DESC LIMIT 1;"
    cursor.execute(statement)
    output = cursor.fetchone()
    cursor.close()
    conn.close()
    return output
    

#process the jobs to find only the skills sections
def processfiles(job_title, last_job_id):
    # determine number of skills before inserting new jobs so we don't process jobs twice
    last_id = query_for_last_id(job_title)
    # collect job summaries
    summaries = query_for_job_summary(job_title, last_job_id)
    #create database connection
    conn = sql_connection()
    #for each summary
    for summary in summaries:
        #only lower case
        summary = summary.lower()
        indexes = []
        # find the start of the skills section
        for skill_section in SKILLS_SECTION:
            index = summary.find(skill_section)
            if index >= 0:
                indexes.append(index)
        # find the first instance of the skills section
        min_index = 0 if not indexes else min(indexes)
        # remove everything before the skills section
        skills_and_beyond = summary[min_index:]
        # find the start of the next section
        for other_titles in OTHER_SECTIONS:
            index = skills_and_beyond.find(other_titles)
            if index >= 0:
                indexes.append(index)
        # select whichever next section comes first
        min_index = None if not indexes else min(indexes)
        # remove everything after the skills section
        only_skills = skills_and_beyond[:min_index]
        # tokenize so every time is a new item in our list
        skill_sentences = sent_tokenize(only_skills)
        # write each line of the skill section to the database
        # each line tends to be one skill
        write_skills_to_table(skill_sentences, job_title, conn)
    #close the connection
    conn.close()
    return last_id

#write our skills to the skills table
def write_skills_to_table(skills, job_title, conn):
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['skills']
    insert_record = "INSERT INTO "+ table +" (skill) VALUES (?)"
    for skill in skills:
        cursor.execute(insert_record, [skill])
        conn.commit()
    cursor.close()

# process each of our skills and write them to a table
def processskills(job_title, last_id):
    # get all the possible skill lines
    possible_skills = query_for_skills(job_title, last_id)
    # initalize some things
    skills = []
    not_skills = [] # this is for viewing purposes only and we don't do anything with it
    final_skills = []
    # for each possible skill
    for line in possible_skills:
        header = False
        # check if this is a header
        for skill_section in HEADERS:
            if skill_section in line:
                header = True
        # if its not a header see if its a skill
        if not header:
            # determine if this line is a skill
            line_skill = find_skills(line)
            if(line_skill):
                # if it is a skill (or many skills) add to our list
                skills = skills + line_skill
            else:
                # we keep track of non skills for observation 
                # to see if we can imporve our find skills method to include more skills that are being missed
                not_skills.append(line)
    # for each line we have determiend is a skill
    for skill in skills:
        # tokenize the skill
        tokenized_skill = word_tokenize(skill)
        # clean the skill of any punctuation or stop words
        cleaned_tokens = []
        for token in tokenized_skill:
            if token not in STOP_WORDS and token not in PUNCTUATION:
                cleaned_tokens.append(token)
        # use the porter stemming algorithm to stem the words in the skill
        stemmed_tokens = []
        for token in cleaned_tokens:
            stemmed_tokens.append(nltk.stem.PorterStemmer().stem(token))
        processed_skill = ' '.join(stemmed_tokens)
        final_skills.append({'skill': skill, 'processed_skill': processed_skill})
    # write all the processed skills to the database
    write_processed_skill_to_table(final_skills, job_title)

# write all processed_skills to the database table
def write_processed_skill_to_table(skills, job_title):
    conn = sql_connection()
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['processed']
    insert_record = "INSERT INTO "+ table +" (skill, processed_skill) VALUES (?, ?)"
    for skill in skills:
        cursor.execute(insert_record, [skill['skill'], skill['processed_skill']])
        conn.commit()
    cursor.close()
    conn.close()
