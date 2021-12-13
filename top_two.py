from datbase import sql_connection
from dictances import bhattacharyya_coefficient
from collections import Counter

# table names
TABLE_NAMES = {
    'software_engineer': {
        'processed': 'software_processed_skill',
        'cluster': 'software_cluster'
    },
    'cashier': {
        'processed': 'cashier_processed_skill',
        'cluster': 'cashier_cluster'
    },
}

# calculate the distnace between the two skills
# skills is an array of dictionaries of length 2
# [{"skill": skill_string, "count": count_int, "processed": processed_skill_string}, {"skill": skill_string, "count": count_int, "processed": processed_skill_string}]
def clustering_dist(skills):
    # get the two skills and counts
    skill1 = skills[0]['skill']
    count1 = skills[0]['count']
    processed1 = skills[0]['processed']
    skill2 = skills[1]['skill']
    count2 = skills[1]['count']
    processed2 = skills[1]['processed']

    # we can to use the processed skills for the bhattacharyya coefficient
    # turn the skill string into a dictionary with Conter
    # calculate the bhattacharyya_coefficient for the two skills
    dist = bhattacharyya_coefficient(Counter(processed1), Counter(processed2))
    # print the results to the screen
    # we print the unprocessed skill because they are easier to read since they are not stemmed
    print("---------------------------------------------------------------------")
    print("The top two skills are: \n\"" + skill1 + "\" with: "+ str(count1) +" \nand\n\"" + skill2 + "\" with: " + str(count2))
    print("The distance between these two skills is: " + str(dist))
    print("---------------------------------------------------------------------")

# from the processed skills find the top two skills without clustering
def top_two_skill_before_clustering(job_title):
    # collect the count of all the porcessed_skills that are the same
    # return only the top two
    conn = sql_connection()
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['processed']
    statement = "SELECT skill, count(processed_skill) as skill_count, processed_skill as skill_count FROM " + table + " GROUP BY processed_skill ORDER BY skill_count DESC LIMIT 2;"
    
    cursor.execute(statement)
    output = cursor.fetchall()
    cursor.close()
    conn.close()
    skills = []
    # return a list of dictionaries with the skill count and the skills, and the processed skills
    for row in output:
        skill = row[0]
        count = row[1]
        processed = row[2]
        skill_dict = {'skill': skill, 'count': count, 'processed': processed}
        skills.append(skill_dict)
    return skills

# after clustering caluclate the top two skills
def top_two_skill_after_clustering(job_title):
    # return the count of skills in each cluster
    # return only the top two
    conn = sql_connection()
    cursor = conn.cursor()
    table_c = TABLE_NAMES[job_title]['cluster']
    table_p = TABLE_NAMES[job_title]['processed']
    statement = "SELECT count(cluster) as skill_count, cluster FROM "+ table_c +" JOIN "+ table_p +" ON "+ table_p +".id = "+ table_c +".skill_id GROUP BY cluster ORDER BY skill_count DESC LIMIT 2;"
    cursor.execute(statement)
    output = cursor.fetchall()

    skill_counts = [ele[0] for ele in output]
    clusters = [ele[1] for ele in output]
    skill_string = []
    processed_string = []

    # for each of the top two clusters return the skill and processed_skill that is the most common for display puroses
    # this is usually the simplest wording of a skill e.g. SQL is more likely than 3-5 years of industry experince using SQL

    for cluster in clusters:
        statement = "SELECT skill, count(processed_skill) as skill_count, processed_skill FROM "+table_p+" JOIN "+table_c+" ON "+table_c+".skill_id = "+table_p+".id WHERE cluster = "+str(cluster)+" GROUP BY processed_skill ORDER BY skill_count DESC LIMIT 1;"    
        cursor.execute(statement)
        output = cursor.fetchall()
        skill_string.append(output[0][0])
        processed_string.append(output[0][2])
    skills = []
    # return a list of dictionaries with the skill count and the skills, and the processed_skill
    i = 0
    for row in skill_counts:
        skill = skill_string[i]
        processed = processed_string[i]
        count = row
        skill_dict = {'skill': skill, 'count': count, 'processed': processed}
        skills.append(skill_dict)
        i += 1

    cursor.close()
    conn.close()
    return skills