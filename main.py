from scrap_so import *
from scraper import *
import argparse
import os


def main():
    """ The main function of the program """

    parser = argparse.ArgumentParser(description='Scrape StackExchange')
    parser.add_argument('-s', '--search', default='python', type=str, help='search tag')
    parser.add_argument('-w', '--where', default='SO', type=str,
                        help='website: [SO: stackoverflow, MATH: math.stackexchange: , UBUNTU: ask.ubuntu]')
    parser.add_argument('-d', '--directory', default='./Downloads/', type=str, help='save directory')
    args = parser.parse_args()
    directory = args.directory
    website = args.where
    tag = args.search
    if not os.path.isdir(directory):
        os.makedirs(directory)

    if website == 'MATH':
        scrapper = MathematicsScraper()
    elif website == 'UBUNTU':
        scrapper = AskUbuntuScraper()
    else:
        scrapper = StackOverflowScraper()

    #test = scrapper.get_question_details(5041008, verbose=True)
    scrapper.get_faq(tag=tag, start_page=2, verbose=True, limit=2, dir=directory)



if __name__ == '__main__':
    main()
