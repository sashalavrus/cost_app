from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import current_user, login_required
from main_app import db
from main_app.models import User, Costs, Needs, CostGroup, Groups
from main_app.needs.form import NeedsForm
from . import needs


@needs.route('/create_need', methods=['GET', 'POST'])
@login_required
def create():

    form = NeedsForm()
    user_groups = {}
    all_cost_groups = CostGroup.query.filter_by(user_id=current_user.id)
    for g in all_cost_groups:
        group = Groups.query.get_or_404(g.group_id)
        user_groups.update(({g.group_id: group.name}))

    if form.validate_on_submit():

        group_id = request.values.get('group_id')
        needs_obj = Needs(text=form.text.data, group_id=group_id)
        needs_obj.who_posted  = current_user.id
        db.session.add(needs_obj)
        db.session.commit()
        flash('Thank you for adding new needs')
        return redirect(url_for('core.index'))

    return render_template('create_needs.html', form=form, user_groups=user_groups)


@needs.route('/view_all')
@login_required
def view_all():

    user_groups = CostGroup.query.filter_by(user_id=current_user.id).all()
    result_query = None
    for g in user_groups:
        need_of_group = db.session.query(Needs).filter_by(group_id=g.group_id)
        if result_query is None:
            result_query = need_of_group
        else:
            result_query = result_query.union(need_of_group)

    return render_template('view_needs.html', result_query=result_query)


@needs.route('/update_need')
@login_required
def update():

    updated_need_id = request.args.get('updated_need_id')
    need = Needs.query.get_or_404(updated_need_id)

    if need.author != current_user:
        abort(403)

    form = NeedsForm()

    if form.validate_on_submit():
        need.text = form.text.data

        db.session.commit()
        flash('Needs update')
        return redirect(url_for('costs.all'))

    elif request.method == 'GET':

        form.text.data = need.cost_title

    return render_template('update_needs.html', form=form)


@needs.route('/delete_need')
@login_required
def delete():

    deleted_need_id = request.args.get('deleted_need_id')
    deleted_need = Needs.query.get_or_404(deleted_need_id)

    if (current_user == deleted_need.author) or current_user.is_administrator:
        db.session.delete(deleted_need)
        db.session.commit()
    else:
        abort(403)
    return redirect(url_for('core.index'))
