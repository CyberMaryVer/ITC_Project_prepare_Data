import wikipedia
import warnings
from resources.element import ShallowTagDetail

warnings.filterwarnings('ignore')


def parse_wiki(tag):
    definition = wikipedia.summary(tag)
    page = wikipedia.page(tag)
    page = page.pageid
    list_of_tags = wikipedia.search(tag)
    list_of_tags = ', '.join(list_of_tags)

    return ShallowTagDetail(name=tag, definition=definition, page=page, list_of_tags=list_of_tags)


def test_func():
    print(parse_wiki('klklkl'))


if __name__ == '__main__':
    test_func()
