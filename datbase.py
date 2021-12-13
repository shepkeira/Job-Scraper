import sqlite3
import io
from sqlite3 import Error
import csv
import os
import re

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


# backup database into many files
# github doesn't like large files, so we need to keep our backup files small
def backup_many_files():
    remove_old_databasefiles()
    conn = sql_connection()
    base_file = 'backupdatabase/backupdatabase_'
    count = 0
    file_count = 0
    max_lines = 1000000
    # vectors table has a very large string so we can keep less in one file
    vector_max_lines = 3000
    in_vectors = False
    current_max_lines = max_lines

    current_file = base_file + str(file_count) + ".sql"
    p = io.open(current_file, 'w', encoding="utf-8")
    for line in conn.iterdump():
        count += 1
        p.write('%s\n' % line)
        # if we are creating a table and its a vectors table we need to have less lines in the file
        if "_vectors" in line and "CREATE TABLE" in line:
            in_vectors = True
            p.write('%s\n' % "COMMIT;")
            p.close()
            count = 0
            file_count += 1
            current_file = base_file + str(file_count) + ".sql"
            p = io.open(current_file, 'w', encoding="utf-8")
            p.write('%s\n' % "BEGIN TRANSACTION;")
            current_max_lines = vector_max_lines
        # if we are creating a table and its not a vectors table we can reset to the standard table size
        if "CREATE TABLE" in line and "_vectors" not in line:
            in_vectors = False
            p.write('%s\n' % "COMMIT;")
            p.close()
            count = 0
            file_count += 1
            current_file = base_file + str(file_count) + ".sql"
            p = io.open(current_file, 'w', encoding="utf-8")
            p.write('%s\n' % "BEGIN TRANSACTION;")
            current_max_lines = max_lines
        # if we reach the max size we start a new file
        if(count >= current_max_lines):
            p.write('%s\n' % "COMMIT;")
            p.close()
            count = 0
            file_count += 1
            current_file = base_file + str(file_count) + ".sql"
            p = io.open(current_file, 'w', encoding="utf-8")
            p.write('%s\n' % "BEGIN TRANSACTION;")
    conn.close()

# connect to the database and back it up
def full_database_backup():
    print('Begin backup')
    backup_many_files()
    print('Backup performed successfully!')

# load a specific file from backup
def load_file_backup(script_file_path, conn):
    file = open(script_file_path, 'r', encoding='utf-8')
    sql_script_string = file.read()
    file.close()
    cursor = conn.cursor()
    cursor.executescript(sql_script_string)
    conn.commit()
    cursor.close()

# load all backup files (stored in the backupdatabase folder)
def load_database_from_folder():
    conn = sql_connection()
    files = os.listdir('./backupdatabase')
    files = sorted_alphanumeric(files)
    
    for file in files:
        if file.endswith(".sql"):
            script = "./backupdatabase/" + file
            print("starting on script: " + script)
            load_file_backup(script, conn)
    conn.close()

# sort database so that it is ordered backupdatabase_1, backupdatabase_2
# this way tables are loaded in the order they are created, and tables are created before data is inserted
def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(data, key=alphanum_key)

# remove old database files so we can add new ones
def remove_old_databasefiles():
    files = os.listdir('./backupdatabase')
    for file in files:
        if file.endswith(".sql"):
            script = "./backupdatabase/" + file
            os.remove(script)

# remove all data from a table
def empty_table(table):
    conn = sql_connection()
    cur = conn.cursor()
    statement = "DELETE FROM "+ table +";"
    cur.execute(statement)
    conn.commit()
    conn.close()
