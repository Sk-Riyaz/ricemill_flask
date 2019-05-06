import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    #set SQLALCHEMY_DATABASE_URI =myql://shaik:toor@localhost/ricemill
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    print(SQLALCHEMY_DATABASE_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SUPER_USER_STR = "SUPER_USER"
    ADMINISTRATOR_STR = "ADMINISTRATOR"
    USER_STR = "USER_STR"
