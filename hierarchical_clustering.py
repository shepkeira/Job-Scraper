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

# cluster skills based on their cosine distance and single linkage (smallest distance)
def cluster_skills(conn, job_title):
    # we need to start with all the skills in their own cluster
    clear_old_cluster_from_table(conn, job_title)
    # we order all our rows by the smallest distance
    # since its cosine distance 1.0 means they are the same and 0.0 means they are completely different
    rows = smallest_dist(conn, job_title)
    # calculate the length of the rows
    N = len(rows)
    # for each row
    for n in range(0, N):
        # get the current row
        row = rows[n]
        # get the clusters for the skills in that row
        current_clusters = get_current_clusters(conn, job_title, row)
        if(len(current_clusters) == 2):
            #both already clustered
            update_2_clusters(conn, job_title, current_clusters, n)
        elif(len(current_clusters) == 1):
            # if either of the skills is in a cluster set old cluster and new element to cluster
            update_1_clusters(conn, job_title, current_clusters, n, row)
        else:
            #if neither skill is in a cluster set cluster to m
            insert_2_clusters(conn, job_title, n, row)
    print("cluster calculated")

#if neither are clustered we inset two new rows
def insert_2_clusters(conn, job_title, cluster, row):
    values = [[row['skill_id_i'], cluster], [row['skill_id_j'], cluster]]
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['cluster']
    insert_record = "INSERT INTO "+ table +"(skill_id, cluster) VALUES (?,?)"
    cursor.executemany(insert_record, values)
    conn.commit()
    cursor.close()

#if one is clustered we enter a row and update all values in our old cluster
def update_1_clusters(conn, job_title, clusters, cluster, row):
    old_cluster = clusters[0]['cluster']
    both_ids = [row['skill_id_i'], row['skill_id_j']]
    update_ids = [ele['id'] for ele in clusters]
    insert_id = [x for x in both_ids if x not in update_ids][0]
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['cluster']
    statement = "UPDATE "+ table +" SET cluster = ? WHERE cluster IN (?);"
    cursor.execute(statement, [cluster, old_cluster])
    insert_record = "INSERT INTO "+ table +"(skill_id, cluster) VALUES (?,?)"
    cursor.execute(insert_record, [insert_id, cluster])
    conn.commit()
    cursor.close()

# if both are clusterd we update both exisiting clusters and merge them into one new cluster
def update_2_clusters(conn, job_title, clusters, cluster):
    old_clusters = [ele['cluster'] for ele in clusters]
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['cluster']
    statement = "UPDATE "+ table +" SET cluster = ? WHERE cluster IN (?,?);"
    cursor.execute(statement, [cluster] + old_clusters)
    conn.commit()
    cursor.close()

# return the rows with of clusters with the requested skill_ids
def get_current_clusters(conn, job_title, row):
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['cluster']
    statement = "SELECT * FROM "+ table +" WHERE skill_id = "+ str(row['skill_id_i'])+" OR skill_id = "+ str(row['skill_id_j'])+";"
    cursor.execute(statement)
    output = cursor.fetchall()
    cursor.close()
    rows = [{'id': ele[1], 'cluster': ele[2]} for ele in output]
    return rows

# return the rows of the cosine matrix table sorted by value form largest to smallest, then in the order you would look through for the smallest value
def smallest_dist(conn, job_title):
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['matrix']
    statement = "SELECT * FROM "+ table +" WHERE skill_id_i <> skill_id_j AND value > .6 ORDER BY value DESC, skill_id_i, skill_id_j"
    
    cursor.execute(statement)
    output = cursor.fetchall()
    cursor.close()
    rows = []
    for line in output:
        row = {'skill_id_i': line[1], 'skill_id_j': line[2], 'value': line[3]}
        rows.append(row)
    return rows

# clear the old value from the clustering
def clear_old_cluster_from_table(conn, job_title):
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['cluster']
    statement = "DELETE FROM "+ table +";"
    
    cursor.execute(statement)
    conn.commit()
    cursor.close()