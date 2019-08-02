from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import (DataRequired, InputRequired,
                                ValidationError, EqualTo)
from flask_login import current_user
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="UserName is required"),
        InputRequired(message="UserName is required")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required"),
        InputRequired(message="Password is required")
    ])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class ChangePasswordForm(FlaskForm):
    prev_password = PasswordField('Old Password', validators=[
        DataRequired(message="Password is required"),
        InputRequired(message="Password is required")
    ])
    new_password = PasswordField('New Password', validators=[
        DataRequired(message="Password is required"),
        InputRequired(message="Password is required")
    ])
    repeat_password = PasswordField('Repeat Password', validators=[
        DataRequired(message="Password is required"),
        EqualTo('new_password')
    ])
    submit = SubmitField('Update')

    @staticmethod
    def validate_prev_password(self, prev_password):
        if current_user.is_anonymous:
            raise ValidationError("Invalid User")
        if not current_user.check_password(prev_password.data):
            raise ValidationError("Incorrect Password")

class ChangeUserPasswordForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="UserName is required"),
        InputRequired(message="UserName is required")
    ])
    new_password = PasswordField('New Password', validators=[
        DataRequired(message="Password is required"),
        InputRequired(message="Password is required")
    ])
    repeat_password = PasswordField('Repeat Password', validators=[
        DataRequired(message="Password is required"),
        EqualTo('new_password')
    ])
    submit = SubmitField('Update')

    @staticmethod
    def validate_username(self, username):
        if current_user.is_anonymous:
            raise ValidationError("Invalid User")
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError(f"User {username.data} doesn't exist")
