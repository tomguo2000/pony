from application.common.foundation import db

class UserGroupModel(db.Model):
    __tablename__ = 'usergroup'

    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(50), nullable=True)
    maxUserCapacity = db.Column(db.Integer, nullable=True)    #maxUserCapacity
    maxPwdCapacity = db.Column(db.Integer, nullable=True)    #maxPwdCapacity will > maxUserCapacity always
    current_used = db.Column(db.Integer, default=0, nullable=True)
    which_thunderservice = db.Column(db.String(40))




    def __repr__(self):
        return '<UserGroupModel %r>' % (self.id)