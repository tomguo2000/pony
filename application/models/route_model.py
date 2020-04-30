from application.common.foundation import db


class RouteModel(db.Model):
    __tablename__ = 'routes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_id = db.Column(db.Integer, nullable=True)
    sequence = db.Column(db.Integer, nullable=True)
    online = db.Column(db.Integer, nullable=True)
    domain = db.Column(db.String(100), nullable=True)
    ipaddress = db.Column(db.String(15), nullable=True)
    servernameEN = db.Column(db.String(100), nullable=True)
    servernameCN = db.Column(db.String(100), nullable=True)
    routeStarttime = db.Column(db.DateTime, nullable=True)
    trafficLimit = db.Column(db.Integer, nullable=True)
    trafficUsed = db.Column(db.Integer, nullable=True)
    trafficResetDay = db.Column(db.String(2), nullable=True)

    def __repr__(self):
        return '<RouteModel %r>' % (self.id)