from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError

RECOUNT_TRY = 3

def scrapsummary(URL):
    summaries_text = ""
    req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        web_page = urlopen(req).read()
        soup = BeautifulSoup(web_page, 'html.parser')
        # print(soup)
        
        summaries = soup.find_all('div', attrs={'id': 'jobDescriptionText'})
        for summary in summaries:
            summary_text = summary.get_text()
            summaries_text = summaries_text + str(summary_text)
        return summaries_text
    except HTTPError:
        print("Job Summary Error")
        return ""