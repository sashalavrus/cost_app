from flask import Blueprint



needs = Blueprint('needs', __name__)

from . import views
from ..models import Permission


@needs.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)