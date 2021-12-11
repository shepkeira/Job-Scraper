import sqlite3
import io
from sqlite3 import Error

# make a connection to our database, or create a new one
def sql_connection():
    try:
        conn = sqlite3.connect('JobScrapper.db')
        return conn
    except Error:
        print(Error)
  
# create our skills tables
def sql_skill_table(conn):
    cursor_object = conn.cursor()
    cursor_object.execute(
        "CREATE TABLE software_skill(id integer PRIMARY KEY AUTOINCREMENT,\
                            skill text)")
    conn.commit()

    cursor_object = conn.cursor()
    cursor_object.execute(
        "CREATE TABLE cashier_skill(id integer PRIMARY KEY AUTOINCREMENT,\
                            skill text)")
    conn.commit()
    cursor_object.close()

# create our table of jobs
def sql_job_table(conn):
    
    cursor_object = conn.cursor()
    cursor_object.execute(
        "CREATE TABLE software_job(id integer PRIMARY KEY AUTOINCREMENT,\
                            summary_link text,\
                            full_summary text,\
                            link text,\
                            title text,\
                            company text,\
                            summary text)")
    conn.commit()
    cursor_object.execute(
        "CREATE TABLE software_id(id integer PRIMARY KEY AUTOINCREMENT,\
                                    job_id text);"
    )
    conn.commit()
    
    cursor_object.execute(
        "CREATE TABLE cashier_job(id integer PRIMARY KEY AUTOINCREMENT,\
                            summary_link text,\
                            full_summary text,\
                            link text,\
                            title text,\
                            company text,\
                            summary text)")
    conn.commit()
    cursor_object.execute(
        "CREATE TABLE cashier_id(id integer PRIMARY KEY AUTOINCREMENT,\
                                    job_id text);"

    )
    conn.commit()
    cursor_object.close()

# backup the data in our database
def backupdatabase(conn):
    with io.open('backupdatabase.sql', 'w', encoding="utf-8") as p:
        for line in conn.iterdump():
            p.write('%s\n' % line)

    print(' Backup performed successfully!')
    print(' Data Saved as backupdatabase_dump.sql')

# connect to the database and back it up
def full_database_backup():
    conn = sql_connection()
    backupdatabase(conn)
    conn.close()

# create our processed skills tables
def create_processed_skills_tables(conn):
    cursor_object = conn.cursor()
    cursor_object.execute(
        "CREATE TABLE software_processed_skill(id integer PRIMARY KEY AUTOINCREMENT,\
                            skill text,\
                            processed_skill text)")
    conn.commit()

    cursor_object = conn.cursor()
    cursor_object.execute(
        "CREATE TABLE cashier_processed_skill(id integer PRIMARY KEY AUTOINCREMENT,\
                            skill text,\
                            processed_skill text)")
    conn.commit()

# create our clustering tables
def create_cluster_tables(conn):
    cursor_object = conn.cursor()
    cursor_object.execute(
        "CREATE TABLE software_cluster(id integer PRIMARY KEY AUTOINCREMENT,\
                            skill_id int,\
                            cluster int,\
                            FOREIGN KEY (skill_id) REFERENCES software_processed_skill(id))")
    conn.commit()

    cursor_object = conn.cursor()
    cursor_object.execute(
        "CREATE TABLE cashier_cluster(id integer PRIMARY KEY AUTOINCREMENT,\
                            skill_id int,\
                            cluster int,\
                            FOREIGN KEY (skill_id) REFERENCES software_processed_skill(id))")
    conn.commit()
    cursor_object.close()

# creating our cosine tables
def create_cosine_tables(conn):
    cursor_object = conn.cursor()
    cursor_object.execute(
        "CREATE TABLE software_cosine_matrix(id integer PRIMARY KEY AUTOINCREMENT,\
                            skill_id_i int,\
                            skill_id_j int,\
                            value float,\
                            FOREIGN KEY (skill_id_i) REFERENCES software_processed_skill(id),\
                            FOREIGN KEY (skill_id_j) REFERENCES software_processed_skill(id))")
    conn.commit()

    cursor_object = conn.cursor()
    cursor_object.execute(
        "CREATE TABLE cashier_cosine_matrix(id integer PRIMARY KEY AUTOINCREMENT,\
                            skill_id_i int,\
                            skill_id_j int,\
                            value float,\
                            FOREIGN KEY (skill_id_i) REFERENCES software_processed_skill(id),\
                            FOREIGN KEY (skill_id_j) REFERENCES software_processed_skill(id))")
    conn.commit()
    cursor_object.close()

# creating our vectors tables
def create_vecotr_tables(conn):
    cursor_object = conn.cursor()
    cursor_object.execute(
        "CREATE TABLE software_vectors(id integer PRIMARY KEY AUTOINCREMENT,\
                            doc_vector text,\
                            skill_id int,\
                            FOREIGN KEY (skill_id) REFERENCES software_processed_skill(id))")
    conn.commit()

    cursor_object = conn.cursor()
    cursor_object.execute(
        "CREATE TABLE cashier_vectors(id integer PRIMARY KEY AUTOINCREMENT,\
                            doc_vector text,\
                            skill_id int,\
                            FOREIGN KEY (skill_id) REFERENCES cashier_processed_skill(id))")
    conn.commit()
    cursor_object.close()

# creating all the tables needed
def create_database():
    conn = sql_connection()
    sql_job_table(conn)
    sql_skill_table(conn)
    create_cluster_tables(conn)
    create_cosine_tables(conn)
    create_vecotr_tables(conn)
    create_processed_skills_tables(conn)
    conn.close()

# load the backup into our database
def load_jobs_backup():
    conn = sql_connection()
    script_file_paths = [
        './backupDatabase/ids.sql',
        './backupDatabase/jobs.sql',
    ]
    for script in script_file_paths:
        print("starting on script: " + script)
        load_file_backup(script, conn)  
    sql_skill_table(conn)
    create_processed_skills_tables(conn)
    create_cluster_tables(conn)
    create_cosine_tables(conn)
    create_vecotr_tables(conn)  
    conn.close()

# load the backup into our database
def load_backup():
    conn = sql_connection()
    script_file_paths = [
        './backupDatabase/cluster.sql',
        './backupDatabase/cosine_matrix_cashier.sql',
        './backupDatabase/cosine_matrix_software.sql',
        './backupDatabase/cosine_matrix_software_1.sql',
        './backupDatabase/cosine_matrix_software_2.sql',
        './backupDatabase/cosine_matrix_software_3.sql',
        './backupDatabase/cosine_matrix_software_4.sql',
        './backupDatabase/cosine_matrix_software_5.sql',
        './backupDatabase/cosine_matrix_software_6.sql',
        './backupDatabase/cosine_matrix_software_7.sql',
        './backupDatabase/cosine_matrix_software_8.sql',
        './backupDatabase/cosine_matrix_software_9.sql',
        './backupDatabase/ids.sql',
        './backupDatabase/raw_skills.sql',
        './backupDatabase/processed_skills.sql',
        './backupDatabase/jobs.sql',
        './backupDatabase/vectors_cashier.sql',
        './backupDatabase/vectors_software.sql',
        './backupDatabase/vectors_software_1.sql'
    ]
    for script in script_file_paths:
        print("starting on script: " + script)
        load_file_backup(script, conn)    
    conn.close()

def load_file_backup(script_file_path, conn):
    file = open(script_file_path, 'r', encoding='utf-8')
    sql_script_string = file.read()
    file.close()
    cursor = conn.cursor()
    cursor.executescript(sql_script_string)
    conn.commit()
    cursor.close()