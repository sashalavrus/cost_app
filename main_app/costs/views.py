from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import current_user, login_required
from main_app import db
from main_app.models import Costs, User, WhoOwesWhom
from main_app.costs.form import CostForm, CostUpdate, CostHandler
from main_app.costs.cost_handler import cost_handle
costs = Blueprint('costs', __name__)


@costs.route('/all_costs')
def all():
    costs_all = Costs.query.all()

    return render_template('costs.html', costs=costs_all)


@costs.route('/create_cost', methods=['GET', 'POST'])
@login_required
def create():
    form = CostForm()

    if form.validate_on_submit():

        cost = Costs(cost_title=form.description.data,
                     spent_money=float(form.spent_money.data),
                     who_spent=current_user.id,
                     group_id=form.group_id.data)

        db.session.add(cost)
        db.session.commit()
        flash('Thank you for yours costs')
        return redirect(url_for('costs.all'))

    return render_template('create_cost.html', form=form)


@costs.route('/<int:costs_id>/update', methods=['GET', 'POST'])
@login_required
def update(costs_id):
    cost = Costs.query.get_or_404(costs_id)

    if cost.cost.author != current_user:
        abort(403)

    form = CostUpdate()

    if form.validate_on_submit():
        cost.cost_title = form.description.data
        cost.spent_money = form.spent_money.data

        db.session.commit()
        flash('Costs update')
        return redirect(url_for('cost.costs'))

    elif request.method == 'GET':

        form.description.data = cost.cost_title
        form.spent_money.data = cost.spent_money

    return render_template('create_cost.html', form=form)


@costs.route('/<int:costs_id>')
def cost(costs_id):
    view_cost = Costs.query.get_or_404(costs_id)
    return render_template('view_cost.html',
                           cost_title=view_cost.cost_title,
                           date=view_cost.purchase_time,
                           view_cost=view_cost)


@costs.route('/cost_handler')
@login_required
def cost_handler():

    form = CostHandler()

    if form.validate_on_submit():
        user_list = []
        users = User.query.filter(User.group.group_id == form.group_id.data).all()
        data = cost_handler(users)
        for u in users:
            user_list.append(u.id)
        for u in user_list:
            who_whom = None
            copy_list = user_list.copy()
            copy_list.remove(u)
            for i in copy_list:
                who_whom = WhoOwesWhom(who=u, whom=i,
                                       group_id=form.group_id.data)
                db.session.add(who_whom)
                db.session.commit()
        for d in data:
            who_whom = WhoOwesWhom.query.filter_by(who=d[0], whom=d[1]).first_or_404()
            who_whom.debt_amount(d[2])
        return redirect(url_for('costs.final', group_id =form.group_id.data))

    return render_template('cost_handler.html', form=form)


@costs.route('/cost_finish')
@login_required
def final(group_id):

    who_to_whom = WhoOwesWhom.query.filter_by(group_id=group_id).all()

    return render_template('final_cost.html', who_to_whom=who_to_whom)
