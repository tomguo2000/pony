from application.common.foundation import db


class PWResourcesModel(db.Model):
    __tablename__ = 'pwresources'

    id = db.Column(db.Integer, primary_key=True)
    oripassword = db.Column(db.String(56), nullable=True)
    hashedpassword = db.Column(db.String(56), nullable=True)
    user_id = db.Column(db.Integer)
    usergroup_id = db.Column(db.Integer, db.ForeignKey('usergroup.id'))



    def __repr__(self):
        return '<PWResourcesModel %r>' % (self.id)