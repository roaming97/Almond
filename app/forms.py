from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, PasswordField, TextField
from wtforms.validators import DataRequired, Length, URL, Regexp


# Form fields

def YouTubeURLField(require: bool = True):
    val = [
        DataRequired(),
        Length(min=28, max=43),
        URL(message=''),
        Regexp(r'^((?:https?:)?\/\/)?((?:www|m)\.)?'
               r'((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|'
               r'embed\/|v\/)?)([\w\-]+)(\S+)?$', message='Not a YouTube URL.')
    ] if require else None
    return StringField('YouTube URL', validators=val)


# Forms

class AuthForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class SearchForm(FlaskForm):
    query = StringField('', validators=[DataRequired()])
    submit = SubmitField('Search')


class QuickAddForm(FlaskForm):
    url = YouTubeURLField()
    submit = SubmitField('Add Video')


class ManualAddForm(FlaskForm):
    title = TextField('Video title', validators=[DataRequired()])
    stream = FileField('Video file', validators=[FileRequired(), FileAllowed(['mp4', 'webm'])])
    thumbnail = FileField('Thumbnail file', validators=[FileAllowed(['jpg', 'png'])])
    profile_picture = FileField('Profile picture file', validators=[FileAllowed(['jpg', 'png'])])
    url = YouTubeURLField(require=False)
    author = StringField('Author', validators=[DataRequired(), Length(max=60)])
    author_url = StringField('Author URL', validators=[Length(max=60)])
    description = TextField('Description')
    views = StringField('Archived views', validators=[Length(max=25)])
    date = StringField('Original upload date (yyyymmdd)', validators=[Length(max=8)])
    likes = StringField('Likes', validators=[Length(max=12)])
    dislikes = StringField('Dislikes', validators=[Length(max=12)])
    subscribers = StringField('Archived subscribers', validators=[Length(max=12)])
    thumbnail_url = StringField('Thumbnail source', validators=[Length(max=50)])
    submit = SubmitField('Add Video')
