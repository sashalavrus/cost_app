from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import  DataRequired
from main_app.models import Needs


class NeedsForm(FlaskForm):

    cost_name = StringField('Name of Cost', validators=[DataRequired()])
    spent_money = FloatField('Amount of spent money', validators=[DataRequired()])
    submit = SubmitField('Submit')


class  CostUpdate(FlaskForm):

    cost_name = StringField('Name Update', validators=[DataRequired()])
    spent_money = FloatField('update amount', validators=[DataRequired()])
    submit = SubmitField('Submit')