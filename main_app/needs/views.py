from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from main_app import db
from main_app.models import User, Costs, Needs, Comments
from main_app.needs.forms import NeedsForm
from main_app.users.picture_handler import add_profile_pic

needs = Blueprint('needs', __name__)


@needs.route('/create', methods=['GET', 'POST'])
@login_required
def create():

    form = NeedsForm()

    if form.validate_on_submit():

        needs_obj = Needs(description=form.description.data)

        db.session.add(needs_obj)
        db.session.commit()
        flash('Thank you for adding new needs')
        return redirect(url_for('core.index'))

    return render_template('create_needs.html', form=form)


@needs.route('/view_all')
@login_required
def view_all():

    all_needs = Needs.query.all()

    return render_template('view_needs.html', all_needs=all_needs)
