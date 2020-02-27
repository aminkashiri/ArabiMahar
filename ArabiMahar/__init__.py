import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from flask import Flask
from flask import render_template

def create_app():
    app = Flask(__name__)
    app.secret_key = 'dev'
    
    from database import init_app
    init_app(app)

    from views import authentication_blueprint , grades_blueprint , mobile_initialize_blueprint , test_blueprint
    app.register_blueprint(authentication_blueprint)
    app.register_blueprint(grades_blueprint)
    app.register_blueprint(mobile_initialize_blueprint)
    app.register_blueprint(test_blueprint)

    @app.route('/')
    def base():
        return render_template('auth/base.html')

    return app
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/logindb'
# db = SQLAlchemy(app)


# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username