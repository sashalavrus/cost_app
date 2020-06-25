from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class NeedsForm(FlaskForm):

    text = StringField('Description of needs', validators=[DataRequired()])

    submit = SubmitField('Submit')
