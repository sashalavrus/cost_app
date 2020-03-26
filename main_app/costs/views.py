from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import login_user, current_user, logout_user, login_required
from main_app import db
from main_app.models import Costs
from main_app.costs.forms import CostForm, CostUpdate

costs = Blueprint('costs', __name__)


@costs.route('/all_costs')
def all_costs():
    return render_template(url_for('costs.html'))


@costs.route('/create_cost', methods=['GET', 'POST'])
@login_required
def create_cost():
    form = CostForm()

    if form.validate_on_submit():
        cost = Costs(cost_title=form.description.data,
                     spent_money=form.description.data,
                     user_id=current_user.id)

        db.session.add(cost)
        db.session.commit()
        flash('Thank you for yours costs')
        return redirect(url_for('all_costs'))

    return render_template('create_cost.html', form=form)


@costs.route('/<int:costs_id>/update', methods=['GET', 'POST'])
@login_required
def update_cost(costs_id):
    cost = Costs.query.get_or_404(costs_id)

    if cost.cost.author != current_user:
        abort(403)

    form = CostUpdate()

    if form.validate_on_submit():
        cost.cost_title = form.description.data
        cost.spent_money = form.spent_money.data

        db.session.commit()
        flash('Costs update')
        return redirect(url_for('cost.costs', ))




