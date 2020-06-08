from . import api
from flask import jsonify, request, current_app, url_for
from ..models import User, Costs, Groups, CostGroup, Permission
from flask_login import current_user, login_required
from main_app import db
from .errors import forbidden


@api.route('/costs/user')
@login_required
def view_user_costs():

    costs = Costs.query.filter_by(who_spent=current_user.id).all()

    return jsonify(costs.to_json()), 200


@api.route('/costs/user_groups')
@login_required
def view_user_group_cost():

    group_id = request.json.get('group_id')

    group_costs = Costs.query.filter_by(group_id=group_id).all()

    return jsonify(group_costs.to_json()), 200


@api.route('/costs/create', methods=['POST'])
@login_required
def create():

    cost = Costs.from_json(request.json)
    cost.who_spent = current_user.id

    db.session.add(cost)
    db.session.commit()

    return jsonify(cost.to_json()), 201


@api.route('/costs/delete/<int:id>', methods=['DELETE'])
@login_required
def delete(id):

    cost = Costs.query.get_or_404(id)

    if current_user.id == cost.who_spent or \
            current_user.can(Permission.MODERATE):

        db.session.delete(cost)
        db.session.commit()

        return jsonify({'massage': 'Cost is deleted'})

    else:

        return forbidden('Access denied')


@api.route('/cost/update/<int:id>', methods=['PUT'])
@login_required
def update(id):

    cost = Costs.query.get_or_404(id)

    if cost.current_user == cost.author or \
            current_user.can(Permission.MODERATE):

        cost.cost_title = request.json.get('cost_title')
        cost.spent_money = request.json.get('spent_money')
        cost.group_id = request.json.get('group_id')

        db.session.commit()

        return jsonify(cost.to_json()), {"massage": 'successfully updated'}

    return forbidden('Access denied')