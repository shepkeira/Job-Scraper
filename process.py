import os
import nltk
from nltk.tokenize import word_tokenize
from string import punctuation
import json
from findskills import find_skills

STOP_WORDS = nltk.corpus.stopwords.words('english')
PUNCTUATION = list(punctuation)

SKILLS_SECTION = ["What do you bring", "qualifications", "requirements", "responsibilities", "must haves", "What you will do"]

def retrieve_jobs_from_file(file_name):
    here = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(here, file_name)
    with open(file_path, 'r', encoding='utf8') as f:
        jobs = f.readlines()
    return jobs

def processfiles(file_name):
    jobs = retrieve_jobs_from_file(file_name)
    for job_str in jobs:
        job = json.loads(job_str)
        summary = job['full_summary']
        indexes = []
        for skill_section in SKILLS_SECTION:
            index = summary.find(skill_section)
            if index >= 0:
                indexes.append(index)
        min_index = 0 if not indexes else min(indexes)
        skills_and_beyond = summary[min_index:]
        process_skills(skills_and_beyond, file_name)

def process_skills(skills, read_file_name):
    file_name_parts = read_file_name.split('.')
    file_name = file_name_parts[0] + "_skills." + file_name_parts[1]
    here = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(here, file_name)
    with open(file_path, 'a', encoding='utf8') as f:
        f.write(skills)
        f.write('\n')

def processskills(read_file_name):
    file_name_parts = read_file_name.split('.')
    file_name = file_name_parts[0] + "_skills." + file_name_parts[1]
    here = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(here, file_name)
    with open(file_path, 'r', encoding='utf8') as f:
        summary_lines = f.readlines()
    skills = []
    not_skills = []
    skills_dict = {}
    for line in summary_lines:
        header = False
        for skill_section in SKILLS_SECTION:
            if skill_section in line:
                header = True
        if not header:
            line_skill = find_skills(line)
            if(line_skill):
                skills = skills + line_skill
            else:
                not_skills.append(line)
    for skill in skills:
        # print("skill:" + str(skill))
        tokenized_skill = word_tokenize(skill)
        cleaned_tokens = []
        for token in tokenized_skill:
            if token not in STOP_WORDS and token not in PUNCTUATION:
                cleaned_tokens.append(token)
        stemmed_tokens = []
        for token in cleaned_tokens:
            stemmed_tokens.append(nltk.stem.PorterStemmer().stem(token))
        processed_skill = ' '.join(stemmed_tokens)
        if processed_skill in skills_dict:
            skills_dict[processed_skill] += 1
        else:
            skills_dict[processed_skill] = 1
    sorted_skills = sorted(skills_dict.items(), key=lambda x:x[1])
    sortdict = dict(sorted_skills, reverse = True)
    sorted_skills = list(sortdict.keys())
    return sorted_skills[:2]
    #for each line
        #remove known lines we don't need SKILLS SECTIONS
        #findskills (noun phrases, verb phrases, you are ___, noun gerund)
        #get ride of the rest
        #save all skills to skills[]
    #remove stop words
    #stem skills

    #group skills
