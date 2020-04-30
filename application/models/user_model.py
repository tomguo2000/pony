from application.common.foundation import db


class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=True)
    admin = db.Column(db.Boolean)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    usergroup = db.Column(db.String(2),  nullable=True)
    membership = db.Column(db.String(2), nullable=True)
    membership_starttime = db.Column(db.DateTime, nullable=True)
    membership_endtime = db.Column(db.DateTime, nullable=False)
    token = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<UserModel %r>' % (self.email)