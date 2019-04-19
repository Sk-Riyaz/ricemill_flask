from flask_wtf import FlaskForm
from wtforms import (BooleanField, IntegerField, FloatField, StringField,
                     PasswordField, SubmitField, DateField, SelectField,
                     TextAreaField, RadioField)
from wtforms.validators import (DataRequired, InputRequired,
                                ValidationError, EqualTo, Email)

from app.models import User


def getVarietyChoices():
    return [
        ("0", "Select"),
        ("1", "NJR"),
        ("2", "1010"),
        ("3", "BPT"),
        ("4", "Nandyala BPT"),
        ("5", "Nandyala Non-BPT")
    ]


def getAgentChoices():
    return [
        ("0", "Select"),
        ("1", "Riyaz"),
        ("2", "Karim")
    ]


class ChoiceValidator(object):
    def __init__(self, choice=None):
        if not choice:
            choice = "choice"
        self.message = f"Please select a valid {choice}"

    def __call__(self, form, field):
        print(f"Choice: {field.data}")

        if field.data == "0":
            raise ValidationError(self.message)


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


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message="UserName is required"),
        InputRequired(message="UserName is required")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required"),
        InputRequired(message="Password is required")
    ])
    password2 = PasswordField('Repeat Password', validators=[
        DataRequired(),
        EqualTo('password')
    ])
    email = StringField('Email', validators=[Email()])
    roles = RadioField('Role', validators=[
        DataRequired(message="Role is required"),
        InputRequired(message="Role is required")],
        choices=getVarietyChoices()
    )

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class AgentForm(FlaskForm):
    name = StringField("Name", validators=[
        DataRequired(message="Name is required"),
        InputRequired(message="Name is required")]
    )
    email = StringField("E-Mail")
    mobile = StringField("Mobile Phone", validators=[
        DataRequired(message="Phone Number is required"),
        InputRequired(message="Phone Number is required")]
    )
    Address = TextAreaField("Address", validators=[
        DataRequired(message="Address is required"),
        InputRequired(message="Address is required")
    ])


class PurchaseForm(FlaskForm):
    rst_number = FloatField('RST No')
    weight = FloatField("Weight", validators=[
        DataRequired(message="Weight is required"),
        InputRequired(message="Weight is required")
    ])
    variety = SelectField("Variety", validators=[
        DataRequired(message="Variety is required"),
        InputRequired(message="Variety is required"),
        ChoiceValidator(choice="Variety")],
        choices=getVarietyChoices()
    )
    agent = SelectField("Agent", validators=[
        DataRequired(message="Agent is required"),
        InputRequired(message="Agent is required"),
        ChoiceValidator(choice="Agent")],
        choices=getAgentChoices()
    )
    moisture = FloatField("Moisture", validators=[
        DataRequired(message="Moisture is required"),
        InputRequired(message="Moisture is required")
    ])
    rate = FloatField("Rate", validators=[
        DataRequired(message="Rate is required"),
        InputRequired(message="Rate is required")
    ])
    date = DateField("Date", format="%d-%m-%Y")
    amount = FloatField("Amount", validators=[
        DataRequired(message="Amount is required"),
        InputRequired(message="Amount is required")
    ])
    submit = SubmitField('Submit')


class SalesForm(FlaskForm):
    party_name = StringField("PartyName", validators=[
        DataRequired(),
        InputRequired()]
    )
    party_address = TextAreaField("PartyAddress", validators=[
        DataRequired(),
        InputRequired()
    ])
    gst_number = StringField("PartyName", validators=[
        DataRequired(),
        InputRequired()]
    )
    vehicle_number = StringField("PartyName", validators=[
        DataRequired(),
        InputRequired()]
    )
    no_of_bags = IntegerField("Number of Bags", validators=[
        DataRequired(),
        InputRequired()
    ])
    variety = SelectField("Agent", validators=[
        DataRequired(),
        InputRequired()],
        choices=getVarietyChoices()
    )
    agent = SelectField("Agent", validators=[
        DataRequired(),
        InputRequired()],
        choices=getAgentChoices()
    )
    quintol = FloatField("Quintol", validators=[
        DataRequired(),
        InputRequired()
    ])
    rate = FloatField("Rate", validators=[
        DataRequired(),
        InputRequired()
    ])
    date = DateField("Date", format="%d-%m-%Y")
    amount = FloatField("Amount", validators=[
        DataRequired(),
        InputRequired()
    ])
    submit = SubmitField('Submit')
