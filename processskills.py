import os
import nltk
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from string import punctuation
import json

STOP_WORDS = nltk.corpus.stopwords.words('english')
PUNCTUATION = list(punctuation)

#SKILLS_SECTION = ["What do you bring", "qualifications", "requirements", "responsibilities", "must haves", "nice-to-haves", "What you will do"]

def retrieve_jobs_from_file(file_name):
    here = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(here, file_name)
    with open(file_path, 'r', encoding='utf8') as f:
        jobs = f.readlines()
    return jobs

def get_job_summary(job_str):
    job = json.loads(job_str)
    return job['full_summary']

def pos_tags_for_sentence(tokenized_summary):
    no_punctuation = []
    for token in tokenized_summary:
        if token not in PUNCTUATION:
            no_punctuation.append(token)
    word_types = nltk.pos_tag(no_punctuation)
    return word_types

def clean_sentence_tokens(tokenized_summary):
    cleaned_tokens = []
    for token in tokenized_summary:
        if token not in STOP_WORDS and token not in PUNCTUATION:
            cleaned_tokens.append(token)
    return cleaned_tokens

def stem_tokens(tokenized_summary):
    stemmed_tokens = []
    for token in tokenized_summary:
        stemmed_tokens.append(nltk.stem.PorterStemmer().stem(token))
    return stemmed_tokens

def process_sentence(sentence):
    tokenized_summary = word_tokenize(sentence)
    word_types_for_sentence = pos_tags_for_sentence(tokenized_summary)
    
    cleaned_tokens = clean_sentence_tokens(tokenized_summary)
    stemmed_tokens = stem_tokens(cleaned_tokens)

    return [word_types_for_sentence, ' '.join(stemmed_tokens)]


def process_skills(file_name):
    jobs = retrieve_jobs_from_file(file_name)
    processed_job_descriptions = []
    processed_word_type_sentences = []
    for job_str in jobs:
        summary = get_job_summary(job_str)
        sentences = sent_tokenize(summary)
        processed_sentences = []
        word_type_sentences = []
        for sentence in sentences:
            word_types_for_sentence, stemmed_tokens = process_sentence(sentence)
            processed_sentences.append(stemmed_tokens)
            word_type_sentences.append(word_types_for_sentence)
        processed_job_descriptions.append('\n'.join(processed_sentences))
        processed_word_type_sentences.append(word_type_sentences)
    write_proccessed_job_descritions(processed_job_descriptions)
    
    write_processed_word_type_sentences(processed_word_type_sentences)
    return processed_word_type_sentences

def write_proccessed_job_descritions(processed_job_descriptions):
    here = os.path.dirname(os.path.abspath(__file__))
    write_file_path = os.path.join(here, 'processed_software_engineering.txt')
    with open(write_file_path, 'a', encoding='utf8') as f:
        for descrption in processed_job_descriptions:
            f.write(descrption)
            f.write('\n')

def write_processed_word_type_sentences(processed_word_type_sentences):
    here = os.path.dirname(os.path.abspath(__file__))
    write_file_path_2 = os.path.join(here, 'word_type_software_engineering.txt')
    with open(write_file_path_2, 'a', encoding='utf8') as f:
        for descrption in processed_word_type_sentences:
            for sentence in descrption:
                f.write(str(sentence))
                f.write('\n')
    
        #https://analyticssteps.com/blogs/nltk-python-tutorial-beginners