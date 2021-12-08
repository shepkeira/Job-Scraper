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
        "CREATE TABLE cashier_job(id integer PRIMARY KEY AUTOINCREMENT,\
                            summary_link text,\
                            full_summary text,\
                            link text,\
                            title text,\
                            company text,\
                            summary text)")
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
def create_processed_skills_tables():
    conn = sql_connection()
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

    conn.close()

# load the backup into our database
def load_backup():
    conn = sql_connection()
    script_file_path = './backupdatabase.sql'
    file = open(script_file_path, 'r')
    sql_script_string = file.read()
    file.close()
    cursor = conn.cursor()
    cursor.executescript(sql_script_string)
    conn.commit()
    cursor.close()
    conn.close()