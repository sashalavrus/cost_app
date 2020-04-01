from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
from main_app.models import Needs


class NeedsForm(FlaskForm):

    description= StringField('Description of needs', validators=[DataRequired()])

    submit = SubmitField('Submit')


