from main_app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, index=True, unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(128))
    profile_image = db.Column(db.String(128), nullable=False, default='default_profile_img.png')
    costs = db.relationship('Costs', backref='author', lazy=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

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

    def __init__(self, cost_title, spent_money, who_spent):
        self.cost_title = cost_title
        self.spent_money = spent_money
        self.who_spent = who_spent

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





