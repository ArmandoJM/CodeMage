# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp

class CodeForm(FlaskForm):
    problem_description = TextAreaField('Problem Description', validators=[
        DataRequired(message='A description is required.'),
        Length(min=10, max=200, message='Description must be between 10 to 200 characters long.'),
        Regexp(r'^[\w\s]+$', message='Description can only contain letters, numbers, and spaces.')
    ])
