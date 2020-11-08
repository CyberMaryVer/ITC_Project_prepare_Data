from scraper import *
import argparse
import os

OBJECT_MAP = {'SO': StackOverflowScraper(), 'MATH': MathematicsScraper(), 'UBUNTU': AskUbuntuScraper()}


def main():
    """ The main function of the program """

    parser = argparse.ArgumentParser(description='Performs a scraping on a web page of the Stack Exchange network saving the information of the questions in a csv file')
    parser.add_argument('-t', '--tag', type=str, help='the tag to specify the topic of the search. If it is not specified, it will search within the general FAQ')
    parser.add_argument('-w', '--where', choices=OBJECT_MAP.keys(), default='SO', type=str,
                        help=f'the target website. -SO: {StackOverflowScraper.DOMAIN}   -MATH: {MathematicsScraper.DOMAIN}   -UBUNTU: {AskUbuntuScraper.DOMAIN}')
    parser.add_argument('-d', '--directory', default='results', type=str,
                        help='the directory path where the results will be saved. If it does not exist, it will be created')
    parser.add_argument('-b', '--begin', default=1, type=int, help='the page number to start the search')
    parser.add_argument('-l', '--limit', default=1000, type=int, help='the maximum number of questions to retrieve')
    parser.add_argument('-v', '--verbose', action='store_true',  help='determines if the program execution is displayed by CLI')

    args = parser.parse_args()
    directory = args.directory

    if not os.path.isdir(directory):
        os.makedirs(directory)

    scrapper = OBJECT_MAP[args.where]
    scrapper.get_faq(tag=args.tag, start_page=1, verbose=True, limit=args.limit, dir=directory)


if __name__ == '__main__':
    main()
