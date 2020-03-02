import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from flask import current_app
import click
from flask.cli import with_appcontext


# db = sqlalchemy()
# engine = create_engine(os.environ['SQLALCHEMY-URL']) // key error
# engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/logindb' , echo = True)
# engine = create_engine('mysql+mysqlconnector://root:root@localhost:3306/arabimahar')

host = os.environ.get('AMMAR_DB_HOST' , 'localhost:3306')
db_name = os.environ.get('AMMAR_DB_NAME' , 'arabimahar')
mysql_user = os.environ.get('AMMAR_DB_USERNAME' , 'root')
mysql_password = os.environ.get('AMMAR_DB_PASSWORD' , 'root')

engine_addr = 'mysql+mysqlconnector://{}:{}@{}/{}'.format(mysql_user,mysql_password,host,db_name)
engine = create_engine(engine_addr)

# print(os.environ.get('ALLUSERSPROFILE' , 'localhost'))
# print(dict(os.environ))


dbSession = scoped_session(sessionmaker(bind=engine))
# print(Session)
# print(type(Session))

# dbSession = Session()
def shutdown_session():
    # for i in  range(10):
    #         print("hey")
    dbSession.remove()

def init_app(app):
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/logindb' #working one
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlclient://root:root@localhost:3306/logindb'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+Flask-MySQLdb://root:root@localhost:3306/logindb'
    app.cli.add_command(init_db_command)

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('initialized DB')

def init_db():
    # from models import base
    # # base.metadata.drop_all(engine)
    # base.metadata.create_all(engine)
    # import dbScript
    # import scripts.inse

#current:
    import dbScript

# def init_app(app):
#     mysql.init_app(app)
#     app.teardown_appcontext(close_db)
