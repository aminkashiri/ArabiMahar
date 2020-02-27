from flask import current_app
from database import dbSession , engine
from models import User , Grade , Lesson , Question , Configuration
# from scripts.questions import dictionary_of_questions

#1
# not worked:
# connection = engine.connect()
# connection.execute( Grade.insert() , [
#     {'title':'haftom' , 'description':'smallest' },
#     {'title':'hashtom' , 'description':'largest' }
# ])

#working
#2
# dbSession.execute('INSERT INTO `tbl-grades`(id ,title , description) VALUES '+
#     '( 7 , "هفتم" , ""),'+
#     '( 8 , "هشتم" , ""),'+
#     '( 9 , "نهم" , ""),'+
#     '( 10, "دهم" , ""),'+
#     '( 11, "یازدهم" , ""),'+
#     '( 12, "دوازدهم" , "")'
# )

#3
# dbSession.execute('INSERT INTO `tbl-grades`(number , title , description , count_of_lessons) VALUES '+
#     '( 7 , "هفتم" , "" , 0),'+
#     '( 8 , "هشتم" , "" , 0 ),'+
#     '( 9 , "نهم" , "" , 0),'+
#     '( 10, "دهم" , "" , 8),'+
#     '( 11, "یازدهم" , "" ,0 ),'+
#     '( 12, "دوازدهم" , "" , 0)'
# )
# dbSession.execute('INSERT INTO `tbl-lessons`(title , description , number) VALUES '+
#     '("درس اول" ,  "" , 1),'+
#     '("درس دوم" ,  "" , 2),'+
#     '("درس سوم" ,  "" , 3),'+
#     '("درس چهارم"  , "" , 4),'+
#     '("درس پنجم" , "" , 5),'+
#     '("درس ششم" ,  "" , 6),'+
#     '("درس هفتم" , "" , 7),'+
#     '("درس هشتم" , "" , 8),'+
#     '("درس نهم" ,  "" , 9),'+
#     '("درس دهم" ,  "" , 10)'
# )

# dbSession.commit()

#4
# with current_app.open_resource('scripts/insert_questions_script.sql') as f:
#         dbSession.execute(f.read().decode('utf8'))
#         dbSession.commit()

# dbSession.commit()
# with current_app.open_resource('scripts/initializeData.sql') as f:
#         table = f.read().decode('utf8').split(';')
#         f.close()
#         for t in table:
#                 t = t + ';'
#                 dbSession.execute(t)
#                 dbSession.commit()
#         dbSession.commit()
# with current_app.open_resource('scripts/initialize.sql') as f:
#         table = f.read().decode('utf8').split(';')
#         f.close()
#         for t in table:
#                 t = t + ';'
#                 dbSession.execute(t)
#                 dbSession.commit()
#         dbSession.commit()

with current_app.open_resource('scripts/initialize.sql') as f:
        table = f.read().decode('utf8').split(';')
        f.close()
        for t in table:
                t = t + ';'
                dbSession.execute(t)
                dbSession.commit()
        dbSession.commit()

# print(result.lenght)

# print(grade7.title)
# print(type(grade7.lessons[0]))

# result = dbSession.query(Grade).order_by('id').all()
# for i in range(7,13):
#     grade = result[i-7]
#     # print(len(grade.lessons))
#     for j in range(0,len(grade.lessons)):
#         lesson = grade.lessons[j]
#         # print(dictionary_of_questions['grade'+str(i)]['lesson'+str(j+1)])
#         # print(i,j)
#         try:
#             for word,meaning in dictionary_of_questions['grade'+str(i)]['lesson'+str(j+1)].items():
#                 lesson.questions.append(Question( word , meaning  ))
#                 # print(lesson.id)
#         except KeyError:
#             pass
    
dbSession.commit()

# dbSession.execute('INSERT INTO `tbl-question`(lesson_id , question_text , definition) VALUES '+
#     '( 1 , "نحن" , "ما"),'+
#     '(  , "فاکهت" , "میوه"),'+
#     '( , "کلب" , "سگ"),'+
#     '( , "رجل" , "مرد"),'+
#     '( , "امراه" , "زن"),'+
#     '( , "سیاره" , "ماشین"),'+
#     '( , "شجره" , "درخت"),'+
#     '( , "نحل" , "زنبور عسل"),'+
# )
# dbSession.

# result = dbSession.query(Grade).all()
# for grade in result:
#     for lesson in grade.lessons:
#         print(lesson.title)