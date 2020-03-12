from application.common.foundation import db


class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=True, nullable=False)
    usergroup = db.Column(db.String(2), unique=True, nullable=True)
    membership = db.Column(db.String(2), unique=True, nullable=True)
    membership_starttime = db.Column(db.DateTime, unique=True, nullable=True)
    membership_endtime = db.Column(db.DateTime, unique=True, nullable=True)
