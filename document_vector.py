import math
import numpy as np

# input: a dictionary of skills: processed skills 
# output: a list of all the terms in the doucment (no duplicates)
def all_terms(skills_array):
    terms = []
    for processed_skill in skills_array:
        processed_skill = processed_skill.split(" ")
        for word in processed_skill:
            terms.append(word)
    return list(set(terms))

def zero_vector(n):
    return np.zeros((n,1))

# input: list of terms to caluclate dv for; doucmetn to caluclate dv for; documents including doument considered
# output: doucment vector (list)
def document_vector(terms, skill, skills_length, all_freq_matrix):
    d_vector = []
    skill_array = skill.split(" ")
    skill_dict = all_terms_frequency(skill_array)
    for term in terms:
        tfidf = term_frequency_inverse_document_frequency(term, skill_dict, skills_length, all_freq_matrix)
        d_vector.append(tfidf)
    return d_vector

#input: array of document words
#output: dict of terms and freqs.
def all_terms_frequency(skill_array):
    term_freq_dict = {}
    for term in skill_array:
        if term in term_freq_dict:
            term_freq_dict[term] += 1
        else:
            term_freq_dict[term] = 1
    return term_freq_dict

# tfidf(t, d, D) = tf(t,d) * idf(t,D)
# input: string of term; dictionary of document term frequencies; documents in a dictionary
# output: term frequency * inverse_document_freqncy for that term and document
def term_frequency_inverse_document_frequency(term, skill_dict, skill_length, all_freq_matrix):
    tf = term_frequency(term, skill_dict)
    if tf != 0:    # print(type(tf))
        idf = inverse_document_frequency(term, skill_length, all_freq_matrix)
        # print(type(idf))
        return tf*idf
    return tf

#idf(t, D) = log( |D| / df(t,D))
# input: string of term; dictionary of documents
# output: log of (# of docuemnets / documetn_frequency of term); if document_frequency of term is 0, log is log(1)
def inverse_document_frequency(term, number_of_docuemts, all_freq_matrix):
    df = all_freq_matrix[term]
    # df = document_frequency(term, skills)
    if df == 0:
        return math.log(1)
    return math.log(number_of_docuemts/df)

# df(t,D) docuements frequency # of doucments that contain t
# input: string of term to find docuement freq for; dictionary of doucments
# output: number of times that term appears in all documents
def document_frequency(term, skills):
    frequency_of_term = 0
    for _file_name, document in skills.items():
        if term in document:
            frequency_of_term += 1
    return frequency_of_term

# tf(t,d) = frequency of t in d / total number of terms in d
#Input: term to find term frequency for; dictionary of term frequencies
#Output: 0 if term is not in document, or if document_dict is empty; else frequnency of term / # of terms
def term_frequency(term, skills_dict):
    total_number_of_terms = len(skills_dict)
    frequency_of_term = 0
    if term in skills_dict:
        frequency_of_term = skills_dict[term]
    if total_number_of_terms != 0:
        return frequency_of_term/total_number_of_terms
    return 0

def term_frequency_for_skill(skill):
    term_freq = {}
    words = skill.split(" ")
    for word in words:
        if word in term_freq:
            term_freq[word] =+ 1
        else:
            term_freq[word] = 1
    return term_freq