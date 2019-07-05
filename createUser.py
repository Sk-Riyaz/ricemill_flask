from app.models import Roles, User
from app import db, create_app
from config import Config
import sys


if len(sys.argv) < 2:
    print("Invalid usage. Please provide user password as argument")
    exit()


def create_roles():
    app = create_app(Config)
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    if Roles.query.all():
        return True
    try:
        role_s = Roles(name="SUPER_USER")
        role_a = Roles(name="ADMINISTRATOR")
        role_u = Roles(name="USER")
        db.session.add(role_s)
        db.session.add(role_a)
        db.session.add(role_u)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        return False
    return True


def create_super_user():
    app = create_app(Config)
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    if User.query.all():
        return True
    try:
        role_id = Roles.query.filter_by(name="SUPER_USER").first()
        user = User(username="super", email="super@mymail.com",
                    role_id=role_id.id, active=True)
        user.set_password(sys.argv[1])
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return False
    return True


# create_super()
create_roles()
create_super_user()
