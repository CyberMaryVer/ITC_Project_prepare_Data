from resources.scraper import *
import _thread
import sys
import argparse
import time
import os

OBJECT_MAP = {'SO': StackOverflowScraper(), 'MATH': MathematicsScraper(), 'UBUNTU': AskUbuntuScraper()}
IS_RUNNING = True


def print_message():
    """ Print the message in Scraping... during a non-verbose run to give the user a visual key """
    global IS_RUNNING

    point_counter = 1
    while IS_RUNNING:
        if point_counter < 4:
            sys.stdout.write('\rScraping' + '.' * point_counter)
            point_counter += 1
        else:
            point_counter = 1
            sys.stdout.write("\r           ")
            sys.stdout.write("\rScraping")
        sys.stdout.flush()
        time.sleep(1)


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

    if not args.verbose:
        _thread.start_new_thread(print_message, ())

    scrapper.get_faq(tag=args.tag, start_page=1, limit=args.limit, verbose=args.verbose, _dir=directory)

    if not args.verbose:
        global IS_RUNNING
        IS_RUNNING = False
        print(f'\rFinished check the {args.directory} directory')

if __name__ == '__main__':
    main()
