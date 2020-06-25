from . import api
from flask import jsonify, request, current_app, url_for, g
from ..models import User, Costs, Groups, CostGroup, Permission, Needs
from flask_login import current_user, login_required
from main_app import db
from .errors import forbidden


@api.route('/needs/<int:id>')
def get_need(id):

    need = Needs.query.get_or_404(id)
    memberships = CostGroup.query.filter_by(group_id=need.group_id,
                                            user_id=g.current_user.id).first()

    if memberships is not None or g.current_user.is_administrator():
        return jsonify(need.to_json()), 200

    return forbidden('You are not a member of the group')


@api.route('/needs/self')
def view_user_needs():

    needs = Needs.query.filter_by(who_posted=g.current_user.id).all()

    return jsonify({'needs': [need.to_json() for need in needs]}), 200


@api.route('/needs/group/<int:id>')
def view_user_group_needs(id):


    memberships = CostGroup.query.filter_by(user_id=g.current_user.id,
                                            group_id=id).first()

    if memberships is not None or g.current_user.is_administrator():
        group_needs = Needs.query.filter_by(group_id=id)

        return jsonify({'needs': [need.to_json() for need in group_needs]}), 200

    return forbidden('You are not a member of the group')


@api.route('/needs/create', methods=['POST'])
def create_need():

    text = request.json.get('text')
    group_id = request.json.get('group_id')
    who_posted = g.current_user.id
    memberships = CostGroup.query.filter_by(user_id=who_posted,
                                            group_id=group_id).first()

    if memberships is not None:
        need = Needs(text=text, group_id=group_id,
                     user_id=who_posted)
        db.session.add(need)
        db.session.commit()
        return jsonify(need.to_json()), 201
    return forbidden('You are not member of group')


@api.route('/needs/<int:id>', methods=['DELETE'])
def delete(id):

    need = Needs.query.get_or_404(id)

    if g.current_user.id == need.who_posted or \
            g.current_user.can(Permission.MODERATE):

        db.session.delete(need)
        db.session.commit()

        return jsonify({'massage': 'Need is deleted'})

    else:

        return forbidden('Access denied')


@api.route('/needs/<int:id>', methods=['PUT'])
def update(id):

    need = Needs.query.get_or_404(id)

    if need.who_posted == need.author or \
            g.current_user.can(Permission.ADMIN):

        need.text = request.json.get('text')
        need.group_id = request.json.get('group_id')

        db.session.commit()

        return jsonify(need.to_json()), {"massage": 'successfully updated'}

    return forbidden('Access denied')
