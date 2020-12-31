from application.common.foundation import db


class ThunderserviceModel(db.Model):
    __tablename__ = 'thunderservice'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    membershipCN = db.Column(db.String(20), nullable=False)
    membershipEN = db.Column(db.String(20), nullable=False)
    duration = db.Column(db.Integer)
    defaultClientAmount = db.Column(db.Integer)
    defaultTrafficAmount = db.Column(db.Integer)
    price = db.Column(db.Float)
    onSalePrice = db.Column(db.Float)
    promotion = db.Column(db.Boolean)
    description = db.Column(db.String(100))


    def __repr__(self):
        return '<ThunderserviceModel %r>' % (self.id)