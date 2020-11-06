class Question:
    SRT_TEMPLATE = 'Question: {id}\n'\
        'title: {title}\n'\
        'asked: {asked}\n' \
        'active: {active}\n'\
        'viewed: {viewed}\n'\
        '\n'\
        'vote_count: {vote_count}\n'\
        'bookmark_count: {bookmark_count}\n'\
        'tags: {tags}\n'\
        '\n'\
        'owner_id: {owner_id}\n'\
        'owner_name: {owner_name}\n'\
        'edited_time: {edited_time}\n'\
        'edited_id: {edited_id}\n'\
        'edited_name: {edited_name}\n'\
        '\n'\
        'Answers: {answer_count}'

    def __init__(self, question_id, title, **kwargs):
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
        self.edited_time = kwargs.get('edited_time')
        self.edited_name = kwargs.get('edited_name')
        self.edited_id = kwargs.get('edited_id')
        self.answers = []

    def add_answer(self, answer):
        self.answers.append(answer)

    def __str__(self):
        if len(self.answers) > 0:
            return (self.SRT_TEMPLATE + '\n{formatted_answers}')\
                .format(**self.__dict__, formatted_answers='\n'.join(map(lambda answer: str(answer), self.answers)))
        return self.SRT_TEMPLATE.format(**self.__dict__)

    def __repr__(self):
        return self.__str__()


class Answer:

    def __init__(self, user_time, user_id, user_name, vote_count, **kwargs):
        self.user_time = user_time
        self.user_id = user_id
        self.user_name = user_name
        self.vote_count = vote_count
        self.edit_time = kwargs.get('edit_time')
        self.edit_id = kwargs.get('edit_id')
        self.edit_name = kwargs.get('edit_name')

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()
