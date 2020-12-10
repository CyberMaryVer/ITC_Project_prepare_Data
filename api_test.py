import wikipedia
import warnings

warnings.filterwarnings('ignore')


def parse_wiki(tag):
    definition, page, list_of_tags = None, None, None
    try:
        definition = wikipedia.summary(tag)
        page = wikipedia.page(tag)
        list_of_tags = wikipedia.search(tag)
    except wikipedia.exceptions.DisambiguationError as ex:
        print(ex)
    except Exception:
        pass
    return [definition, page, list_of_tags]


def test_func():
    print(parse_wiki('klklkl'))


if __name__ == '__main__':
    test_func()
