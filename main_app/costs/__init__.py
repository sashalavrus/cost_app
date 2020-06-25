from flask import Blueprint


costs = Blueprint('costs', __name__)

from . import views
from ..models import Permission


@costs.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
