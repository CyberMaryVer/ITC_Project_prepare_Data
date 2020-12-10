from sqlalchemy import Table, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Source(Base):
    """ The Source class map the source table
    The source is the stackExchange domain that Question and User belongs
    """
    # noinspection SpellCheckingInspection
    __tablename__ = 'source'

    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(255))

    questions = relationship('Question', back_populates='source')
    users = relationship('User', back_populates='source')


class User(Base):
    """ The User class map the user table
    A user from some stackExchange domain
    """
    # noinspection SpellCheckingInspection
    __tablename__ = 'user'

    id = Column('id', Integer, primary_key=True)

    source_id = Column('source_id', ForeignKey('source.id'))
    source = relationship('Source', back_populates='users')

    stack_exchange_id = Column('stack_exchange_id', Integer)
    username = Column('username', String(255))
    name = Column('name', String(255))

    questions = relationship('Question', foreign_keys='Question.owner_id', back_populates='owner')
    edited_questions = relationship('Question', foreign_keys='Question.editor_id', back_populates='editor')
    answers = relationship('Answer', foreign_keys='Answer.user_id', back_populates='user')
    edited_answers = relationship('Answer',  foreign_keys='Answer.editor_id', back_populates='editor')


question_tag = Table('question_tag', Base.metadata,
                     Column('question_id', Integer, ForeignKey('question.id')),
                     Column('tag_id', Integer, ForeignKey('tag.id'))
                     )


class Tag(Base):
    """ The Tag class map the tag table
    A tag for a question
    """
    # noinspection SpellCheckingInspection
    __tablename__ = 'tag'

    id = Column('id', Integer, primary_key=True)
    name = Column('source', String(255))

    questions = relationship('Question', secondary=question_tag, back_populates='tags')

class Tag_details(Base):
    """ The Tag class map the tag table
    A tag for a question
    """
    # noinspection SpellCheckingInspection
    __tablename__ = 'tag_details'

    id = Column('id', Integer, primary_key=True)
    definition = Column('source', String(255))
    page = Column('source', String(255))
    list_of_tags = Column('source', String(255))

    tags = relationship('Tag', secondary=question_tag, back_populates='tags')


class Question(Base):
    """ The Question class map the question table
    A question from stackExchange domain
    """
    # noinspection SpellCheckingInspection
    __tablename__ = 'question'

    id = Column('id', Integer, primary_key=True)

    source_id = Column('source_id', ForeignKey('source.id'))
    source = relationship('Source', back_populates='questions')

    stack_exchange_id = Column('stack_exchange_id', Integer)
    title = Column('title', String(255))
    asked = Column('asked', DateTime)
    active = Column('active', DateTime)
    viewed = Column('viewed', Integer)
    answer_count = Column('answer_count', Integer)

    owner_id = Column('owner_id', ForeignKey('user.id'))
    owner = relationship('User', foreign_keys=[owner_id], back_populates='questions')

    vote_count = Column('vote_count', Integer)
    bookmark_count = Column('bookmark_count', Integer)

    tags = relationship('Tag', secondary=question_tag, back_populates='questions')

    edited_time = Column('edited_time', DateTime)

    editor_id = Column('editor_id', ForeignKey('user.id'))
    editor = relationship('User', foreign_keys=[editor_id], back_populates='edited_questions')

    answers = relationship('Answer', cascade="all, delete-orphan", back_populates='question')


class Answer(Base):
    """ The Answer class map the answer table
    A answer from stackExchange question
    """
    # noinspection SpellCheckingInspection
    __tablename__ = 'answer'

    id = Column('id', Integer, primary_key=True)

    question_id = Column('question_id', ForeignKey('question.id'))
    question = relationship('Question', back_populates='answers')

    answer_time = Column('answer_time', DateTime)

    user_id = Column('user_id', ForeignKey('user.id'))
    user = relationship('User', foreign_keys=[user_id], back_populates='answers')

    vote_count = Column('vote_count', Integer)

    edit_time = Column('edit_time', DateTime)

    editor_id = Column('editor_id', ForeignKey('user.id'))
    editor = relationship('User', foreign_keys=[editor_id], back_populates='edited_answers')