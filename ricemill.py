from app import create_app, db
from app.models import User, Roles

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Roles': Roles}


if __name__ == "__main__":
    app.run(debug=True)
