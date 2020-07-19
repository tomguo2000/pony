from application.common.foundation import db


class RouteModel(db.Model):
    __tablename__ = 'routes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sequence = db.Column(db.Integer, nullable=True)
    online = db.Column(db.Boolean)
    domain = db.Column(db.String(100), nullable=True)
    ipaddress = db.Column(db.String(15), nullable=True)
    port = db.Column(db.Integer, nullable=True)
    ipv6 =  db.Column(db.Boolean)
    trojanVersion = db.Column(db.String(100))
    onlineUserAmount = db.Column(db.Integer)
    servernameEN = db.Column(db.String(100), nullable=True)
    servernameCN = db.Column(db.String(100), nullable=True)
    routeStartTime = db.Column(db.BigInteger)
    routeExpTime = db.Column(db.BigInteger)
    trafficLimit = db.Column(db.Integer, nullable=True)
    trafficUsed = db.Column(db.Integer, nullable=True)
    trafficResetDay = db.Column(db.String(2), nullable=True)
    usergroup_id = db.Column(db.Integer)
    lastCheckTime  = db.Column(db.BigInteger)
    certificateExpTime = db.Column(db.BigInteger)

    def __repr__(self):
        return '<RouteModel %r>' % (self.id)