from . import api
from flask import jsonify, request, abort
from ..models import  Costs, Groups, CostGroup, Permission, Needs
from main_app import db
from ..decorators import api_permission_required as permission_required
from sqlalchemy.exc import IntegrityError


@api.route('/groups/<int:id>')
def get_group(id):

    group = Groups.query.get_or_404(id)

    return jsonify(group.to_json()), 200


@api.route('/groups/user/<int:id>')
def get_user_groups(id):

    interim_req = CostGroup.query.filter_by(user_id=id).all()
    result_query = None

    for i in interim_req:
        user_group = db.session.query(Groups).filter_by(id=i.group_id)
        if result_query is None:
            result_query = user_group
        else:
            result_query = result_query.union(user_group)
    if result_query is not None:
        return jsonify({'user_groups': [group.to_json() for group in result_query]}), 200
    return jsonify({'massage': 'user is not in groups jet'})


@api.route('/groups/create', methods=['POST'])
@permission_required(Permission.MODERATE)
def create_group():

    group = Groups.from_json(request.json)
    if group is None or group.name == '':
        abort(400)
    try:
        db.session.add(group)
        db.session.commit()
        return jsonify(group.to_json()), 201
    except IntegrityError:
        return jsonify({'massage': 'This group name already exist'}), 200


@api.route('/groups/membership', methods=['POST'])
@permission_required(Permission.MODERATE)
def create_membership():

    user_membership = CostGroup.from_json(request.json)
    if user_membership is None:
        abort(400)

    db.session.add(user_membership)
    db.session.commit()

    return jsonify(user_membership.to_json()), 201


@api.route('/groups/<int:id>', methods=['DELETE'])
@permission_required(Permission.ADMIN)
def delete_group(id):

    deleted_group = Groups.query.get_or_404(id)
    deleted_costs = Costs.query.filter_by(group_id=id).all()
    deleted_group_mem = CostGroup.query.filter_by(group_id=id).all()
    deleted_needs = Needs.query.filter_by(group_id=id).all()

    for cost in deleted_costs:
        db.session.delete(cost)
        db.session.commit()

    for need in deleted_needs:
        db.session.delete(need)
        db.session.commit()

    for mem in deleted_group_mem:
        db.session.delete(mem)
        db.session.commit()

    db.session.delete(deleted_group)
    db.session.commit()

    return jsonify({'massage': 'Removal was successful'}), 200


@api.route('/groups/membership', methods=['DELETE'])
@permission_required(Permission.MODERATE)
def delete_membership():

    group_members = CostGroup.query.filter_by(
        group_id=request.json.get('group_id')).all()

    deleted_meber = CostGroup.query.filter_by(
        user_id=request.json.get('user_id')).first_or_404()

    db.session.delete(deleted_meber)
    db.session.commit()

    return jsonify({'massage': 'Removal was successful'}), 200


@api.route('/groups/<int:id>', methods=['PUT'])
@permission_required(Permission.MODERATE)
def update_group(id):

    group = Groups.query.get_or_404(id)

    group.name = request.json.get('name')

    db.session.commit()

    return jsonify(group.to_json()), 200
