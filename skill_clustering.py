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

# this function takes in the job_title an calculates the clusters for that job's skills
def cluster(job_title):
    conn = sql_connection()
    #get processed skills
    print("Calculating Document Vectors")
    processed_skills = query_for_processed_skills(job_title, conn)
    get_document_vectors(conn, job_title, processed_skills) #only add vectors we don't have yet
    # #save document vectors to a table
    # #cacluate cosine matrix as [x,y] = z table columns x,y,z
    print("Cacluating Cosine Matrix")
    calculate_cosine_matrix(conn, job_title)
    #cluster
    print("Calculating Clusters")
    cluster_skills(conn, job_title)
    #save cluster assignments to table
    conn.close()

#this function finds the cosine matrix entry with the highest skill_id_i
#this will give us our starting point to cacluate new cosine distances
def query_for_vector_id(job_title, conn):
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['matrix']
    statement = "SELECT skill_id_i FROM "+ table +" ORDER BY skill_id_i DESC LIMIT 1"
    cursor.execute(statement)
    output = cursor.fetchall()
    id = output[0][0]
    cursor.close()
    return id

#this function retrives our document vectors, and calculates thier cosine distance
def calculate_cosine_matrix(conn, job_title, last_id):
    vectors = query_for_vectors(job_title, conn)
    get_cosine_matrix(vectors, conn, job_title, last_id)

#this function writes our cosine values to the cosine_matrix table
def write_values(values, conn, job_title):
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['matrix']
    insert_record = "INSERT INTO "+ table +" (skill_id_i, skill_id_j, value) VALUES (?,?,?)"
    cursor.executemany(insert_record, values)
    conn.commit()
    cursor.close()

# this function takes in the document_vectors, job_title, and a database connection
def get_cosine_matrix(skills_vectors, conn, job_title):
    values = [] # values to be entered into the database
    norms = {} # the vector magnitude of the document vectors
    #full length of the skills matrix
    N = len(skills_vectors) 
    # clear out old cosines since our document vecotors could change everytime
    clear_old_consines_from_table(conn, job_title)
    for i in range(0, N):
        # we get our jth row and its skill_id, and document vector
        row_i = skills_vectors[i]
        skill_id_i = row_i['skill_id']
        vecotr_i = np.array(row_i['doc_vector'].split(",")).astype(np.float)
        # if we have already calculated this norm we retirve it
        # if not we calculate the norm for this vecotr and save it in norms
        if skill_id_i not in norms:
            norm_i = norm(vecotr_i)
            norms[skill_id_i] = norm_i
        else:
            norm_i = norms[skill_id_i]
        # we start j at i+1 because we ignore diagonals (we don't need to cluster i with i)
        for j in range(i+1, N):
            # we get our jth row and its skill_id, and document vector
            row_j = skills_vectors[j]
            skill_id_j = row_j['skill_id']
            vecotr_j = np.array(row_j['doc_vector'].split(",")).astype(np.float)
            # if we have already calculated this norm we retirve it
            # if not we calculate the norm for this vecotr and save it in norms
            if skill_id_j not in norms:
                norm_j = norm(vecotr_j)
                norms[skill_id_j] = norm_j
            else:
                norm_j = norms[skill_id_j]
            # next we calculate the cosine similarity
            value_i_j = dot(vecotr_i, vecotr_j)/(norm_i*norm_j)
            # next we want to save all the vectors into value in the correct order
            value = [skill_id_i, skill_id_j, value_i_j]
            # then we append this to values
            values.append(value)
        # we write the contents of values to the cosine table
        write_values(values, conn, job_title)
        # we reset values to an empty array to save memory
        values = []

# this function retrieves all the document vectors that have been caluclated
def query_for_vectors(job_title, conn):
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['vector']
    statement = "SELECT * FROM "+ table
    
    cursor.execute(statement)
    output = cursor.fetchall()
    cursor.close()
    rows = [{'id': ele[0], 'doc_vector': ele[1], 'skill_id': ele[2]} for ele in output]
    return rows

# this function will return all the stemmed words from the skills
def term_freqency(skills_array):
    term_freq = {}
    # for each skill split into terms
    for _id, skill in skills_array:
        skill = skill.split(" ")
        # for each term increase the count or set it to 1
        for term in skill:
            if term in term_freq:
                term_freq[term] =+ 1
            else:
                term_freq[term] = 1
    return term_freq

# this will calculate the document vector for all the new processed_skills
def get_document_vectors(conn, job_title, processed_skills):
    #get id and document vector for each skill
    skills_array = [[ele['id'], ele['processed']] for ele in processed_skills]
    skills_length = len(processed_skills)
    # find the term_frequency for all skills
    term_freq = term_freqency(skills_array)
    # find all the terms
    terms = list(term_freq.keys())
    # we store the document_vectors as [[id, [document vector]],[id, [document vector]],...]
    document_vectors = []
    # clear out the old values as they have to be recalulated with our new term frequency
    clear_old_vectors_from_table(conn, job_title)
    # for each processed skill
    for id, skill in skills_array:
        # to calcualate the document vecotr we need 
        #                    terms, skill, skills_length, all_freq_matrix
        dv = document_vector(terms, skill, skills_length, term_freq)
        # save the document vector as a string
        dv_str = ','.join(str(x) for x in dv)
        # save the row as id, document_vector_string
        row = [id, dv_str]
        # add this row to our document_vectors
        document_vectors.append(row)
    # write all the vectors to the database
    write_to_database(document_vectors, job_title, conn)

# clear all the vectors from the table
def clear_old_vectors_from_table(conn, job_title):
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['vector']
    statement = "DELETE FROM "+ table +";"
    
    cursor.execute(statement)
    conn.commit()
    cursor.close()

# clear all the vectors from the table
def clear_old_consines_from_table(conn, job_title):
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['matrix']
    statement = "DELETE FROM "+ table +";"
    
    cursor.execute(statement)
    conn.commit()
    cursor.close()

# write the document vectors to the table
def write_to_database(document_vectors, job_title, conn):
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['vector']
    insert_record = "INSERT INTO "+ table +" (skill_id, doc_vector) VALUES (?,?)"
    cursor.executemany(insert_record, document_vectors)
    conn.commit()
    cursor.close()

# query to find all the proccessed skills
def query_for_processed_skills(job_title, conn):
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['processed']
    statement = "SELECT * FROM "+ table
    
    cursor.execute(statement)
    output = cursor.fetchall()
    cursor.close()
    rows = [{'id': ele[0], 'skill': ele[1], 'processed': ele[2]} for ele in output]
    return rows
