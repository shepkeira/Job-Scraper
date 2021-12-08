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
# [{"skill": skill_string, "count": count_int}, {"skill": skill_string, "count": count_int}]
def clustering_dist(skills):
    # get the two skills and counts
    skill1 = skills[0]['skill']
    count1 = skills[0]['count']
    skill2 = skills[1]['skill']
    count2 = skills[1]['count']

    # turn the skill string into a dictionary with Conter
    # calculate the bhattacharyya_coefficient for the two skills
    dist = bhattacharyya_coefficient(Counter(skill1), Counter(skill2))
    # print the results to the screen
    print("The top two skills are: \n\"" + skill1 + "\" with: "+ str(count1) +" \nand\n \"" + skill2 + "\" with: " + str(count2))
    print("The distance between these two skills is: " + str(dist))

# from the processed skills find the top two skills without clustering
def top_two_skill_before_clustering(job_title):
    # collect the count of all the porcessed_skills that are the same
    # return only the top two
    conn = sql_connection()
    cursor = conn.cursor()
    table = TABLE_NAMES[job_title]['processed']
    statement = "SELECT skill, count(processed_skill) as skill_count FROM " + table + " GROUP BY processed_skill ORDER BY skill_count DESC LIMIT 2;"
    
    cursor.execute(statement)
    output = cursor.fetchall()
    cursor.close()
    conn.close()
    skills = []
    # return a list of dictionaries with the skill count and the skills
    for row in output:
        skill = row[0]
        count = row[1]
        skill_dict = {'skill': skill, 'count': count}
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
    statement = "SELECT count(cluster) as skill_count, skill FROM "+ table_c +" JOIN "+ table_p +" ON "+ table_p +".id = "+ table_c +".skill_id GROUP BY cluster ORDER BY skill_count DESC LIMIT 2;"
    cursor.execute(statement)
    output = cursor.fetchall()
    cursor.close()
    conn.close()
    skills = []
    # return a list of dictionaries with the skill count and the skills
    for row in output:
        skill = row[1]
        count = row[0]
        skill_dict = {'skill': skill, 'count': count}
        skills.append(skill_dict)
    return skills