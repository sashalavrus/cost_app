from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CommentForm(FlaskForm):

    text = StringField('Text of Comment', validators=[DataRequired()])
    submit = SubmitField('Post')
