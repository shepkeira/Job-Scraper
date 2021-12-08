from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError

RECOUNT_TRY = 3

# this function takes in a URL for a job pages and returns a string of the summary
def scrapsummary(URL):
    # default stirng is empty
    summaries_text = ""
    # request the HTML from the URL
    req = Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        web_page = urlopen(req).read()
        soup = BeautifulSoup(web_page, 'html.parser')
        # we use BeautifulSoup to parse our HTML
        
        # find the summaries on the page under the id: 'jobDescriptionText'
        summaries = soup.find_all('div', attrs={'id': 'jobDescriptionText'})
        # this should return only one results but it gets returned as an array no matter what
        # this loop is here because summaries is an array even though it should only every return one result
        for summary in summaries:
            summary_text = summary.get_text()
            summaries_text = summaries_text + str(summary_text)
        return summaries_text
    # if there is an error getting to the page, print to the screen and return an empty string
    except HTTPError:
        print("Job Summary Error")
        return ""