from application.common.foundation import db


class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=True)
    admin = db.Column(db.Boolean)
    email = db.Column(db.String(50), unique=True, nullable=False)
    email_verified = db.Column(db.String(10), nullable=True)
    account_status = db.Column(db.String(10), nullable=True)
    password = db.Column(db.String(50), nullable=False)
    register_source = db.Column(db.String(50), nullable=True)
    register_datetime = db.Column(db.DateTime, nullable=True)
    service_starttime = db.Column(db.DateTime, nullable=True)
    service_endtime = db.Column(db.DateTime, nullable=True)
    token = db.Column(db.String(255), nullable=True)
    usergroup_id = db.Column(db.Integer)
    thunderservice_id = db.Column(db.Integer)
    last_login_datetime = db.Column(db.DateTime, nullable=True)
    last_login_ipaddress = db.Column(db.String(50), nullable=True)
    mentor = db.Column(db.Integer)
    individual_coupon = db.Column(db.String(50), nullable=True)
    affiliate = db.Column(db.Boolean)


    def __repr__(self):
        return '<UserModel %r>' % (self.email)