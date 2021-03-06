import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SUPER_USER_STR = "SUPER_USER"
    ADMINISTRATOR_STR = "ADMINISTRATOR"
    USER_STR = "USER"
    REPORT_LIMIT_PER_PAGE = 10
