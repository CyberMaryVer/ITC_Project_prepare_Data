import requests
from element import Question, Answer
from bs4 import BeautifulSoup
import pandas as pd
import datetime


class StackExchangeScraper:
    """ The StackExchangeScraper class provides methods
    for scraping questions from the Stack Exchange network.

    :param str domain: A domain belonging to the Stack Exchange network
    """
    ID_INDEX = 2
    FAULT_TOLERANCE = 5

    def __init__(self, domain):
        """ Constructor method

        :param str domain: A domain belonging to the Stack Exchange network
        """
        self.domain = domain

    def get_faq(self, tag=None, start_page=1, limit=100, verbose=False, _dir='results'):
        """ Find and collect the frequently asked questions and relevant answers

        :param str tag: (Optional) A tag specify the category of the search
        :param int start_page: The page where the search is started
        :param int limit: The number of questions to retrieve
        :param bool verbose: Specifies whether the program execution should be printed in the terminal
        :param str _dir: The directory path where the results will be saved
        """
        questions_counter = 0
        attempts = 0

        # Creating an empty list for data
        to_csv = []

        if verbose:
            print(f'Getting the FAQ for {self.domain}', end="")
            if tag is not None:
                print(f' for Tag: {tag}')
            print('\n')

        while questions_counter < limit:
            faq_url = self.__faq_url(tag, start_page)

            if verbose:
                print(f'Requesting page {start_page}: ', faq_url, end=' ')

            page = requests.get(faq_url)

            if verbose:
                print('--> Status: ', page.status_code)

            if page.status_code != requests.codes.ok:
                if attempts >= self.FAULT_TOLERANCE:
                    assert Exception(f'There is a problem with URL: {faq_url} STATUS: {page.status_code}')
                attempts += 1
                continue

            soup = BeautifulSoup(page.content, 'html.parser')

            question_summaries = soup.find_all('div', class_='question-summary')

            for question_summary in question_summaries:
                try:
                    question_url = question_summary.find('a', class_="question-hyperlink")['href']
                    question_id = question_url.split('/')[self.ID_INDEX]

                    if verbose:
                        print(f'{questions_counter + 1}. ', end="")

                    question_details = self.get_question_details(question_id, verbose=verbose)

                    # Creating a list with all the data
                    to_csv.append([question_details.title, question_details.asked, question_details.active,
                                   question_details.viewed, question_details.vote_count,
                                   question_details.bookmark_count, question_details.tags, question_details.owner_id,
                                   question_details.owner_name, question_details.edited_time,
                                   question_details.edited_id, question_details.edited_name,
                                   question_details.answer_count, question_details.answers])

                    if verbose:
                        print(question_details)
                        print('-' * 100, end='\n\n')

                except AssertionError as assertion_error:
                    if verbose:
                        print('Invalid status code')
                        print(assertion_error)
                        print('Moving to the next question')
                    pass
                else:
                    questions_counter += 1
                    if questions_counter == limit:
                        break

            start_page += 1

        if verbose:
            print(f'Scraping finished {questions_counter} questions collected')

        # saving in .csv
        df = pd.DataFrame(to_csv, columns=['question title', 'asked', 'active',
                           'viewed', 'vote_count', 'bookmark_count', 'tags', 'owner_id',
                           'owner_name', 'edited_time','edited_id', 'edited_name',
                           'answer_count', 'answers'])
        df.to_csv(_dir + f'/{self.__class__.__name__.lower()}_{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}.csv')

    def get_question_details(self, question_id, verbose=False):
        """ Retrieve the detailed information of a specific question and and its answers

        :param int|str question_id: The id of a question
        :param bool verbose: Specifies whether the program execution should be printed in the terminal
        :return: A Question object with the info
        :rtype: Question
        """
        question_url = self.__question_url(question_id)

        if verbose:
            print(f'Requesting question {question_id}: ', question_url, end=' ')

        page = requests.get(question_url)

        if verbose:
            print('--> Status: ', page.status_code)

        assert page.status_code == requests.codes.ok

        soup = BeautifulSoup(page.content, 'html.parser')

        question_header = soup.find(id='question-header')
        title = question_header.a.text

        post_details_container = question_header.find_next_sibling('div')
        asked = post_details_container.find('time')['datetime']
        active = post_details_container.find('a', href='?lastactivity')['title']
        viewed = post_details_container.find_all('div')[-1]['title']

        answer_count = soup.find(id='answers-header').find('h2')['data-answercount']

        post_layout_containers = soup.find_all('div', class_='post-layout')
        post_layout_question_container = post_layout_containers.pop(0)  # Because the first post is the question

        question_post_properties = self.__get_post_data(post_layout_question_container, is_question=True)

        question = Question(question_id, title, asked=asked, active=active, viewed=viewed, answer_count=answer_count,
                            **question_post_properties)

        for post_layout_container in post_layout_containers:
            try:
                answer_post_properties = self.__get_post_data(post_layout_container)
                question.add_answer(Answer(**answer_post_properties))
            except AttributeError as attribute_error:
                if verbose:
                    print('Incompatible format')
                    print(attribute_error)
                pass
            except TypeError as type_error:
                if verbose:
                    print('Missing Attributes for Answer Object')
                    print(type_error)
                pass

        return question

    def __question_url(self, question_id):
        """ Generate the url for a specific question

        :param int|str question_id: The id of a question
        :return: The url for a specific question
        :rtype: str
        """
        return f'{self.domain}/questions/{question_id}'

    def __faq_url(self, tag=None, page=1, page_size=50):
        """ Generate the url for a question list page (faq)

        :param str tag: (Optional) A tag specify the category of the search
        :param int page: The specific page for the pagination system
        :param int page_size: The number of questions to return
        :return: The url for a specific question list (fqq)
        :rtype: str
        """
        url = f'{self.domain}/questions'
        if tag is not None:
            url += f'/tagged/{tag}'
        return url + f'?tab=votes&page={page}&pagesize={page_size}'

    @staticmethod
    def __get_post_data(post_layout_container, is_question=False):
        """ Extract the data from a post container

        :param bs4.element.Tag post_layout_container: The post container
        :param bool is_question: Determine if the post should be treated as a question or as an answer
        :return: A dict with the info of the post
        :rtype: dict
        """
        post_properties = {}

        vote_cell_container = post_layout_container.find('div', class_='votecell')
        post_properties['vote_count'] = vote_cell_container.find('div', class_='js-vote-count')['data-value']

        if is_question:
            post_properties['bookmark_count'] = vote_cell_container.find('div', class_='js-bookmark-count')[
                'data-value']

            post_cell_container = post_layout_container.find('div', class_='postcell')
            post_properties['tags'] = [tag.text for tag in post_cell_container.find_all('a', class_='post-tag')]

            owner_container = post_cell_container.find('div', class_='owner')
            if owner_container is not None and owner_container.find('div', class_='user-details') is not None and owner_container.find('div', class_='user-details').a is not None:
                post_properties['owner_name'] = owner_container.find('div', class_='user-details').a.text
                post_properties['owner_id'] = owner_container.find('div', class_='user-details').a['href']
            else:
                post_properties['owner_name'] = None
                post_properties['owner_id'] = None

            edited_container = post_cell_container.find('div', class_='post-signature grid--cell')
            if edited_container is not None:
                edited_container = edited_container.find('div', class_='user-details')
                post_properties['edited_time'] = post_cell_container.find('span', class_='relativetime')['title']

                if edited_container.a is not None:
                    post_properties['edited_name'] = edited_container.a.text
                    post_properties['edited_id'] = edited_container.a['href']
                else:
                    post_properties['edited_name'] = post_properties['owner_name']
                    post_properties['edited_id'] = post_properties['owner_id']

        else:
            user_info_containers = post_layout_container.find('div', class_='answercell').find_all('div',
                                                                                                   class_='user-info')

            answered_container = user_info_containers.pop()  # Because the last one is the user who answered the question

            relative_time_tag = answered_container.find('span', class_='relativetime')
            post_properties['user_time'] = relative_time_tag['title'] if relative_time_tag is not None else None

            user_details_tag = post_properties['user_name'] = answered_container.find('div', class_='user-details')

            if user_details_tag is not None and user_details_tag.a is not None:
                post_properties['user_name'] = user_details_tag.a.text
                post_properties['user_id'] = user_details_tag.a['href']
            else:
                post_properties['user_name'] = None
                post_properties['user_id'] = None

            for user_info_container in user_info_containers:
                post_properties['edit_time'] = user_info_container.find('span', class_='relativetime')['title']

                user_details_container = user_info_container.find('div', class_='user-details')
                if user_details_container.a is not None:
                    post_properties['edit_name'] = user_details_container.a.text
                    post_properties['edit_id'] = user_details_container.a['href']
                else:
                    post_properties['edit_name'] = post_properties['user_name']
                    post_properties['edit_id'] = post_properties['user_id']

        return post_properties


class StackOverflowScraper(StackExchangeScraper):
    """ A Stack Overflow wrapper for the StackExchangeScraper class """
    DOMAIN = 'https://stackoverflow.com'

    def __init__(self):
        """ Constructor method """
        super().__init__(domain=self.DOMAIN)


class AskUbuntuScraper(StackExchangeScraper):
    """ A Ask Ubuntu wrapper for the StackExchangeScraper class """
    DOMAIN = 'https://askubuntu.com'

    def __init__(self):
        """ Constructor method """
        super().__init__(domain=self.DOMAIN)


class MathematicsScraper(StackExchangeScraper):
    """ A Mathematics wrapper for the StackExchangeScraper class """
    DOMAIN = 'https://math.stackexchange.com'

    def __init__(self):
        """ Constructor method """
        super().__init__(domain=self.DOMAIN)
