from datbase import sql_connection
from dictances import bhattacharyya_coefficient
from collections import Counter

# table names
TABLE_NAMES = {
    'software_engineer': {
        'processed': 'software_processed_skill'
    },
    'cashier': {
        'processed': 'cashier_processed_skill'
    },
}


def before_clustering_dist(skills):
    skill1 = skills[0]['skill']
    count1 = skills[0]['count']
    skill2 = skills[1]['skill']
    count2 = skills[1]['count']

    dist = bhattacharyya_coefficient(Counter(skill1), Counter(skill2))
    print("The top two skills are: \"" + skill1 + "\" with: "+ count1 +" and \"" + skill2 + "\" with: " + count2)
    print("The distance between these two skills is: " + str(dist))
    return dist

# from the processed skills find the top two skills
def top_two_skill_before_clustering(job_title):
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