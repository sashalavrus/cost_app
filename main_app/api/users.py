from . import api
from flask import jsonify, request, g
from ..models import User
from main_app import db
from ..users.email import send_mail
from sqlalchemy.exc import IntegrityError


@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/users/register', methods=['POST'])
def register():

    user = User.from_json(request.json)
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        return jsonify({'Username or Email is already exist'})

    token = user.generate_reset_token()
    send_mail(user.email, 'Confirm Your Account',
              'confirm', user=user, token=token)

    return jsonify(user.to_json()), 201


@api.route('/users/self', methods=['PUT'])
def update_user():
    user = g.current_user

    user.username = request.json.get('username')
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        return jsonify({'massage': 'This Username is already used'})

    return jsonify(user.to_json())


@api.route('/users/self', methods=['GET'])
def get_self_info():
    user = g.current_user

    return jsonify(user.to_json())
