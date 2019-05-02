from flask_wtf import FlaskForm
from wtforms import (IntegerField, FloatField, StringField,
                     SubmitField, DateField, SelectField, TextAreaField,
                     FormField, FieldList)
from wtforms.validators import DataRequired, InputRequired, ValidationError

from app import utilities
from flask_login import current_user


class ChoiceValidator(object):
    def __init__(self, choice=None):
        if not choice:
            choice = "choice"
        self.message = f"Please select a valid {choice}"

    def __call__(self, form, field):
        print(f"Choice: {field.data}, {type(field.data)}")

        if field.data == 0:
            raise ValidationError(self.message)


class PurchaseForm(FlaskForm):
    rst_number = FloatField('RST Number', validators=[
        DataRequired(message="Weight is required"),
        InputRequired(message="Weight is required")
    ])
    weight = FloatField("Weight", validators=[
        DataRequired(message="Weight is required"),
        InputRequired(message="Weight is required")
    ])
    variety = SelectField("Variety", coerce=int, validators=[
        DataRequired(message="Variety is required"),
        InputRequired(message="Variety is required"),
        ChoiceValidator(choice="Variety")]
    )
    agent = SelectField("Agent", coerce=int, validators=[
        DataRequired(message="Agent is required"),
        InputRequired(message="Agent is required"),
        ChoiceValidator(choice="Agent")]
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
    party_name = StringField("Party Name", validators=[
        DataRequired(message="PartyName is required"),
        InputRequired(message="PartyName is required")]
    )
    party_address = TextAreaField("Party Address", validators=[
        DataRequired(message="PartyAddress is required"),
        InputRequired(message="PartyAddress is required")
    ])
    gst_number = StringField("GST Number", validators=[
        DataRequired(message="GST Number is required"),
        InputRequired(message="GST Number is required")]
    )
    vehicle_number = StringField("Vehicle Number", validators=[
        DataRequired(message="Vehicle Number is required"),
        InputRequired(message="Vehicle Number is required")]
    )
    no_of_bags = IntegerField("Number of Bags", validators=[
        DataRequired(message="Number of Bags is required"),
        InputRequired(message="Number of Bags is required")
    ])
    variety = SelectField("Variety", coerce=int, validators=[
        DataRequired(message="Variety is required"),
        InputRequired(message="Variety is required")]
    )
    agent = SelectField("Agent", coerce=int, validators=[
        DataRequired(message="Agent is required"),
        InputRequired(message="Agent is required")]
    )
    quintol = FloatField("Quintol", validators=[
        DataRequired(message="Quintol is required"),
        InputRequired(message="Quintol is required")
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


"""
class PurchaseReportFields(FlaskForm):
    rst_number = FloatField('RST No')
    weight = FloatField("Weight", validators=[
        DataRequired(message="Weight is required"),
        InputRequired(message="Weight is required")
    ])
    variety = SelectField("Variety", coerce=int, validators=[
        DataRequired(message="Variety is required"),
        InputRequired(message="Variety is required"),
        ChoiceValidator(choice="Variety")]
    )
    agent = StringField("Agent", validators=[
        DataRequired(message="Agent is required"),
        InputRequired(message="Agent is required")]
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


class PurchaseReportForm(FlaskForm):
    purchases = FieldList(FormField(PurchaseReportFields))


class SalesReportForm(FlaskForm):
    sales = FieldList(FormField(SalesForm))
"""
