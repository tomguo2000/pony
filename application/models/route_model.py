from application.common.foundation import db


class RouteModel(db.Model):
    __tablename__ = 'routes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sequence = db.Column(db.Integer, nullable=True)
    online = db.Column(db.Boolean)
    domain = db.Column(db.String(100), nullable=True)
    ipaddress = db.Column(db.String(15), nullable=True)
    port = db.Column(db.Integer, nullable=True)
    servernameEN = db.Column(db.String(100), nullable=True)
    servernameCN = db.Column(db.String(100), nullable=True)
    routeStarttime = db.Column(db.BigInteger)
    trafficLimit = db.Column(db.Integer, nullable=True)
    trafficUsed = db.Column(db.Integer, nullable=True)
    trafficResetDay = db.Column(db.String(2), nullable=True)
    usergroup_id = db.Column(db.Integer, db.ForeignKey('usergroup.id'))

    def __repr__(self):
        return '<RouteModel %r>' % (self.id)