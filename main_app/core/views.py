from flask import render_template, request, jsonify
from . import core
from ..models import CostGroup, Costs
from flask_login import current_user


@core.route('/')
def index():
    if current_user.is_authenticated:

        groups = CostGroup.query.filter_by(user_id=current_user.id).all()
        costs = Costs.query.all()
        return render_template('index.html', groups=groups, costs=costs)
    return render_template('index.html')


@core.route('/info')
def info():
    return render_template('info.html')


@core.app_errorhandler(403)
def forbidden(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'forbidden'})
        response.status_code = 403
        return response
    return render_template('error_pages/403.html'), 403


@core.app_errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return render_template('error_pages/404.html'), 404


@core.app_errorhandler(500)
def internal_server_error(e):

    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'internal server error'})
        response.status_code = 500
        return response
    return render_template('error_pages/500.html'), 500
