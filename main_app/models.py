from main_app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime




class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, index=True, unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(128))
    profile_image = db.Column(db.String(128), nullable=False, default='default_profile_img.png')
    costs_id = db.Column(db.Integer, db.ForeignKey('costs.id'))

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

    spent_money = db.Column(db.Float, nullable=False, default=0.00)

    who_spent = db.relationship('User', backref='cost')

    purchase_time = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, cost_name, spent_money, who_spent):
        self.cost_name = cost_name
        self.spent_money = spent_money
        self.who_spent = who_spent

    def __repr__(self):
        return f"{self.cost_name} was spent {self.spent_money} UAN by {self.who_spent} at {self.purchase_time} "


class Needs(db.Model):

    __tablename__ = 'needs'

    id = db.Column(db.Integer, primary_key=True)

    description = db.Column(db.Text)

    done = db.Column(db.Boolean, default=False)

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return f"Need {self.description} as soon as possible"