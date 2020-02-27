from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table , Column , Integer ,String ,Text , ForeignKey , Boolean
from sqlalchemy.orm import relationship

base = declarative_base()


class User(base):
    __tablename__ = 'tbl-users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(120) , nullable=False)
    phone_number = Column(String(120) , nullable = True )

    # def __init__(self , username , password):
        # self.username = username
        # self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

class Grade(base):
    __tablename__ = 'tbl-grades'
    id = Column(Integer , primary_key = True)
    title = Column(String(80) , nullable = False)
    description = Column(String(120) , nullable=True)
    # lessons = relationship('Lesson' , back_populates='grade')
    count_of_lessons = Column(Integer , nullable = False)
    number = Column(Integer , nullable = False)
    # lessons = relationship('Lesson')

class Lesson(base):
    __tablename__ = 'tbl-lessons'
    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    # grade_id = Column(Integer , ForeignKey('tbl-grades.id') , nullable = False)
    description = Column(String(120) , nullable=True)
    number = Column(Integer , nullable = False)

    # grade = relationship('Grade' , back_populates='lessons')
    questions = relationship('Question' , back_populates='lesson')

    def __repr__(self):
        return '<lesson %r>' % self.title

class Question(base):
    __tablename__ = 'tbl-questions'
    id = Column(Integer , primary_key = True)
    # lesson_id = Column(Integer ,  ForeignKey('tbl-lessons.id') , nullable = False , server_default = '1')
    grade_number = Column(Integer , nullable = False)
    lesson_id = Column(Integer ,  ForeignKey('tbl-lessons.id') , nullable = False)
    question_text = Column(String(80) , nullable = False)
    definition = Column(String(200))
    question_number = Column(Integer , nullable = False)

    # Grade = relationship('Grade' , back_populates='questions')
    lesson = relationship('Lesson' , back_populates='questions')
    tests = relationship('Test', secondary='association' , back_populates='questions')

    def __init__(self , question_text , definition ):
        self.question_text = question_text
        self.definition = definition

class Configuration(base):
    __tablename__ = 'tbl-configuration'
    id = Column(Integer , primary_key = True)
    last_version = Column(String(80) , nullable = False)

class Test(base):
    __tablename__ = 'tbl-tests'
    id = Column(Integer , primary_key = True)
    title = Column(String(80), nullable=False)
    user_id = Column(Integer , nullable = False)
    question_count = Column(Integer , nullable = False)
    current_question = Column(Integer , nullable = False)
    correct_answers = Column(Integer , nullable = False)
    lesson_id = Column(Integer , nullable = True)

    questions = relationship('Question' , secondary='association' , back_populates='tests')

# association_table = Table('association', base.metadata,
#     Column('tbl-questions.id', Integer, ForeignKey(Test.id)),
#     Column('tbl-tests.id', Integer, ForeignKey(Question.id))
# )

class Link(base):
   __tablename__ = 'association'
   question_id = Column(Integer,ForeignKey('tbl-tests.id'), primary_key = True)
   test_id = Column(Integer,ForeignKey('tbl-questions.id'), primary_key = True)
