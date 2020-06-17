from . import api
from flask import jsonify, request, current_app, url_for
from ..models import User, Costs, Groups, CostGroup
from flask_login import current_user, login_required
from main_app import db
from ..users.email import send_mail


@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/users/register', methods=['POST'])
def register():

    user = User.from_json(request.json)

    db.session.add(user)
    db.session.commit()

    token = user.generate_reset_token()
    send_mail(user.email, 'Confirm Your Account',
              'confirm', user=user, token=token)

    return jsonify(user.to_json()), 201


@api.route('/users/update', methods=['PUT'])
@login_required
def update_user():
    user = current_user

    user.username = request.json.get('username')
    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_json())
