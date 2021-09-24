from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class QuickAddForm(FlaskForm):
    url = StringField('YouTube URL', validators=[DataRequired(), Length(min=28, max=43)])
    submit = SubmitField('Add Video')
