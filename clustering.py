import math
from tabulate import tabulate
import os
import json
import pandas as pd
import scipy.cluster.hierarchy as shc
from matplotlib import pyplot as plt
import numpy as np
from dictances import cosine, bhattacharyya_coefficient
from sklearn.cluster import KMeans
from hierarchical_clustering import skills_for_largest_clusters

def create_frequency_matrix(processed_skills):
    frequency_matrix = {}
    for skill in processed_skills:
        words = skill.split(" ")
        for word in words:
            if word in frequency_matrix:
                frequency_matrix[word] =+ 1
            else:
                frequency_matrix[word] = 1
    return frequency_matrix

def cluster_skills_2(file_name):
    skills_dict = read_skill_dict(file_name)
    terms = all_terms(skills_dict)
    processed_skills = list(skills_dict.values())
    all_freqency_matrix = create_frequency_matrix(processed_skills)
    skills_vectors = []
    for skill, processed_skill in skills_dict.items():
        skill_vector = document_vector_2(processed_skill)
        # skill_vector = document_vector(terms, processed_skill, skills_dict, all_freqency_matrix)
        skill_vector_dict = {'full_skill': skill, 'skill_vector': skill_vector}
        skills_vectors.append(skill_vector_dict)
        write_skills_vector(file_name, skill_vector_dict)
    # write_skills_vectors(file_name, skills_vectors)

def document_vector_2(skill):
    skill_array = skill.split(" ")
    return all_terms_frequency(skill_array)

# input: a dictionary of skills: processed skills
def cluster_skills(file_name):
    skills_dict = read_skill_dict(file_name)
    terms = all_terms(skills_dict)
    processed_skills = list(skills_dict.values())
    all_freqency_matrix = create_frequency_matrix(processed_skills)
    skills_vectors = []
    for skill, processed_skill in skills_dict.items():
        skill_vector = document_vector(terms, processed_skill, skills_dict, all_freqency_matrix)
        skill_vector_dict = {'full_skill': skill, 'skill_vector': skill_vector}
        skills_vectors.append(skill_vector_dict)
        write_skills_vector(file_name, skill_vector_dict)
    # write_skills_vectors(file_name, skills_vectors)

def calculate_cosine_matrix_2(file_name):
    skills_vectors_dict = read_skills_vector(file_name)
    skills_vectors = []
    skills = []
    for row in skills_vectors_dict:
        skill_vector = row['skill_vector']
        skill = row['full_skill']
        skills_vectors.append(skill_vector)
        skills.append(skill)
    cosine_matrix_n_x_n = cosine_matrix_2(skills_vectors)
    df_matrix = pd.DataFrame(cosine_matrix_n_x_n)
    # smaller_df, columns = remove_all_1_rows(df_matrix)
    # col_skills = []
    # for index in columns:
    #     col_skills.append(skills[index])
    top_skills_indexes = skills_for_largest_clusters(df_matrix, skills)
    if len(top_skills_indexes) >= 2:
        skill_index_1 = top_skills_indexes[0]
        skill_vector_1 = skills_vectors[skill_index_1]
        skill_index_2 = top_skills_indexes[1]
        skill_vector_2 = skills_vectors[skill_index_2]
        distance = bhattacharyya_coefficient(skill_vector_1, skill_vector_2)
    else:
        distance = None
    return distance


    #build_dendrogram_2(smaller_df, col_skills, file_name)

    #build clusters that stop when distance is greater than 1 via dendrogram based on furthers method

def remove_all_1_rows(df):
    columns_to_be_deleted = []
    columns_kept = []
    count = 0
    values = []
    for column_name, column in df.iteritems():
        delete = True
        for item in column:
            if round(item, 2) <= 0.1 and round(item, 2) > 0:
                delete = False
                values.append(item)
        if delete:
            columns_to_be_deleted.append(count)
        else:
            columns_kept.append(count)
        count += 1
    # values = list(set(values))
    # count_dict = {}
    # my_rounded_list = [ round(elem, 2) for elem in values ]
    # for value in my_rounded_list:
    #     value_str = str(value)
    #     if value_str in count_dict:
    #         count_dict[value_str] += 1
    #     else:
    #         count_dict[value_str] = 1
    df.drop(df.columns[columns_to_be_deleted], axis=1, inplace=True)
    df.drop(columns_to_be_deleted, axis=0, inplace=True)
    return [df, columns_kept]

def calculate_cosine_matrix(file_name):
    skills_vectors_dict = read_skills_vector(file_name)
    skills_vectors = []
    skills = []
    for row in skills_vectors_dict:
        skill_vector = row['skill_vector']
        skill = row['full_skill']
        skills_vectors.append(skill_vector)
        skills.append(skill)
    cosine_matrix_n_x_n, skills = cosine_matrix(skills_vectors)
    
    # table = tabulate(skills_vectors)
    # write_matrix_to_file(table, file_name)
    build_dendrogram(cosine_matrix_n_x_n, skills, file_name)
    #cosine matrix

def build_dendrogram_2(df_matrix, skills, file_name):
    shc.dendrogram((shc.linkage(df_matrix, method ='single')), labels=skills, color_threshold=0.8, above_threshold_color="green")
    file_name_parts = file_name.split('.')
    dendogram_file_name = file_name_parts[0] + "_dendogram_closest.png"
    path = os.path.join(os.getcwd(), dendogram_file_name)
    plt.savefig(path)
    shc.dendrogram((shc.linkage(df_matrix, method ='complete')), labels=skills, color_threshold=0.8, above_threshold_color="green")
    file_name_parts = file_name.split('.')
    dendogram_file_name = file_name_parts[0] + "_dendogram_farthest.png"
    path = os.path.join(os.getcwd(), dendogram_file_name)
    plt.savefig(path)
    shc.dendrogram((shc.linkage(df_matrix, method ='centroid')), labels=skills, color_threshold=0.8, above_threshold_color="green")
    file_name_parts = file_name.split('.')
    dendogram_file_name = file_name_parts[0] + "_dendogram_center.png"
    path = os.path.join(os.getcwd(), dendogram_file_name)
    plt.savefig(path)
    # Cluster Based on Cosine Matrix

def build_dendrogram(cosine_matrix_n_x_n, skills, file_name):
    df_matrix = pd.DataFrame(cosine_matrix_n_x_n, columns=skills)
    shc.dendrogram((shc.linkage(df_matrix, method ='single')), labels=skills, color_threshold=0.8, above_threshold_color="green")
    file_name_parts = file_name.split('.')
    dendogram_file_name = file_name_parts[0] + "_dendogram_closest.png"
    path = os.path.join(os.getcwd(), dendogram_file_name)
    plt.savefig(path)
    shc.dendrogram((shc.linkage(df_matrix, method ='complete')), labels=skills, color_threshold=0.8, above_threshold_color="green")
    file_name_parts = file_name.split('.')
    dendogram_file_name = file_name_parts[0] + "_dendogram_farthest.png"
    path = os.path.join(os.getcwd(), dendogram_file_name)
    plt.savefig(path)
    shc.dendrogram((shc.linkage(df_matrix, method ='centroid')), labels=skills, color_threshold=0.8, above_threshold_color="green")
    file_name_parts = file_name.split('.')
    dendogram_file_name = file_name_parts[0] + "_dendogram_center.png"
    path = os.path.join(os.getcwd(), dendogram_file_name)
    plt.savefig(path)
    # Cluster Based on Cosine Matrix
    

def read_skills_vector(file_name):
    file_name_parts = file_name.split('.')
    vector_file_name = file_name_parts[0] + "_skills_vec3." + file_name_parts[1]
    path = os.path.join(os.getcwd(), vector_file_name)
    with open(path, 'r') as f:
        lines = f.readlines()
    skills_vectors = []
    for line in lines:
        skills_vectors.append(json.loads(line))
    return skills_vectors


def write_skills_vector(file_name, skills_vector):
    file_name_parts = file_name.split('.')
    vector_file_name = file_name_parts[0] + "_skills_vec2." + file_name_parts[1]
    path = os.path.join(os.getcwd(), vector_file_name)
    with open(path, 'a') as f:
        f.write(json.dumps(skills_vector))
        f.write('\n')

def write_skills_vectors(file_name, skills_vectors):
    file_name_parts = file_name.split('.')
    vector_file_name = file_name_parts[0] + "_skills_vec." + file_name_parts[1]
    path = os.path.join(os.getcwd(), vector_file_name)
    with open(path, 'w') as f:
        f.write(json.dumps(skills_vectors))

def read_skill_dict(file_name):
    file_name_parts = file_name.split('.')
    skill_dict_file_name = file_name_parts[0] + "_skills_dict.json"
    path = os.path.join(os.getcwd(), skill_dict_file_name)
    with open(path, 'r') as f:
        line = f.read()
    return json.loads(line)

# input: takes in a tabulare table
# output: writes the results to results/cosine_matrix.txt
def write_matrix_to_file(table, file_name):
    file_name_parts = file_name.split('.')
    matrix_file_name = file_name_parts[0] + "_cosine_matrix." + file_name_parts[1]
    path = os.path.join(os.getcwd(), matrix_file_name)
    f = open(path, 'w')
    f.write(table)
    f.close()
    
# input: a list of document vectors and the file names for each document
# output: a matrix and a list of file_names in the order placed in the matrix
def cosine_matrix(skills_vectors):
    matrix = []
    skills = []
    for vector_dict_i in skills_vectors:
        name_i = vector_dict_i['full_skill']
        skill_vector_i = vector_dict_i['skill_vector']
        matrix_row_i = []
        skills.append(name_i)
        for vector_dict_j in skills_vectors:
            _name_j = vector_dict_j['full_skill']
            skill_vector_j = vector_dict_j['skill_vector']
            value_i_j = cosine(skill_vector_i, skill_vector_j) # we don't need all the other values just dict of words and values
            # value_i_j = cosine_similarity(skill_vector_i, skill_vector_j)
            matrix_row_i.append(value_i_j)
        matrix.append(matrix_row_i)
    return [matrix, skills]

# input: a list of document vectors and the file names for each document
# output: a matrix and a list of file_names in the order placed in the matrix
def cosine_matrix_2(skills_vectors):
    matrix = []
    for vector_i in skills_vectors:
        matrix_row_i = []
        for vector_j in skills_vectors:
            value_i_j = cosine(vector_i, vector_j) # we don't need all the other values just dict of words and values
            # value_i_j = cosine_similarity(skill_vector_i, skill_vector_j)
            matrix_row_i.append(value_i_j)
        matrix.append(matrix_row_i)
    return matrix


# cos(theta) = d_1 dot d_2 / vect_mag(d_1) * vect_mag(d_2)
# input: document vector (list) x 2
# output: cosine similarity of vecotrs (num)
def cosine_similarity(skill_vec_1, skill_vec_2):
    dot_prod = dot_product(skill_vec_1, skill_vec_2)
    if not dot_prod and dot_prod != 0:
        print("Document Vecotors are not the same length")
        return False
    vec_1_mag = vector_magnitude(skill_vec_1)
    vec_2_mag = vector_magnitude(skill_vec_2)
    vec_mag_prod = vec_1_mag * vec_2_mag
    if vec_mag_prod == 0:
        return 0
    cosine = dot_prod / vec_mag_prod
    return cosine

# input: a vector of indeterminate length
# output: the magnitude the vector
def vector_magnitude(vector):
    vec_mag_sqared = 0
    for value in vector:
        vec_mag_sqared += value**2
    vec_mag = math.sqrt(vec_mag_sqared)
    return vec_mag

# input: two vecotrs of the same length
# output: dot product of vectors (num)
def dot_product(vec_1, vec_2):
    dot_prod = 0
    length_1 = len(vec_1)
    length_2 = len(vec_2)
    if length_1 != length_2:
        return False
    for i in range(length_1):
        di1 = vec_1[i]
        di2 = vec_2[i]
        dot_prod += di1 * di2
    return dot_prod

# input: a dictionary of skills: processed skills 
# output: a list of all the terms in the doucment (no duplicates)
def all_terms(skills_dict):
    terms = []
    for _skill, processed_skill in skills_dict.items():
        processed_skill = processed_skill.split(" ")
        for word in processed_skill:
            terms.append(word)
    return list(set(terms))

def zero_vector(n):
    return np.zeros((n,1))

# input: list of terms to caluclate dv for; doucmetn to caluclate dv for; documents including doument considered
# output: doucment vector (list)
def document_vector(terms, skill, skills, all_freq_matrix):
    d_vector = []
    skill_array = skill.split(" ")
    skill_dict = all_terms_frequency(skill_array)
    skills_length = len(skills)
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
def inverse_document_frequency(term, skills, number_of_docuemts, all_freq_matrix):
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