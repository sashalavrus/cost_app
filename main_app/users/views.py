from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from main_app import db
from main_app.models import User, Permission, Role
from main_app.users.form import RegistrationForm, LoginForm, UpdateUserForm, AdminForm
from main_app.users.picture_handler import add_profile_pic
from . import users
from .email import send_mail
from ..decorators import permission_required


@users.before_app_request
def before_request():
    if current_user.is_authenticated:
        if not current_user.confirmed \
                and request.endpoint \
                and request.endpoint[:6] != 'users.' \
                and request.endpoint != 'users.confirm':
            return redirect(url_for('users.unconfirmed'))


@users.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('core.index'))
    return render_template('unconfirmed.html')


@users.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_mail(current_user.email, 'Confirm Your Account',
              'confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('core.index'))


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        token = user.generate_reset_token()
        send_mail(user.email, 'Confirm Your Account',
                  'confirm', user=user, token=token)
        flash('Thank you for the registration')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)


@users.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('core.index'))
    if current_user.confirm(token):
        flash('Your account is confirmed, Thank you!!!')
    else:
        flash('Confirmation link is invalid, or occur unexpected error')

    return redirect(url_for('core.index'))


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash('Log in is Done')

            return redirect(url_for('core.index'))

    return render_template('login.html', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))


@users.route('/change_account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserForm()

    if form.validate_on_submit():

        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User account updated')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', form=form, profile_image=profile_image)


@users.route('/<username>')
def info(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_info.html', user=user)


@users.route('/admin_panel', methods=['GET', 'POST'])
@login_required
@permission_required(Permission.ADMIN)
def admin_panel():

    form = AdminForm()
    roles = Role.query.all()

    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first_or_404()

        user.role_id = request.form.get('role_id')
        db.session.commit()

        return redirect(url_for('users.admin_panel'))

    return render_template('admin_panel.html', form=form, roles=roles)
