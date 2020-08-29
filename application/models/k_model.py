from application.common.foundation import db


class KModel(db.Model):
    __tablename__ = 'k'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    yearly = db.Column(db.String(20))
    monthly = db.Column(db.String(20))
    daily = db.Column(db.String(20))
    hourly = db.Column(db.String(20))
    minutely = db.Column(db.String(20))
    timestamp = db.Column(db.BigInteger)
    action = db.Column(db.String(20))
    parameter1 = db.Column(db.String(50))
    parameter2 = db.Column(db.String(50))

    def __repr__(self):
        return '<k %r>' % (self.id)