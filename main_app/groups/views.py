from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from main_app import db
from main_app.models import User, Costs, Needs, Groups, CostGroup, Permission
from main_app.groups.form import CreateCostGroup, CreateGroup
from . import groups
from .. decorators import permission_required, admin_required



@groups.route('/create_group', methods=['GET', 'POST'])
@login_required
def create():

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

        user = User.query.filter_by(username=str(form.user.data)).first_or_404()
        group = Groups.query.filter_by(name=str(form.group_name.data)).first_or_404()
        group_obj = CostGroup(user_id=user.id, group_id=group.id)

        db.session.add(group_obj)
        db.session.commit()
        flash('Thank you for register new Group')
        return redirect(url_for('core.index'))

    return render_template('create_cost_group.html', form=form)


@groups.route('/all_groups')
@login_required
def view_all():

    group_member = CostGroup.query.filter_by(user_id=current_user.id).all()

    return render_template('view_user_group.html', result_query=group_member)


@groups.route('/delete_group')
@login_required
@permission_required(Permission.MODERATE)
def delete():

    deleted_group_id = request.args.get('group_id')

    deleted_group_obj = Groups.query.get(deleted_group_id)

    deleted_costs = Costs.query.filter_by(group_id=deleted_group_id)

    deleted_group_mem = CostGroup.query.filter_by(group_id=deleted_group_id)

    deleted_group_needs = Needs.query.filter_by(group_id=deleted_group_id)

    deleted_needs_comments = None

    for n in deleted_group_needs:
        deleted_comments = db.session.query(Comments).filter_by(post_id=n.id)

        if deleted_needs_comments is None:
            deleted_needs_comments = deleted_comments
        else:
            deleted_needs_comments = deleted_needs_comments.union(deleted_comments)

    for cost in deleted_costs:
        db.session.delete(cost)
        db.session.commit()

    for comment in deleted_needs_comments:
        db.session.delete(comment)
        db.session.commit()

    for need in deleted_group_needs:
        db.session.delete(need)
        db.session.commit()

    for membership in deleted_group_mem:
        db.session.delete(membership)
        db.session.commit()

    db.session.delete(deleted_group_obj)
    db.session.commit()

    return redirect(url_for('groups.view_all'))


@groups.route('/update_group', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.MODERATE)
def update():

    group_id = request.args.get('group_id')
    updated_group = Groups.query.get_or_404(group_id)

    form = CreateGroup()

    if form.validate_on_submit():

        updated_group.name = form.name.data
        db.session.commit()
        flash('Group name has been updated')
        return redirect(url_for('groups.view_all'))

    elif request.method == 'GET':

        form.name.data = updated_group.name

        return render_template('update_group.html', form=form)











