from scraper import *


def test():
    """ A tiny test for the program usage

    Retrieve the top 1000 favorite questions in the stack overflow under the Python tag.
    Show the execution in the CLI and save the results in the directory ./test
    """
    try:
        StackOverflowScraper().get_faq(tag='python', start_page=1, verbose=True, limit=1000, _dir='./test')
    except KeyboardInterrupt:
        print('Program finish by the user')

if __name__ == '__main__':
    test()
