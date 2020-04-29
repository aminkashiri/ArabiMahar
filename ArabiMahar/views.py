import functools
from flask import (
    Blueprint , flash , g , redirect , render_template , request , session , url_for ,jsonify
)
from werkzeug.security import check_password_hash , generate_password_hash
from models import User , Grade , Lesson ,Question ,Configuration ,Test
from database import dbSession
from sqlalchemy.sql.expression import func
# from wsgi import app

authentication_blueprint = Blueprint('verification' , __name__ , url_prefix='/verification')
grades_blueprint = Blueprint('grades' , __name__ , url_prefix='/grades')
mobile_initialize_blueprint = Blueprint('mobileInitialize' , __name__ , url_prefix='/initialize')
update_blueprint = Blueprint('update' , __name__ , url_prefix='/update')
test_blueprint = Blueprint('test' , __name__ , url_prefix='/test')



def is_logined():
    if g.user is None:
        return False
    else:
        return True

@update_blueprint.route('/add' , methods = ['POST','GET'])
def add():
    if request.method == 'POST':
        b = True
        user_name = request.form['user_name']
        city = request.form['city']
        province = request.form['province']
        buy_number = request.form['buy_number']
        error = None
        if not city:
            error = 'لطفا شهرت رو وارد کن'
        elif not province:
            error = 'لطفا استانت رو وارد کن'
        elif not buy_number:
            error = 'کدوم درس رو بخرم؟'
        elif buy_number > 4:
            error = 'تو خرید درس مشکل داشتیم'
        else:
            user = dbSession.query(User).filter_by(username = user_name).first()
            if user is None:
                error = 'انگار ثبت نام نکردی'
        if error is None:
            user.city = city
            user.province = province
            
            if buy_number == 4:
                user.bought = 7
            else:
                user.bought = user.bought + buy_number
            dbSession.commit()
            b = False

        return_dict = {'error' : b , 'errorMessage' : error}
        return return_dict


                


@authentication_blueprint.route('/register' , methods=['POST' , 'GET'])
def register():
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        email = request.form['email']
        phone_number = str(request.form['phone_number'])
        error = None
        if not user_name:
            error = 'Please enter user name'
        elif not password:
            error = 'Please enter password'
        elif not email:
            error = 'Please enter your e-mail'
        elif not phone_number:
            error = 'Please enter your phone number'
        else :
            user = dbSession.query(User).filter_by(username=user_name).first()
            if user is not None:
                error = 'username is taken'
            # cursor.execute('SELECT ID FROM users WHERE username = %s' ,(user_name,))
            # a = cursor.fetchone()
            # if a is not None:
        if error is None:
            # cursor.execute('INSERT INTO users (username,password) VALUES(%s,%s)' , (user_name,generate_password_hash(password) ,) )
            # dbSession.add(User(username = user_name,password = generate_password_hash(password) , email = email , phone_number = phone_number))
            dbSession.add(User(username = user_name,password = generate_password_hash(password) , phone_number = phone_number))
            dbSession.commit()
            return redirect(url_for('verification.login'))
        else:
            flash(error)
    return render_template('auth/register.html')

@authentication_blueprint.route('/mregister' , methods=['POST' , 'GET'])
def mregister():
    b= True
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        try:
            phone_number = request.form['phone_number']
        except:
            print('no phone number')
        error = None
        if not user_name:
            error = 'لطفا اسمتو وارد کن'
        elif not password:
            error = 'لطفا رمزتو وارد کن'
        else :
            user =  dbSession.query(User).filter_by(username=user_name).first()
            if user is not None:
                error = 'اسمت تکراریه'
        if error is None:
            user = User( username = user_name , password = generate_password_hash(password) , phone_number = phone_number , bought = 0)
            dbSession.add(user)
            # user_server_id = dbSession.query(User).filter_by(id=user_server_id).first()
            dbSession.commit()
            b = False

    returnDict = { "error" : b , "errorMessage" : error , 'user_server_id' : user.id }
    return returnDict

@authentication_blueprint.route('/login' , methods=['POST' , 'GET'])
def login():
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        user =  dbSession.query(User).filter_by(username=user_name).first()
        error = None

        if user is None:
            error = 'Username not founded'
        elif not check_password_hash(user.password, password):
            error = 'Password incorrect'
        if error is None :
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('verification.index'))
        flash(error)

    return render_template('auth/login.html')

@authentication_blueprint.route('/mlogin' , methods=['POST' , 'GET'])
def mlogin():
    b = True
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        user = dbSession.query(User).filter_by(username=user_name).first()
        error = None

        if user is None:
            error = 'Username not founded'
        elif not check_password_hash(user.password, password):
            error = 'Password incorrect'
        if error is None :
            b = False

    returnDict = { "error" : b , "errorMessage" : error , "server_user_id" : user.id }
    return returnDict

@authentication_blueprint.route('/index' , methods=['POST','GET'])
def index():
    if is_logined():
        user_id = session.get('user_id')
        user =  dbSession.query(User).filter_by(id=user_id).first()
        # cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
        # user = cursor.fetchone()
        return render_template('auth/index.html' , user =  user)
    return redirect(url_for('verification.login'))
    

@authentication_blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None :
         g.user = None
    else:
        g.user =  dbSession.query(User).filter_by(id = user_id).first()
        # print(g.user)

@authentication_blueprint.route('/logout' , methods = ['POST' , 'GET'])
def logout():
    session.clear()
    return redirect(url_for('verification.register'))


@grades_blueprint.route('/')
def grades_page():
    if is_logined():
        result = dbSession.query(Grade.title).order_by(Grade.id).all()
        return render_template('navigation/grades.html' , grade_names = result)
    else:
        return redirect(url_for('verification.login'))
    
@grades_blueprint.route('/<int:grade_number>')
def lessons_page(grade_number):
    if is_logined():
        result = dbSession.query(Lesson.title).filter(Lesson.grade_id==grade_number).order_by(Lesson.id).all()
        return render_template('navigation/lessons.html' , grade_number = grade_number , lesson_names = result)
    else:
        return redirect(url_for('verification.login'))


@grades_blueprint.route('/<int:grade_number>/lessons/<int:lesson_number>')
def test_page(grade_number , lesson_number):
    if is_logined():
        # def rowdict(row):
        #     d = {}
        #     for column in row:
        #         d[column.question_text] = column.definition

        #     return d
        
        grade = dbSession.query(Grade).filter_by(id=grade_number).first()
        try:
            lesson = grade.lessons[lesson_number-1]
            test = Test(user_id = g.user.id ,title = lesson.title , question_count = len(lesson.questions) , current_question = 0 , correct_answers = 0 , lesson_id = lesson.id)
            test.questions = lesson.questions
            question = test.questions[0]
            dbSession.add(test)
            dbSession.commit()
            return render_template('test_page/test_page.html' ,test_title = test.title , test_id = test.id , question = question)
            # return render_template('test_page/test_page.html' , test_id = test.id , question = question)
        except IndexError as e:
            print(e)
            return render_template('test_page/no_question.html')
    else:
        return redirect(url_for('verification.login'))

@test_blueprint.route('/<int:testid>/<string:response>')
def answer(testid , response):
    if is_logined():
        test = dbSession.query(Test).filter(Test.id == testid).first()
        test.current_question = test.current_question+1
        if response == 'True':
            test.correct_answers = test.correct_answers+1
            dbSession.commit()
        if test.current_question< test.question_count:
            question  = test.questions[test.current_question]
            return render_template('test_page/test_page.html' , test_title = test.title , test_id = testid , question = question)
        else:
            corrects = test.correct_answers
            all_count = test.question_count
            lesson_id = test.lesson_id
            grade_id = dbSession.query(Lesson).filter(Lesson.id == lesson_id).first().grade_id
            return render_template('test_page/result_page.html' ,test = test , corrects = corrects , all_count = all_count ,grade_id = grade_id , lesson_id = lesson_id)
    else :
        return redirect(url_for('verification.login'))


@grades_blueprint.route('/<int:grade_number>/lessons/first_term_random')
def first_term_random(grade_number):
    if is_logined():
        grade = dbSession.query(Grade).filter(Grade.id == grade_number).first()
        first_lesson_id = grade.lessons[0].id
        size = int(len(grade.lessons)/2)
        questions_list = dbSession.query(Question).filter(Question.lesson_id>=first_lesson_id, Question.lesson_id<= (first_lesson_id+size)).order_by(func.random()).limit(10).all()
        test = Test(user_id = g.user.id , title = 'مرور نیم سال اول' , question_count = len(questions_list) , current_question = 0 , correct_answers = 0 )
        test.questions = questions_list
        dbSession.add(test)
        dbSession.commit()
        question = questions_list[0]
        return render_template('test_page/test_page.html' ,test_title = test.title , test_id = test.id , question = question)
    else:
        return redirect(url_for('verification.login'))

@grades_blueprint.route('/<int:grade_number>/lessons/second_term_random')
def second_term_random(grade_number):
    if is_logined():
        grade = dbSession.query(Grade).filter(Grade.id == grade_number).first()
        first_lesson_id = grade.lessons[0].lesson_id
        size = int(len(grade.lessons)/2)
        questions_list = dbSession.query(Question).filter(Question.lesson_id>=first_lesson_id, Question.lesson_id<= (first_lesson_id+size)).order_by(func.random()).limit(10).all()
        return render_template('test_page/test_page.html' , questions = questions_list)
    else:
        return redirect(url_for('verification.login'))

@mobile_initialize_blueprint.route('')
def initialize():
    # grades_list = dbSession.query(Grade).all()
    # grades = list()
    # for grade in grades_list:
    #     grade_dict = dict()
    #     grade_dict['id'] = grade.id
    #     grade_dict['title'] = grade.title
    #     grade_dict['description'] = grade.description
    #     lessons_list = list()
    #     for lesson in grade.lessons:
    #         lesson_dict = dict()
    #         lesson_dict['id'] = lesson.id
    #         lesson_dict['grade_id'] = lesson.id
    #         lesson_dict['title'] = lesson.title
    #         lesson_dict['description'] = lesson.description
    #         questions_list = list()
    #         for question in questions_list:
    #             question_dict = dict()
    #             question_dict['id'] = question.id
    #             question_dict['question_text'] = question.question_text
    #             question_dict['lesson_id'] = question.lesson_id
    #             question_dict['definition'] = question.definition
    #             questions_list.append(question_dict)
    #         lesson_dict['questions'] = questions_list
    #         lessons_list.append(lesson_dict)
        
    #     grade_dict['lessons'] = lessons_list
    #     grades.append(grade_dict)

    # return { 'grades' : grades}

#current:
    # grades_list = dbSession.query(Grade).all()
    # grades = list()
    # lessons = list()
    # questions = list()
    # for grade in grades_list:
    #     grade_dict = dict()
    #     grade_dict['id'] = grade.id
    #     grade_dict['title'] = grade.title
    #     grade_dict['count_of_lessons'] = len(grade.lessons)
    #     grade_dict['description'] = grade.description
    #     grade_dict['number'] = grade.number
    #     grades.append(grade_dict)
    #     for lesson in grade.lessons:
    #         lesson_dict = dict()
    #         lesson_dict['id'] = lesson.id
    #         lesson_dict['title'] = lesson.title
    #         # lesson_dict['grade_id'] = lesson.
    #         lesson_dict['description'] = lesson.description
    #         lesson_dict['number'] = lesson.number
    #         lessons.append(lesson_dict)
    #         for question in lesson.questions:
    #             question_dict = dict()
    #             question_dict['id'] = question.id
    #             question_dict['lesson_id'] = question.lesson_id
    #             question_dict['grade_number'] = question.grade_number
    #             question_dict['question_text'] = question.question_text
    #             question_dict['definition'] = question.definition
    #             question_dict['number'] = question.number
    #             questions.append(question_dict)
    
    grades_list = dbSession.query(Grade).all()
    grades = list()
    lessons = list()
    questions = list()
    for grade in grades_list:
        grade_dict = dict()
        grade_dict['id'] = grade.id
        grade_dict['title'] = grade.title
        grade_dict['count_of_lessons'] = grade.count_of_lessons
        grade_dict['description'] = grade.description
        grade_dict['number'] = grade.number
        grades.append(grade_dict)

    lessons_list = dbSession.query(Lesson).all()
    for lesson in lessons_list:
        lesson_dict = dict()
        lesson_dict['id'] = lesson.id
        lesson_dict['title'] = lesson.title
        # lesson_dict['grade_id'] = lesson.
        lesson_dict['description'] = lesson.description
        lesson_dict['number'] = lesson.number
        lessons.append(lesson_dict)

    questions_list = dbSession.query(Question).all()
    for question in questions_list:
        question_dict = dict()
        question_dict['id'] = question.id
        question_dict['lesson_id'] = question.lesson_id
        question_dict['grade_number'] = question.grade_number
        question_dict['question_text'] = question.question_text
        question_dict['definition'] = question.definition
        question_dict['number'] = question.question_number
        questions.append(question_dict)
        
    print(grades)
    print(lessons)
    print(questions)
    return { "grades" : grades , "lessons" : lessons , "questions" : questions}
    # return render_template('test_page/test_page.html' , questions = questions)

