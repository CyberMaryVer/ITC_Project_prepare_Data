from scrap_so import *
from scraper import *


def main():
    """ The main function of the program """

    # question_url = 'https://stackoverflow.com/questions/5041008/how-to-find-elements-by-class'
    # answers = get_answer(question_url)
    # print(answers)
    #
    # url = 'https://stackoverflow.com/questions'
    # tag = 'python'
    # faq = get_faq(url, tag, 40).head(10)
    # print(faq)
    #
    # faq.to_csv('scrap_so.csv')

    scrapper = StackOverflowScrapper()
    test = scrapper.get_question_details(5041008)



if __name__ == '__main__':
    main()
