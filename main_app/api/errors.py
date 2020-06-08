from flask import jsonify
from . import api


def unauthorized(massage):
    response = jsonify({'error': 'unauthorized',
                        'massage': massage})
    response.status_code = 401
    return response


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response
