import requests
from bs4 import BeautifulSoup


class StackExchangeScrapper:

    def __init__(self, domain):
        self.domain = domain

    def get_question_details(self, question_id):
        question_url = self.__question_url(question_id)
        page = requests.get(question_url)

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

        print(question_url)
        print('PAGE')
        print(title)
        print(asked)
        print(active)
        print(viewed)
        print(len(post_layout_containers))
        print(answer_count)

        self.__get_post_data(post_layout_containers[0])

    def __question_url(self, question_id):
        return f'{self.domain}/questions/{question_id}'

    @staticmethod
    def __get_post_data(post_layout_container):
        vote_cell_container = post_layout_container.find('div', class_='votecell')
        vote_count = vote_cell_container.find('div', class_='js-vote-count')['data-value']
        bookmark_count = vote_cell_container.find('div', class_='js-bookmark-count')['data-value']

        post_cell_container = post_layout_container.find('div', class_='postcell')
        tags = [tag.text for tag in post_cell_container.find_all('a', class_='post-tag')]

        owner_tag = post_cell_container.find('div', class_='owner').find('div', class_='user-details')
        owner_name = owner_tag.a.text
        owner_id = owner_tag.a['href']

        edited_tag = post_cell_container.find('div', class_='post-signature grid--cell').find('div', class_='user-details')
        edited_time = post_cell_container.find('span', class_='relativetime')['title']
        edited_name = edited_tag.a.text
        edited_id = edited_tag.a['href']

        print(vote_count)
        print(bookmark_count)
        print(tags)
        print(owner_name)
        print(owner_id)
        print(edited_time)
        print(edited_name)
        print(edited_id)

        return 'hola'


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
