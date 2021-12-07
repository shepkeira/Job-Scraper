import csv
import sqlite3
import io
from sqlite3 import Error
import json

def sql_connection():
    try:
        conn = sqlite3.connect('JobScrapper.db')
        return conn
    except Error:
        print(Error)
  
def sql_sw_skill_table(conn):
    cursor_object = conn.cursor()
    cursor_object.execute(
        "CREATE TABLE software_skill(id integer PRIMARY KEY AUTOINCREMENT,\
                            skill text)")
    conn.commit()

def sql_cashier_skill_table(conn):
    cursor_object = conn.cursor()
    cursor_object.execute(
        "CREATE TABLE cashier_skill(id integer PRIMARY KEY AUTOINCREMENT,\
                            skill text)")
    conn.commit()

def sql_sw_job_table(conn):
    
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

def sql_cashier_job_table(conn):
    
    cursor_object = conn.cursor()
    cursor_object.execute(
        "CREATE TABLE cashier_job(id integer PRIMARY KEY AUTOINCREMENT,\
                            summary_link text,\
                            full_summary text,\
                            link text,\
                            title text,\
                            company text,\
                            summary text)")
    conn.commit()

def insert_cashier_job(conn):
    cursor = conn.cursor()

    with open("data/cashier.txt", 'r') as f:
        jobs = f.readlines()

    newegg_jsons = []
    for job in jobs:
        newegg_json = json.loads(job)
        newegg_jsons.append(newegg_json)
        column = []
        columns = []
    for data in newegg_jsons:
        column = list(data.keys())
        for col in column:
            if col not in columns:
                columns.append(col)

    value = []
    values = []
    for data in newegg_jsons:
        for i in columns:
            value.append(str(dict(data).get(i)))
        values.append(list(value))
        value.clear()


    insert_record = "INSERT INTO cashier_job (summary_link, full_summary, link, title, company, summary) VALUES (?,?,?,?,?,?)"
    # for value in values:
    cursor.executemany(insert_record, values)
    conn.commit()
    cursor.close()

def insert_swe_job(conn):
    cursor = conn.cursor()

    with open("data/software_engineer.txt", 'r') as f:
        jobs = f.readlines()

    newegg_jsons = []
    for job in jobs:
        newegg_json = json.loads(job)
        newegg_jsons.append(newegg_json)
        column = []
        columns = []
    for data in newegg_jsons:
        column = list(data.keys())
        for col in column:
            if col not in columns:
                columns.append(col)

    value = []
    values = []
    for data in newegg_jsons:
        for i in columns:
            value.append(str(dict(data).get(i)))
        values.append(list(value))
        value.clear()


    insert_record = "INSERT INTO software_job (summary_link, full_summary, link, title, company, summary) VALUES (?,?,?,?,?,?)"
    # for value in values:
    cursor.executemany(insert_record, values)
    conn.commit()
    cursor.close()

def save_ids(conn):
    cursor_object = conn.cursor()
    cursor_object.execute(
        "CREATE TABLE software_id(id integer PRIMARY KEY AUTOINCREMENT,\
                            job_id text)")
    conn.commit()

    cursor_object = conn.cursor()
    cursor_object.execute(
        "CREATE TABLE cashier_id(id integer PRIMARY KEY AUTOINCREMENT,\
                            job_id text)")
    conn.commit()

    with open("data/software_engineer_ids.txt", 'r') as f:
        ids_str = f.readline()
    ids = ids_str.split(',')

    value = []
    values = []
    for id in ids:
        values.append([id])
        value.clear()

    insert_record = "INSERT INTO software_id (job_id) VALUES (?)"
    # for value in values:
    cursor_object.executemany(insert_record, values)
    conn.commit()

    with open("data/cashier_ids.txt", 'r') as f:
        ids_str = f.readline()
    ids = ids_str.split(',')

    value = []
    values = []
    for id in ids:
        values.append([id])
        value.clear()

    insert_record = "INSERT INTO cashier_id (job_id) VALUES (?)"
    # for value in values:
    cursor_object.executemany(insert_record, values)
    conn.commit()

    cursor_object.close()

def backupdatabase(conn):
    with io.open('backupdatabase.sql', 'w', encoding="utf-8") as p:
        for line in conn.iterdump():
            p.write('%s\n' % line)

    print(' Backup performed successfully!')
    print(' Data Saved as backupdatabase_dump.sql')


def full_database_backup():
    conn = sql_connection()
    backupdatabase(conn)
    conn.close()

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


def create_cluster_tables():
    conn = sql_connection()
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
                            skill_id_i int,\
                            skill_id_j int,\
                            value float,\
                            FOREIGN KEY (skill_id_i) REFERENCES software_processed_skill(id),\
                            FOREIGN KEY (skill_id_j) REFERENCES software_processed_skill(id))")
    conn.commit()

def create_cosine_tables():
    conn = sql_connection()
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
    
    # Close the connection
    conn.close()

def create_vecotr_tables():
    conn = sql_connection()
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
    
    # Close the connection
    conn.close()

def create_database():
    conn = sql_connection()
    sql_sw_job_table(conn)
    sql_cashier_job_table(conn)

    # insert_swe_job(conn)
    # insert_cashier_job(conn)

    # save_ids(conn)

    # sql_cashier_skill_table(conn)
    # sql_sw_skill_table(conn)

    backupdatabase(conn)

    conn.close()