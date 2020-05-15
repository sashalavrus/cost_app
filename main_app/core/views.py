from flask import render_template, request, url_for
from . import core
from ..models import CostGroup, Needs, Costs
from flask_login import current_user


@core.route('/')
def index():
    if current_user.is_authenticated:

        groups = CostGroup.query.filter_by(user_id=current_user.id).all()
        costs = Costs.query.all()
        return render_template('index.html', groups=groups, costs=costs)
    return render_template('index.html')


@core.route('/info')
def info():
    return render_template('info.html')




