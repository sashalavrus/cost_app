from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from main_app import db
from main_app.models import User, Costs, Needs, Comments, CostGroup
from main_app.needs.form import NeedsForm
from . import needs


@needs.route('/create', methods=['GET', 'POST'])
@login_required
def create():

    form = NeedsForm()

    if request.method == 'GET':
        groups = CostGroup.query.filter_by(user_id=current_user.id).all()

        return render_template('create_needs.html', form=form, groups=groups)

    elif form.validate_on_submit():

        need_group = request.values.get('group_choice')
        needs_obj = Needs(description=form.description.data, group_id=need_group)

        db.session.add(needs_obj)
        db.session.commit()
        flash('Thank you for adding new needs')
        return redirect(url_for('core.index'))

    return render_template('create_needs.html', form=form)


@needs.route('/view_all')
@login_required
def view_all():

    all_needs = Needs.query.all()

    return render_template('view_needs.html', all_needs=all_needs)
