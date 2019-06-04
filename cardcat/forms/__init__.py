from flask_wtf import FlaskForm
from wtforms import StringField, SelectField


class ChargeForm(FlaskForm):
    person = SelectField('Person', choices=[
        ('Anthony', 'anthony'),
        ('Ting', 'ting'),
    ])
    category = SelectField()