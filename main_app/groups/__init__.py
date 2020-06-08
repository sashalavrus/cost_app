from flask import Blueprint


groups = Blueprint('groups', __name__)

from . import views
from ..models import Permission


@groups.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
