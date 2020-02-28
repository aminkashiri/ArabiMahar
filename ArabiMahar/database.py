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

host = os.environ.get('db_host' , 'localhost')
db_name = os.environ.get('db_name' , 'arabimahar')
mysql_user = os.environ.get('db_host' , 'root')
mysql_password = os.environ.get('db_host' , 'root')

engine_addr = 'mysql+mysqlconnector://{}:{}@{}:3306/{}'.format(mysql_user,mysql_password,host,db_name)
engine = create_engine(engine_addr)

# print(os.environ.get('ALLUSERSPROFILE' , 'localhost'))
# print(dict(os.environ))


Session = scoped_session(sessionmaker(bind=engine))
dbSession = Session()


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
