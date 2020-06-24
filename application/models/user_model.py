from application.common.foundation import db
from werkzeug.security import generate_password_hash, check_password_hash


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    admin = db.Column(db.Boolean)
    email = db.Column(db.String(50), unique=True, nullable=False)
    email_verified = db.Column(db.Boolean)
    account_status = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(50), nullable=False)
    register_source = db.Column(db.String(50), nullable=True)
    register_datetime = db.Column(db.BigInteger)
    thunderservice_starttime = db.Column(db.BigInteger)
    thunderservice_endtime = db.Column(db.BigInteger)
    token = db.Column(db.String(255), nullable=True)
    refreshToken = db.Column(db.String(255), nullable=True)
    usergroup_id = db.Column(db.Integer)
    thunderservice_id = db.Column(db.Integer)
    last_login_datetime = db.Column(db.BigInteger)
    last_login_ipaddress = db.Column(db.String(50), nullable=True)
    mentor = db.Column(db.Integer)
    individual_coupon = db.Column(db.String(50), nullable=True)
    affiliate = db.Column(db.Boolean)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
