from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, URL


class QuickAddForm(FlaskForm):
    url = StringField('YouTube URL', validators=[DataRequired(), Length(min=28, max=43), URL()])
    submit = SubmitField('Add Video')
