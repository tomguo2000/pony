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
    servernameEN = db.Column(db.String(100), nullable=True)
    servernameCN = db.Column(db.String(100), nullable=True)
    routeStartTime = db.Column(db.BigInteger)
    routeExpTime = db.Column(db.BigInteger)
    trafficLimit = db.Column(db.Integer, nullable=True)
    trafficUsed = db.Column(db.Integer, nullable=True)
    trafficStartAt = db.Column(db.BigInteger)
    trafficResetDay = db.Column(db.BigInteger)
    usergroup_id = db.Column(db.Integer)
    lastCheckTime  = db.Column(db.BigInteger)
    certificateExpTime = db.Column(db.BigInteger)
    availablePwd = db.Column(db.Integer)
    routeLocalTime = db.Column(db.String(50))

    def __repr__(self):
        return '<RouteModel %r>' % (self.id)

class CpuIOModel(db.Model):
    __tablename__ = 'cpuio'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ipaddress = db.Column(db.String(15))
    cpu = db.Column(db.Float)
    mem = db.Column(db.Float)
    addtime  = db.Column(db.BigInteger)

    def __repr__(self):
        return '<CpuIOModel %r>' % (self.id)

class DiskIOModel(db.Model):
    __tablename__ = 'diskio'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ipaddress = db.Column(db.String(15))
    read_count = db.Column(db.Integer)
    write_count = db.Column(db.Integer)
    read_bytes = db.Column(db.Integer)
    write_bytes = db.Column(db.Integer)
    read_time = db.Column(db.BigInteger)
    write_time = db.Column(db.BigInteger)
    addtime  = db.Column(db.BigInteger)

    def __repr__(self):
        return '<DiskIOModel %r>' % (self.id)

class LoadAverageModel(db.Model):
    __tablename__ = 'load_average'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ipaddress = db.Column(db.String(15))
    one = db.Column(db.Float)
    five = db.Column(db.Float)
    fifteen = db.Column(db.Float)
    addtime  = db.Column(db.BigInteger)

    def __repr__(self):
        return '<LoadAverageModel %r>' % (self.id)

class NetworkModel(db.Model):
    __tablename__ = 'network'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ipaddress = db.Column(db.String(15))
    up = db.Column(db.Integer)
    down = db.Column(db.Integer)
    total_up = db.Column(db.Integer)
    total_down = db.Column(db.Integer)
    up_packets = db.Column(db.Integer)
    down_packets = db.Column(db.Integer)
    addtime  = db.Column(db.BigInteger)

    def __repr__(self):
        return '<NetworkModel %r>' % (self.id)

class OnlineUserAmountModel(db.Model):
    __tablename__ = 'onlineuseramount'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ipaddress = db.Column(db.String(15))
    online_user_amount = db.Column(db.Integer)
    server_local_time = db.Column(db.String(50))
    server_start_time = db.Column(db.String(50))
    addtime  = db.Column(db.BigInteger)

    def __repr__(self):
        return '<OnlineUserAmountModel %r>' % (self.id)