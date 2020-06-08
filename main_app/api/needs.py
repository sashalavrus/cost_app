from . import api
from flask import jsonify, request, current_app, url_for
from ..models import User, Costs, Groups, CostGroup, Permission, Needs
from flask_login import current_user, login_required
from main_app import db
from .errors import forbidden


@api.route('/needs/user')
@login_required
def view_user_needs():

    needs = Needs.query.filter_by(who_posted=current_user.id).all()

    return jsonify(needs.to_json()), 200


@api.route('/needs/user_groups')
@login_required
def view_user_group_needs():

    group_id = request.json.get('group_id')

    group_needs = Needs.query.filter_by(group_id=group_id).all()

    return jsonify(group_needs.to_json()), 200


@api.route('/needs/create', methods=['POST'])
@login_required
def create():

    need = Needs.from_json(request.json)
    need.who_posted = current_user.id

    db.session.add(need)
    db.session.commit()

    return jsonify(need.to_json()), 201


@api.route('/needs/delete/<int:id>', methods=['DELETE'])
@login_required
def delete(id):

    need = Needs.query.get_or_404(id)

    if current_user.id == need.who_posted or \
            current_user.can(Permission.MODERATE):

        db.session.delete(need)
        db.session.commit()

        return jsonify({'massage': 'Need is deleted'})

    else:

        return forbidden('Access denied')


@api.route('/needs/update/<int:id>', methods=['PUT'])
@login_required
def update(id):

    need = Needs.query.get_or_404(id)

    if need.current_user == need.author or \
            current_user.can(Permission.MODERATE):

        need.description = request.json.get('description')
        need.group_id = request.json.get('group_id')

        db.session.commit()

        return jsonify(need.to_json()), {"massage": 'successfully updated'}

    return forbidden('Access denied')
