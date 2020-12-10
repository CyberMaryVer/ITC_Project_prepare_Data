class ShallowQuestion:
    """ The question class contains the information
    of a Stack Exchange question.

    :param str question_id: Question id
    :param str title: The title of the question
    """
    SRT_TEMPLATE = 'Question: {id}\n' \
                   'title: {title}\n' \
                   'asked: {asked}\n' \
                   'active: {active}\n' \
                   'viewed: {viewed}\n' \
                   '\n' \
                   'vote_count: {vote_count}\n' \
                   'bookmark_count: {bookmark_count}\n' \
                   'tags: {tags}\n' \
                   '\n' \
                   'owner_id: {owner_id}\n' \
                   'owner_name: {owner_name}\n' \
                   'edited_time: {edited_time}\n' \
                   'edited_id: {edited_id}\n' \
                   'edited_name: {edited_name}\n' \
                   '\n' \
                   'Answers: {answer_count}'

    def __init__(self, question_id, title, **kwargs):
        """ Constructor method

        :param str question_id: Question id
        :param str title: The title of the question
        :param dict **kwargs: All other optional parameters
        """
        self.id = question_id
        self.title = title
        self.asked = kwargs.get('asked')
        self.active = kwargs.get('active')
        self.viewed = kwargs.get('viewed')
        self.answer_count = kwargs.get('answer_count')
        self.owner_id = kwargs.get('owner_id')
        self.owner_name = kwargs.get('owner_name')
        self.vote_count = kwargs.get('vote_count')
        self.bookmark_count = kwargs.get('bookmark_count')
        self.tags = kwargs.get('tags')
        self.tags_details = []
        self.edited_time = kwargs.get('edited_time')
        self.edited_name = kwargs.get('edited_name')
        self.edited_id = kwargs.get('edited_id')
        self.answers = []

    def add_answer(self, answer):
        """ Add an Answer Object to the answer list

        :param ShallowAnswer answer: An answer object
        """
        self.answers.append(answer)

    def __str__(self):
        """ Convert the Question object converted to a string

        :return: The Question object converted to a string
        :rtype: str
        """
        if len(self.answers) > 0:
            return (self.SRT_TEMPLATE + '\n{formatted_answers}') \
                .format(**self.__dict__, formatted_answers='\n'.join(map(lambda answer: str(answer), self.answers)))
        return self.SRT_TEMPLATE.format(**self.__dict__)

    def __repr__(self):
        """ Compute the official string representation of an Question object

        :return: The Question object converted to a string
        :rtype: str
        """
        return self.__str__()


class ShallowAnswer:

    def __init__(self, user_time, user_id, user_name, vote_count, **kwargs):
        """ Constructor method

        :param str user_time: The publication date of the answer
        :param str user_id: The id of the user who answered
        :param str user_name: The name of the user who answered
        :param str vote_count: The answer vote score
        :param dict **kwargs: All other optional parameters
        """
        self.user_time = user_time
        self.user_id = user_id
        self.user_name = user_name
        self.vote_count = vote_count
        self.edit_time = kwargs.get('edit_time')
        self.edit_id = kwargs.get('edit_id')
        self.edit_name = kwargs.get('edit_name')

    def __str__(self):
        """ Convert the Answer object converted to a string

        :return: The Answer object converted to a string
        :rtype: str
        """
        return str(self.__dict__)

    def __repr__(self):
        """ Compute the official string representation of an Answer object

        :return: The Answer object converted to a string
        :rtype: str
        """
        return self.__str__()


class ShallowTagDetail:
    """ The TagDetails class contains the information
        of a tag obtained from the wikipedia

        :param str name: tag name
        :param str definition: tag definition
        :param str page: tag page
        :param str list_of_tags: list of related tags
        """
    def __init__(self, name, definition, page, list_of_tags):
        """ Constructor method

        :param str name: tag name
        :param str definition: tag definition
        :param str page: tag page
        :param str list_of_tags: list of related tags
        """
        self.name = name
        self.definition = definition
        self.page = page
        self.list_of_tags = list_of_tags

    def __str__(self):
        """ Convert the ShallowTagDetail object to a string

        :return: The ShallowTagDetail object converted to a string
        :rtype: str
        """
        return str(self.__dict__)

    def __repr__(self):
        """ Compute the official string representation of an ShallowTagDetail object

        :return: The ShallowTagDetail object converted to a string
        :rtype: str
        """
        return self.__str__()