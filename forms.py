from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange

class LibraryForm(FlaskForm):
    title = StringField('Tytuł', validators=[DataRequired(), Length(max=100)])
    year = IntegerField('Rok', validators=[DataRequired(), NumberRange(min=0)])
    description = TextAreaField('Opis', validators=[DataRequired(), Length(max=1000)])
    done = BooleanField('Przeczytane')
