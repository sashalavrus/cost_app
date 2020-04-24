from flask import Blueprint

core = Blueprint('core', __name__, template_folder='/home/laviss/Workspace/final_project/main_app/templates')

from . import views
from main_app.models import Permission


@core.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)

