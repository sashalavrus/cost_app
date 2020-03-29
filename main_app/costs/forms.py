from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField
from wtforms.validators import DataRequired


class CostForm(FlaskForm):

    description = StringField('Description', validators=[DataRequired()])
    spent_money = FloatField('Spent money', validators=[DataRequired()])
    submit = SubmitField('Submit')


class CostUpdate(FlaskForm):

    description = StringField('Update description', validators=[DataRequired()])
    spent_money = FloatField('Spent money', validators=[DataRequired()])
    submit = SubmitField('Submit')
