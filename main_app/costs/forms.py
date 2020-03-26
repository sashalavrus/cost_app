from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CostForm(FlaskForm):

    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class CostUpdate(FlaskForm):

    description = StringField('Update description', validators=[DataRequired()])
    submit = SubmitField('Submit')
