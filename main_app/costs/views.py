from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from main_app import db
from main_app.models import Costs, User, WhoOwesWhom, CostGroup, Groups
from main_app.costs.form import CostForm, CostUpdate, CostHandler
from main_app.costs.cost_handler import cost_handle
from . import costs


@costs.route('/all_costs', methods=['GET', 'POST'])
@login_required
def all():
    if request.method == 'GET':
        groups = CostGroup.query.filter_by(user_id=current_user.id).all()
        return render_template('costs.html', groups=groups)
    elif request.method == 'POST':
        costs_all = Costs.query.filter_by(group_id=request.values.get('group_choice')).all()
        groups = CostGroup.query.filter_by(user_id=current_user.id).all()
        return render_template('costs.html', costs=costs_all,
                               group_id=request.values.get('group_choice'),
                               groups=groups)


@costs.route('/create_cost', methods=['GET', 'POST'])
@login_required
def create():

    form = CostForm()
    user_groups = {}
    all_cost_groups = CostGroup.query.filter_by(user_id=current_user.id).all()
    for g in all_cost_groups:
        group = Groups.query.get_or_404(g.group_id)
        user_groups.update(({g.group_id: group.name}))
    if form.validate_on_submit():

        group_id = request.form.get('group_id')

        cost = Costs(cost_title=form.description.data,
                     spent_money=float(form.spent_money.data),
                     who_spent=current_user.id,
                     group_id=group_id)

        db.session.add(cost)
        db.session.commit()
        flash('Thank you for yours costs')
        return redirect(url_for('costs.all'))

    return render_template('create_cost.html', form=form, user_groups=user_groups)


@costs.route('/update', methods=['GET', 'POST'])
@login_required
def update():

    updated_cost_id = request.args.get('updated_cost_id')
    cost = Costs.query.get_or_404(updated_cost_id)

    if cost.author != current_user:
        abort(403)

    form = CostUpdate()

    if form.validate_on_submit():
        cost.cost_title = form.description.data
        cost.spent_money = form.spent_money.data

        db.session.commit()
        flash('Costs update')
        return redirect(url_for('costs.all'))

    elif request.method == 'GET':

        form.description.data = cost.cost_title
        form.spent_money.data = cost.spent_money

    return render_template('update_cost.html', form=form)


@costs.route('/delete_cost')
@login_required
def delete():

    deleted_cost_id = request.args.get('deleted_cost_id')
    deleted_cost = Costs.query.get_or_404(deleted_cost_id)

    if (current_user == deleted_cost.author) or current_user.is_administrator:
        db.session.delete(deleted_cost)
        db.session.commit()
    else:
        abort(403)
    return redirect(url_for('core.index'))




@costs.route('/handler')
@login_required
def cost_handler():
    group_id = request.args.get('group_id')
    user_list = []
    users = CostGroup.query.filter(CostGroup.group_id == group_id).all()
    data = cost_handle(users)
    for u in users:
        user_list.append(u.user_id)
    for u in user_list:
        who_whom = None
        copy_list = user_list.copy()
        copy_list.remove(u)
        for i in copy_list:
            who_whom = WhoOwesWhom(who=u, whom=i,
                                   group_id=group_id)
            db.session.add(who_whom)
            db.session.commit()
    for d in data:
        who_whom = WhoOwesWhom.query.filter_by(who=d[0], whom=d[1]).first_or_404()
        who_whom.set_amount(d[2])
        db.session.commit()
    return redirect(url_for('costs.final', group_id=group_id))


@costs.route('/cost_finish')
@login_required
def final():

    group_id = request.args.get('group_id')
    who_to_whom = WhoOwesWhom.query.filter_by(group_id=group_id).all()

    return render_template('final_cost.html', who_to_whom=who_to_whom)
