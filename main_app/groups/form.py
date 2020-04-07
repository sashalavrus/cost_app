from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class CreateGroup(FlaskForm):

    name = StringField('Group Name', validators=[DataRequired()])
    submit = SubmitField('Crete')


class CreateCostGroup(FlaskForm):

    user = IntegerField('User id', validators=[DataRequired()])
    group_name = IntegerField('Group Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


