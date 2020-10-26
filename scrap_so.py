
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import requests # Getting Webpage content
from bs4 import BeautifulSoup as bs # Scraping webpages

def get_answer(q_url):
    """
    The function extracts answers by url of question

    :param q_url: string (url of the question)
    :return: list (list of answers)
    """
    # Extracting answer
    answ_url = q_url
    answ_page = requests.get(answ_url)
    answ_soup = bs(answ_page.text, 'html.parser')
    table = answ_soup.findAll('div', attrs={"class": "s-prose js-post-body"})
    answers = []

    for par in table:
        try:
            s = (par.find('p').text).strip()
            answers.append(s)
            # answers = answers + '. ' + (par.find('p').text) # if output as string is needed
        except:
            pass
    return answers



def get_faq(url, tag, n_questions=50):
    """
    The function uses url and tag to find and collect the frequently asked questions
    and relevant answers from stackoverflow.com. The function returns
    dataframe with questions, summary, link and list of answers.

    :param url: URL = 'https://stackoverflow.com/questions'
    :param tag: string (!StackOverflow tags only!)
    :param n_questions: integer
    :return: pd.DataFrame
    """
    simple_list = [[]]
    for n in range(int(n_questions/50) + 1):
        url0 = url + "/tagged/" + tag + "?sort=votes&page={}pagesize={}".format(n + 1,n_questions)

        r = requests.get(url0)
        soup = bs(r.text, "html.parser")

        # Extracting questions and links
        link_hrefs = soup.select("a.question-hyperlink")
        questions = [l.text.strip() for l in link_hrefs]  # questions list
        href_tags = [url[:-10] + l['href'] for l in link_hrefs]  # links list

        # Extracting additional information for question (summary)
        summary_divs = soup.select("div.excerpt")
        summaries = [i.text.strip() for i in summary_divs]  # summaries list

        # Creating a list with all the data
        for i in range(1,len(questions)-1):
            try:
                answer_lst = get_answer(href_tags[i])
                simple_list.append([questions[i], summaries[i], href_tags[i], answer_lst])
            except:
                pass

    # Putting all of them together in a dataframe
    df = pd.DataFrame(simple_list, columns=['question', 'summary', 'link', 'answers'])
    df = df.head(n_questions + 1)

    return df

def test_scrap(f1=False, f2=True):
    """
    The test function, used for displaying the result of web-scrapping on the screen.
    By default only main function is tested, but testing of get_answer function
    can be enabled separately.

    :return: None
    """
    if f1: # test for get_answer function
        QURL = 'https://stackoverflow.com/questions/5041008/how-to-find-elements-by-class'
        print(get_answer(QURL))

    if f2: # test for get_forum_text function
        URL = 'https://stackoverflow.com/questions'
        TAG = 'python'
        print(get_faq(URL, TAG, 40).head(10))


def main():
    """Main function"""

    URL = 'https://stackoverflow.com/questions'
    TAG = 'web-scraping'

    df0 = get_faq(URL, TAG, 50)
    df0.to_csv('scrap_so.csv')
    print(df0.head())

if __name__ == '__main__':
    # main()
    test_scrap()



