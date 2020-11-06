class Question:
    def __init__(self, question_id, title, **kwargs):
        self.id = question_id
        self.title = title
        self.asked = kwargs.get('asked')
        self.active = kwargs.get('active')
        self.viewed = kwargs.get('viewed')
        self.answer_count = kwargs.get('owner_name')
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


class Answer:
    def __init__(self, user_time, user_id, user_name, vote_count, **kwargs):
        self.user_time = user_time
        self.user_id = user_id
        self.user_name = user_name
        self.vote_count = vote_count
        self.edit_time = kwargs.get('edit_time')
        self.edit_id = kwargs.get('edit_id')
        self.edit_name = kwargs.get('edit_name')
