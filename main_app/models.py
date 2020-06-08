from main_app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime
from flask import current_app, redirect, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Permission:
    COMMENT = 1
    WRITE = 2
    MODERATE = 4
    ADMIN = 8


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.COMMENT, Permission.WRITE],
            'Moderator': [Permission.COMMENT, Permission.WRITE,
                          Permission.MODERATE],
            'Administrator': [Permission.COMMENT, Permission.WRITE,
                              Permission.MODERATE, Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, index=True, unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    profile_image = db.Column(db.String(128), nullable=False, default='default_profile_img.png')
    costs = db.relationship('Costs', backref='author', lazy=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    needs = db.relationship('Needs', backref='author', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

        if self.role is None:
            if self.email == current_app.config['COSTAPP_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, permissions):
        return self.role.permissions is not None and\
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def __repr__(self):
        return f"Name = {self.username} "

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.commit()
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def to_json(self):
        user_json = {
            'url': url_for('api.get_user', id=self.id, _external=True),
            'username': self.username,
            'role': self.role_id,
            'groups': url_for('api.user_groups', id=self.id, _external=True),
            'costs': url_for('api.user_costs', id=self.id, _external=True),
            'needs': url_for('api.user_needs', id=self.id, _external=True)
        }
        return user_json

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('ascii')


    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    @staticmethod
    def from_json(user_json):
        username = user_json.get('username')
        email = user_json.get('email')
        password_hash = generate_password_hash(
                    user_json.get('password'))
        return User(username, email, password_hash)


class AnonUser(AnonymousUserMixin):

    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


login_manager.anonymous_user = AnonUser


class Costs(db.Model):

    __tablename__ = "costs"

    id = db.Column(db.Integer, primary_key=True)
    cost_title = db.Column(db.String(128), nullable=False)
    spent_money = db.Column(db.Float, nullable=False)
    who_spent = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    purchase_time = db.Column(db.DateTime, default=datetime.now())
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)

    def __init__(self, cost_title, spent_money, who_spent, group_id):
        self.cost_title = cost_title
        self.spent_money = spent_money
        self.who_spent = who_spent
        self.group_id = group_id

    def __repr__(self):
        return f"{self.cost_title} was spent {self.spent_money} UAN " \
               f"at {self.purchase_time.year} {self.purchase_time.month} {self.purchase_time.day}  "

    def to_json(self):
        json_cost = {
            'title': self.cost_title,
            'spent_money': self.spent_money,
            'who_spent': url_for('api.get_user', id=self.who_spent, _external=True),
            'purchase_time': self.purchase_time,
            'group': url_for('api.get_group', id=self.group_id, _external=True)
        }
        return json_cost

    @staticmethod
    def from_json(cost_json):
        cost_title = cost_json.get('cost_title')
        spent_money = cost_json.get('spent_money')
        group_id = cost_json.get('group_id')

        return Costs(cost_title=cost_title,
                     spent_money=spent_money,
                     group_id=group_id)


class Needs(db.Model):

    __tablename__ = 'needs'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    who_posted = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, description, group_id, user_id):
        self.description = description
        self.group_id = group_id
        self.who_posted = user_id

    def __repr__(self):
        return f"Need {self.description} as soon as possible"

    def to_json(self):
        json_needs = {
            'url': url_for('api.get_need', id=self.id, _external=True),
            'text': self.text,
            'done': self.done,
            'group': url_for('api.get_group', id=self.group_id, _external=True),
            'author': url_for('api.get_user', id=self.who_posted, _external=True)
        }
        return json_needs

    @staticmethod
    def from_json(json_need):
        description = json_need.get('description')
        group_id = json_need.get('group_id')

        return Needs(description, group_id)


class CostGroup(db.Model):

    __tablename__ = 'cost_groups'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    group_member = db.relationship('User', backref='group', lazy=True)

    def __init__(self, user_id, group_id):
        self.user_id = user_id
        self.group_id = group_id


class Groups(db.Model):

    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    cost_group = db.relationship('CostGroup', backref='cost_group', lazy=True)

    def __init__(self, name):
        self.name = name

    def to_json(self):
        json_group = {

            'url': url_for('api.get_group', id=self.id, _external=True),
            'name': self.name,
            }
        return json_group

    @staticmethod
    def from_json(group_json):
        name = group_json.get('name')
        return Groups(name)


class WhoOwesWhom(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    who = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    whom = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    debt_amount = db.Column(db.Integer)

    def __init__(self, who, whom, group_id):
        self.who = who
        self.whom = whom
        self.group_id = group_id
        self.debt_amount = 0

    @property
    def get_amount(self):
        return self.debt_amount

    def set_amount(self, amount):

        self.debt_amount = amount

    def to_json(self):
        json_wow = {
            'url': url_for('api.get_group_calculation', group_id=self.id, _external=True)
                }
        return json_wow
