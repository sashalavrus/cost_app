from . import api
from flask import jsonify, request, current_app, url_for, g
from ..models import User, Costs, Groups, CostGroup, Permission
from flask_login import current_user, login_required
from main_app import db
from .errors import forbidden
from .auth import auth


@api.route('/costs/<int:id>')
def get_cost(id):

    cost = Costs.query.get_or_404(id)

    return jsonify(cost.to_json()), 200


@api.route('/costs/user')
def view_user_costs():

    costs = Costs.query.filter_by(who_spent=g.current_user.id).all()

    return jsonify({'costs': [cost.to_json() for cost in costs]}), 200


@api.route('/costs/user_groups')
def view_user_group_cost():

    group_id = request.json.get('group_id')

    group_costs = Costs.query.filter_by(group_id=group_id).all()

    return jsonify({'costs': [cost.to_json() for cost in group_costs]}), 200


@api.route('/costs/create', methods=['POST'])
def create_cost():

    cost = Costs.from_json(request.json)
    cost.who_spent = g.current_user.id

    db.session.add(cost)
    db.session.commit()

    return jsonify(cost.to_json()), 201


@api.route('/costs/delete/<int:id>', methods=['DELETE'])
def delete_cost(id):

    cost = Costs.query.get_or_404(id)

    if g.current_user.id == cost.who_spent or \
            g.current_user.can(Permission.MODERATE):

        db.session.delete(cost)
        db.session.commit()

        return jsonify({'massage': 'Cost was deleted'})

    else:

        return forbidden('Access denied')


@api.route('/cost/update/<int:id>', methods=['PUT'])
def update_cost(id):

    cost = Costs.query.get_or_404(id)

    if g.current_user == cost.author or \
            g.current_user.can(Permission.MODERATE):

        cost.cost_title = request.json.get('cost_title')
        cost.spent_money = request.json.get('spent_money')
        cost.group_id = request.json.get('group_id')

        db.session.commit()

        return jsonify(cost.to_json()), {"massage": 'successfully updated'}

    return forbidden('Access denied')
