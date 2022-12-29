from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.schema import ForeignKey
from flask_login import UserMixin

db = SQLAlchemy()


# model to store user information who sing-up to caste their vote
class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_num = db.Column(db.Integer, nullable=False, unique=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    admin = db.Column(db.Integer, default=0)
    votes = db.relationship('VotesModel')


# model to store voting information
class VotesModel(db.Model):
    __tablename__ = 'votes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_num = db.Column(db.Integer, nullable=False, unique=True)
    voter_id = db.Column(db.Integer, ForeignKey('users.id', ondelete='CASCADE'))
    post_1 = db.Column(db.Integer, nullable=False)
    post_2 = db.Column(db.Integer, nullable=False)


# model to store the information of candidate who are stand in election
class CandidateModel(db.Model):
    __tablename__ = 'candidates'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_num = db.Column(db.Integer, nullable=False, unique=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80))
    batch = db.Column(db.String(120), nullable=False)
    course = db.Column(db.String(120), nullable=False)
    department = db.Column(db.String(120), nullable=False)
    post = db.Column(db.String(80), nullable=False)
    agenda = db.Column(db.String(300), default="No agenda")
