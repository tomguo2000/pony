from application.common.foundation import db


class PWResourcesModel(db.Model):
    __tablename__ = 'pwresources'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, nullable=True)
    oripassword = db.Column(db.String(56), nullable=True)
    hashedpassword = db.Column(db.String(56), nullable=True)
    uid = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<PWResourcesModel %r>' % (self.id)