from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, URL, Regexp


class AuthForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class QuickAddForm(FlaskForm):
    url = StringField('YouTube URL', validators=[
        DataRequired(),
        Length(min=28, max=43),
        URL(message=''),
        Regexp(r'^((?:https?:)?\/\/)?((?:www|m)\.)?'
               r'((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|'
               r'embed\/|v\/)?)([\w\-]+)(\S+)?$', message='Not a YouTube URL.')
    ])
    submit = SubmitField('Add Video')
