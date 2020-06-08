from . import api
from flask import jsonify, request, current_app, url_for
from ..models import User, Costs, Groups, CostGroup, Permission, Needs
from flask_login import current_user, login_required
from main_app import db
from .errors import forbidden
from ..decorators import permission_required

@api.route('/user_groups')
@login_required
def get_user_groups():

    interim_req = CostGroup.query.filter_by(user_id=current_user.id).all()
    result_query = None

    for i in interim_req:
        user_group = db.session.query(Groups).filter_by(id=i.group_id)
        if result_query is None:
            result_query = user_group
        else:
            result_query = result_query.union(user_group)

    return jsonify(result_query)


@api.route('/groups/create', methods=['POST'])
@login_required
@permission_required(Permission.MODERATE)
def create():

    group = Groups.from_json(request.json)

    db.session.add(group)
    db.session.commit()

    return jsonify(group.to_json()), 201
##To be

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
