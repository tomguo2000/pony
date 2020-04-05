from application.common.foundation import db


class UserGroupModel(db.Model):
    __tablename__ = 'usergroup'

    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(50), nullable=True)
    maxcapacity = db.Column(db.Integer, nullable=True)
    current_capacity = db.Column(db.Integer, default=0, nullable=True)