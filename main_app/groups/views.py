from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from main_app import db
from main_app.models import User, Costs, Needs, Comments, Groups, CostGroup
from main_app.groups.form import CreateCostGroup, CreateGroup
from . import groups


@groups.route('/create_group', methods=['GET', 'POST'])
@login_required
def create_group():

    form = CreateGroup()

    if form.validate_on_submit():

        group = Groups(name=form.name.data)

        db.session.add(group)
        db.session.commit()
        flash('Thank you for register new Group')
        return redirect(url_for('core.index'))

    return render_template('create_group.html', form=form)


@groups.route('/create_cost_group', methods=['GET', 'POST'])
@login_required
def create_cost_group():

    form = CreateCostGroup()

    if form.validate_on_submit():

        group = CostGroup(user_id=form.user.data, group_id=form.group_name.data)

        db.session.add(group)
        db.session.commit()
        flash('Thank you for register new Group')
        return redirect(url_for('core.index'))

    return render_template('create_cost_group.html', form=form)
