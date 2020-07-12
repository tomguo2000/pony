from application.common.foundation import db


class OrderModel(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    thunderservice_id = db.Column(db.Integer)
    placeOrderTime = db.Column(db.BigInteger)
    coupon = db.Column(db.String(20))
    paymentMethod = db.Column(db.String(20))
    paymentTime = db.Column(db.BigInteger)
    paymentSN = db.Column(db.String(100))
    emailNotification = db.Column(db.Boolean)
    amount = db.Column(db.Float)
    orderStatus = db.Column(db.String(20))
    thunderserviceStatus = db.Column(db.String(20))

    def __repr__(self):
        return '<OrderModel %r>' % (self.id)