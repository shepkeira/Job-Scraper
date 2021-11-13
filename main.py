from jobscrapper import scrapweb
from process import processfiles, processskills

if __name__ == "__main__":
    # URL = 'https://ca.indeed.com/jobs?q=software%20engineer&l=canada&sort=date'
    file_name = "software_engineer.txt"
    # scrapweb(URL, file_name)
    #processfiles(file_name)
    top_2_skills = processskills(file_name)
    print(top_2_skills)
    # URL2 = 'https://ca.indeed.com/jobs?q=cashier&l=canada&sort=date'
    file_name2 = "cashier.txt"
    # scrapweb(URL2, file_name2)
    processfiles(file_name2)
    top_2_skills = processskills(file_name2)
    print(top_2_skills)

    #eliminate duplicate jobs
    #get more jobs
    #try again