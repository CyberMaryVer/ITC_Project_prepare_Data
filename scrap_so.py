import pandas as pd
import requests
from bs4 import BeautifulSoup
from math import ceil
import sys

PAGE_SIZE = 50


def get_answer(url):
    """ Extracts answers for a stack overflow question

    :param str url: url of the question
    :return: list of answers
    :rtype: list
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    table = soup.findAll('div', attrs={"class": "s-prose js-post-body"})

    return [answer.text.strip() for par in table if (answer := par.find('p')) is not None]


def get_faq(url, tag, n_questions=50):
    """ Find and collect the frequently asked questions and relevant answers from stackoverflow.com. The function returns

    :param str url: URL = 'https://stackoverflow.com/questions'
    :param str tag: (!StackOverflow tags only!)
    :param int n_questions: number of questions
    :return: dataframe with questions, summary, link and list of answers.
    :rtype: pd.DataFrame
    """

    simple_list = [[]]

    for page in range(1, ceil(n_questions/PAGE_SIZE) + 1):
        page_url = f"{url}/tagged/{tag}?tab=votes&page={page}&pagesize={PAGE_SIZE}"

        page_request = requests.get(page_url)
        soup = BeautifulSoup(page_request.text, "html.parser")

        # Extracting questions and links
        link_href = soup.select("a.question-hyperlink")
        questions = [question.text.strip() for question in link_href]  # questions list
        href_tags = [url[:-10] + tag['href'] for tag in link_href]  # links list

        # Extracting additional information for question (summary)
        summary_divs = soup.select("div.excerpt")
        summaries = [summary_div.text.strip() for summary_div in summary_divs]  # summaries list

        # Creating a list with all the data
        for i in range(1, len(questions)-1):
            try:
                answer_lst = get_answer(href_tags[i])
                simple_list.append([questions[i], summaries[i], href_tags[i], answer_lst])
            except requests.exceptions.ConnectionError as connection_error:
                print(connection_error)
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


if __name__ == '__main__':
    # main()
    test_scrap()



