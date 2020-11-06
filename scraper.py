import requests
from element import Question, Answer
from bs4 import BeautifulSoup


class StackExchangeScrapper:

    def __init__(self, domain):
        self.domain = domain

    def get_question_details(self, question_id, verbose=False):
        question_url = self.__question_url(question_id)

        if verbose:
            print('Requesting: ', question_url, end=' ')

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
        return f'{self.domain}/questions/{question_id}'

    @staticmethod
    def __get_post_data(post_layout_container, is_question=False):
        post_properties = {}

        vote_cell_container = post_layout_container.find('div', class_='votecell')
        post_properties['vote_count'] = vote_cell_container.find('div', class_='js-vote-count')['data-value']

        if is_question:
            post_properties['bookmark_count'] = vote_cell_container.find('div', class_='js-bookmark-count')['data-value']

            post_cell_container = post_layout_container.find('div', class_='postcell')
            post_properties['tags'] = [tag.text for tag in post_cell_container.find_all('a', class_='post-tag')]

            owner_container = post_cell_container.find('div', class_='owner').find('div', class_='user-details')
            post_properties['owner_name'] = owner_container.a.text
            post_properties['owner_id'] = owner_container.a['href']

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
            user_info_containers = post_layout_container.find('div', class_='answercell').find_all('div', class_='user-info')

            answered_container = user_info_containers.pop()  # Because the last one is the user who answered the question
            post_properties['user_time'] = answered_container.find('span', class_='relativetime')['title']
            post_properties['user_name'] = answered_container.find('div', class_='user-details').a.text
            post_properties['user_id'] = answered_container.find('div', class_='user-details').a['href']

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


class StackOverflowScrapper(StackExchangeScrapper):
    DOMAIN = 'https://stackoverflow.com'

    def __init__(self):
        super().__init__(domain=self.DOMAIN)

    pass


class AskUbuntuScrapper(StackExchangeScrapper):
    DOMAIN = 'https://askubuntu.com'

    def __init__(self):
        super().__init__(domain=self.DOMAIN)

    pass


class MathematicsScrapper(StackExchangeScrapper):
    DOMAIN = 'https://math.stackexchange.com'

    def __init__(self):
        super().__init__(domain=self.DOMAIN)

    pass
