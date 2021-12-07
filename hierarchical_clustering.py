TABLE_NAMES = {
    'software_engineer': {
        'skills': 'software_skill',
        'jobs': 'software_job',
        'processed': 'software_processed_skill',
        'vector': 'software_vectors',
        'matrix': 'software_cosine_matrix',
        'cluster': 'software_cluster'
    },
    'cashier': {
        'skills': 'cashier_skill',
        'jobs': 'cashier_job',
        'processed': 'cashier_processed_skill',
        'vector': 'cashier_vectors',
        'matrix': 'cashier_cosine_matrix',
        'cluster': 'cashier_cluster'
    },
}

def cluster_skills(conn, job_title):
    dist = 0
    cluster = 0
    while(dist < 1):
        #find row with smallest value in matrix 
        row = smallest_dist(conn, job_title)
        current_clusters = get_current_clusters(conn, job_title, row)
        if(len(current_clusters) == 2):
            #both already clustered
            update_2_clusters(conn, job_title, current_clusters, cluster)
        elif(len(current_clusters) == 1):
            # if either of the skills is in a cluster set old cluster and new element to cluster
            update_1_clusters(conn, job_title, current_clusters, cluster, row)
        else:
            #if neither skill is in a cluster set cluster to m
            insert_2_clusters(conn, job_title, cluster, row)
        dist = row['value']
        cluster += 1
    print("cluster calculated")

def insert_2_clusters(conn, job_title, cluster, row):
    values = [[row['skill_id_i'], cluster], [row['skill_id_j'], cluster]]
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['cluster']
    insert_record = "INSERT INTO "+ table +"(skill_id, cluster) VALUES (?,?)"
    cursor.executemany(insert_record, values)
    cursor.close()

def update_1_clusters(conn, job_title, clusters, cluster, row):
    old_cluster = clusters[0]
    both_ids = [row['skill_id_i'], row['skill_id_j']]
    update_ids = [ele['id'] for ele in clusters]
    insert_id = [x for x in both_ids if x not in update_ids][0]
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['cluster']
    statement = "UPDATE "+ table +" SET cluster = "+ cluster +" WHERE cluster IN (?);"
    cursor.execute(statement, [old_cluster])
    insert_record = "INSERT INTO "+ table +"(skill_id, cluster) VALUES (?,?)"
    cursor.execute(insert_record, [insert_id, cluster])
    cursor.close()

def update_2_clusters(conn, job_title, clusters, cluster):
    old_clusters = [ele['cluster'] for ele in clusters]
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['cluster']
    statement = "UPDATE "+ table +" SET cluster = ? WHERE cluster IN (?,?);"
    cursor.execute(statement, [cluster] + old_clusters)
    cursor.close()

def get_current_clusters(conn, job_title, row):
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['cluster']
    statement = "SELECT * FROM "+ table +" WHERE skill_id = "+ str(row['skill_id_i'])+" OR skill_id = "+ str(row['skill_id_j'])+";"
    cursor.execute(statement)
    output = cursor.fetchall()
    cursor.close()
    rows = [{'id': ele[1], 'cluster': ele[2]} for ele in output]
    return rows

def smallest_dist(conn, job_title):
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['matrix']
    statement = "SELECT * FROM "+ table +" WHERE skill_id_i <> skill_id_j ORDER BY value, skill_id_i, skill_id_j LIMIT 1"
    
    cursor.execute(statement)
    output = cursor.fetchone()
    cursor.close()
    row = {'skill_id_i': output[1], 'skill_id_j': output[2], 'value': output[3]}
    return row
