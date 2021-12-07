import math
from datbase import sql_connection
from document_vector import document_vector
from hierarchical_clustering import cluster_skills
import numpy as np
from numpy import dot
from numpy.linalg import norm

TABLE_NAMES = {
    'software_engineer': {
        'skills': 'software_skill',
        'jobs': 'software_job',
        'processed': 'software_processed_skill',
        'vector': 'software_vectors',
        'matrix': 'software_cosine_matrix'
    },
    'cashier': {
        'skills': 'cashier_skill',
        'jobs': 'cashier_job',
        'processed': 'cashier_processed_skill',
        'vector': 'cashier_vectors',
        'matrix': 'cashier_cosine_matrix'
    },
}

def cluster(job_title):
    conn = sql_connection()
    #get processed skills
    # processed_skills = query_for_processed_skills(job_title, conn)
    # get_document_vectors(conn, job_title, processed_skills) #only add vectors we don't have yet
    #save document vectors to a table
    #cacluate cosine matrix as [x,y] = z table columns x,y,z
    # calculate_cosine_matrix(conn, job_title)
    #cluster
    cluster_skills(conn, job_title)
    #save cluster assignments to table
    conn.close()
    
def calculate_cosine_matrix(conn, job_title):
    vectors = query_for_vectors(job_title, conn)
    values = get_cosine_matrix(vectors, conn, job_title)

def write_values(values, conn, job_title):
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['matrix']
    insert_record = "INSERT INTO "+ table +" (skill_id_i, skill_id_j, value) VALUES (?,?,?)"
    cursor.executemany(insert_record, values)
    conn.commit()
    cursor.close()

# input: a list of document vectors and the file names for each document
# output: a matrix and a list of file_names in the order placed in the matrix
def get_cosine_matrix(skills_vectors, conn, job_title):
    # [{'id': ele[0], 'doc_vector': ele[1], 'skill_id': ele[2]}]
    values = []
    norms = {}
    N = len(skills_vectors) #add something here to find the max id, and start from there?
    for i in range(0, N-1):
        row_i = skills_vectors[i]
        skill_id_i = row_i['skill_id']
        vecotr_i = np.array(row_i['doc_vector'].split(",")).astype(np.float)
        if skill_id_i not in norms:
            norm_i = norm(vecotr_i)
            norms[skill_id_i] = norm_i
        else:
            norm_i = norms[skill_id_i]
        for j in range(i+1, N-1):
            row_j = skills_vectors[j]
            skill_id_j = row_j['skill_id']
            vecotr_j = np.array(row_j['doc_vector'].split(",")).astype(np.float)
            if skill_id_j not in norms:
                norm_j = norm(vecotr_j)
                norms[skill_id_j] = norm_j
            else:
                norm_j = norms[skill_id_j]
            value_i_j = dot(vecotr_i, vecotr_j)/(norm_i*norm_j)
            if value_i_j <= 1:
                value = [skill_id_i, skill_id_j, value_i_j]
                values.append(value)
        write_values(values, conn, job_title)
        values = []
    return values

def query_for_vectors(job_title, conn):
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['vector']
    statement = "SELECT * FROM "+ table
    
    cursor.execute(statement)
    output = cursor.fetchall()
    cursor.close()
    rows = [{'id': ele[0], 'doc_vector': ele[1], 'skill_id': ele[2]} for ele in output]
    return rows

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



def term_freqency(skills_array):
    term_freq = {}
    for _id, skill in skills_array:
        skill = skill.split(" ")
        for term in skill:
            if term in term_freq:
                term_freq[term] =+ 1
            else:
                term_freq[term] = 1
    return term_freq

def get_document_vectors(conn, job_title, processed_skills):
    #get document vector for each skill
    skills_array = [[ele['id'], ele['processed']] for ele in processed_skills]
    skills_length = len(processed_skills)
    term_freq = term_freqency(skills_array)
    terms = list(term_freq.keys())
    document_vectors = []
    for id, skill in skills_array:
        #terms, skill, skills_length, all_freq_matrix
        dv = document_vector(terms, skill, skills_length, term_freq)
        dv_str = ','.join(str(x) for x in dv)
        row = [id, dv_str]
        document_vectors.append(row)
    write_to_database(document_vectors, job_title, conn)

def write_to_database(document_vectors, job_title, conn):
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['vector']
    insert_record = "INSERT INTO "+ table +" (skill_id, doc_vector) VALUES (?,?)"
    cursor.executemany(insert_record, document_vectors)
    conn.commit()
    cursor.close()


def query_for_processed_skills(job_title, conn):
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['processed']
    statement = "SELECT * FROM "+ table
    
    cursor.execute(statement)
    output = cursor.fetchall()
    cursor.close()
    rows = [{'id': ele[0], 'skill': ele[1], 'processed': ele[2]} for ele in output]
    return rows
