from application.common.foundation import db

class LogsModel(db.Model):
    __tablename__ = 'logs'

    id = db.Column(db.Integer, primary_key=True)
    logtime = db.Column(db.String(50), nullable=True)
    content = db.Column(db.String(1024), nullable=True)
    user_id =  db.Column(db.Integer)
    remote_ip = db.Column(db.String(15), nullable=True)

    # def set_password(self, password):
        # self.password_hash = generate_password_hash(password)

    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<LogsModel %r>' % (self.id)