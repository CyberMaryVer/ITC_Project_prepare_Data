import re
from resources.element import ShallowQuestion, ShallowAnswer
from db.connection import session
from db.entities import *
from datetime import datetime


def str_to_time(date, fmt='%Y-%m-%d %H:%M:%SZ', default=None):
    try:
        return datetime.strptime(date, fmt)
    except (ValueError, TypeError):
        return default


def extract_id(route):
    try:
        return int(route.split('/')[-2])
    except (AttributeError, IndexError, ValueError):
        return None


def extract_username(route):
    try:
        return route.split('/')[-1]
    except (AttributeError, IndexError):
        return None


class EntityManager:
    def __init__(self, source):
        self.source = source

    def save(self, shallow_question):
        """
        :param ShallowQuestion shallow_question:
        """
        users_to_create = {}

        source = session.query(Source).filter_by(name=self.source).first()

        if source is None:
            source = Source()
            source.name = self.source

        question = session.query(Question).filter_by(source_id=source.id, stack_exchange_id=shallow_question.id).first()

        if question is None:
            question = Question()
            question.source = source
            question.stack_exchange_id = shallow_question.id
        else:
            question.answers = []

        question.title = shallow_question.title
        question.asked = shallow_question.asked

        question.active = str_to_time(shallow_question.active)

        question.viewed = re.findall('\d+', shallow_question.viewed)[0]

        question.answer_count = shallow_question.answer_count

        owner_stack_exchange_id = extract_id(shallow_question.owner_id)
        owner = session.query(User).filter_by(source_id=source.id, stack_exchange_id=owner_stack_exchange_id).first()

        if owner is None:
            owner = User()
            owner.source = source
            owner.stack_exchange_id = owner_stack_exchange_id
            users_to_create[owner.stack_exchange_id] = owner

        owner.username = extract_username(shallow_question.owner_id)
        owner.name = shallow_question.owner_name

        question.owner = owner

        question.vote_count = shallow_question.vote_count
        question.bookmark_count = shallow_question.bookmark_count

        for tag_name in shallow_question.tags:
            tag = session.query(Tag).filter_by(name=tag_name).first()
            if tag is None:
                tag = Tag()
                tag.name = tag_name
            question.tags.append(tag)

        question.edited_time = str_to_time(shallow_question.edited_time)

        editor_stack_exchange_id = extract_id(shallow_question.edited_id)
        editor = session.query(User).filter_by(source_id=source.id, stack_exchange_id=editor_stack_exchange_id).first()

        if editor_stack_exchange_id in users_to_create:
            editor = users_to_create[editor_stack_exchange_id]

        if editor is None:
            editor = User()
            editor.source = source
            editor.stack_exchange_id = editor_stack_exchange_id
            users_to_create[editor.stack_exchange_id] = editor

        editor.username = extract_username(shallow_question.edited_id)
        editor.name = shallow_question.edited_name

        for shallow_answer in shallow_question.answers:
            answer = Answer()

            answer.answer_time = str_to_time(shallow_answer.user_time)

            user_stack_exchange_id = extract_id(shallow_answer.user_id)
            user = session.query(User).filter_by(source_id=source.id, stack_exchange_id=user_stack_exchange_id).first()

            if user_stack_exchange_id in users_to_create:
                user = users_to_create[user_stack_exchange_id]

            if user is None:
                user = User()
                user.source = source
                user.stack_exchange_id = user_stack_exchange_id
                users_to_create[user.stack_exchange_id] = user

            user.username = extract_username(shallow_answer.user_id)
            user.name = shallow_answer.user_name

            answer.user = user

            answer.vote_count = shallow_answer.vote_count

            answer.edit_time = str_to_time(shallow_answer.edit_time)

            question_editor_stack_exchange_id = extract_id(shallow_answer.edit_id)
            question_editor = session.query(User).filter_by(source_id=source.id,
                                                            stack_exchange_id=question_editor_stack_exchange_id).first()

            if question_editor_stack_exchange_id in users_to_create:
                question_editor = users_to_create[question_editor_stack_exchange_id]

            if question_editor is None:
                question_editor = User()
                question_editor.source = source
                question_editor.stack_exchange_id = question_editor_stack_exchange_id
                users_to_create[question_editor.stack_exchange_id] = question_editor

            question_editor.username = extract_username(shallow_answer.edit_id)
            question_editor.name = shallow_answer.edit_name

            question.answers.append(answer)

        if question.id is None:
            session.add(question)
        session.commit()
