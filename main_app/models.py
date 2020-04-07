from main_app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from flask import current_app

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
    profile_image = db.Column(db.String(128), nullable=False, default='default_profile_img.png')
    costs = db.relationship('Costs', backref='author', lazy=True)
    group_member = db.relationship('CostGroup', backref='group', lazy=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Name = {self.username} "


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


class Needs(db.Model):

    __tablename__ = 'needs'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)
    comments = db.relationship('Comments', backref='needs', lazy=True)

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return f"Need {self.description} as soon as possible"


class Comments(db.Model):

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    time = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('needs.id'), nullable=False)

    def __init__(self, text, user_id, post_id):

        self.text = text
        self.user_id = user_id
        self.post_id = post_id

    def __repr__(self):
        return f"Comment ID {self.id} -- Date {self.time}"


class CostGroup(db.Model):

    __tablename__ = 'cost_groups'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)

    def __init__(self, user_id, group_id):
        self.user_id = user_id
        self.group_id = group_id


class Groups(db.Model):

    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)

    def __init__(self, name):
        self.name = name


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

    @property
    def debt_amount(self):
        return self.debt_amount

    @debt_amount.setter
    def debt_amount(self, amount):
        self.debt_amount = amount


