from flask import render_template, request, url_for
from . import core
from ..models import CostGroup, Needs
from flask_login import current_user


@core.route('/')
def index():
    groups = CostGroup.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html')


@core.route('/info')
def info():
    return render_template('info.html')




