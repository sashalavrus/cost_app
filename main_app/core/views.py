from flask import render_template, request, Blueprint

core = Blueprint('core', __name__, template_folder='/home/laviss/Workspace/final_project/main_app/templates')


@core.route('/')
def index():
    return render_template('index.html')

@core.route('/info')
def info():
    return render_template('info.html')




