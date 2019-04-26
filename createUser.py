from app.models import Roles, User
from app import db
def create_super():
    #role = Roles.query.filter_by(name="").first()
    try:
        role = Roles(name="ADMINISTRATOR")
        db.session.add(role)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
    
    try:
        role_id = Roles.query.filter_by(name="SUPER_USER").first()
        user = User(username="super",
                #password_hash=generate_password_hash("super"),
                email="super@mymail.com", role_id=role_id.id)
        user.set_password("super")
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
create_super()
